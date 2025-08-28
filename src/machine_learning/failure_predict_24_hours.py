"""
Previsão de falha em horizonte fixo (próximas 24h)
- Lê src/app/database/sensores.csv
- Consolida por (id_peca, leitura_data_hora)
- Cria rótulo binário: há falha da mesma peça nos próximos 1 dia? (ajuste HORIZON_H)
- Gera features recentes (janelas) e treina um classificador (GradientBoosting)
- Avalia com ROC-AUC e matriz de confusão; salva gráficos em /assets
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
import joblib

# Config
CSV_PATH = Path("src/app/database/sensores.csv")
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR = Path("src/machine_learning/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

HORIZON_H = 24 # Tempo de previsão de falhas (próximas 24 horas)
RANDOM_SEED = 42

# Carregar e consolidar dados
df = pd.read_csv(CSV_PATH, parse_dates=["leitura_data_hora"])

agg_cols = ["tempo_uso", "ciclos", "temperatura", "vibracao", "falha"]
df_agg = (
    df.sort_values(["id_peca", "leitura_data_hora"])
      .groupby(["id_peca", "leitura_data_hora"], as_index=False)[agg_cols]
      .agg({
          "tempo_uso": "max",
          "ciclos": "max",
          "temperatura": "max",
          "vibracao": "max",
          "falha": "max"
      })
)

# Criar rótulo "falha nas próximas 24h"
def label_next_horizon(piece_df: pd.DataFrame, hours: int = 24) -> pd.DataFrame:
    piece_df = piece_df.sort_values("leitura_data_hora").copy()
    times = piece_df["leitura_data_hora"].values
    fail_times = piece_df.loc[piece_df["falha"] == 1, "leitura_data_hora"].values

    has_fail_next = np.zeros(len(piece_df), dtype=int)
    if len(fail_times) > 0:
        j = 0
        for i, t in enumerate(times):
            while j < len(fail_times) and fail_times[j] < t:
                j += 1
            k = j
            while k < len(fail_times) and (fail_times[k] - t).astype('timedelta64[h]').astype(int) <= hours:
                if (fail_times[k] - t).astype('timedelta64[h]').astype(int) > 0:
                    has_fail_next[i] = 1
                    break
                k += 1
    piece_df["fail_next_h"] = has_fail_next
    return piece_df

df_labeled = (
    df_agg.groupby("id_peca", group_keys=False)
          .apply(label_next_horizon, hours=HORIZON_H)
)

# Features com janelas (robustez temporal)
def add_window_features(piece_df: pd.DataFrame) -> pd.DataFrame:
    piece_df = piece_df.sort_values("leitura_data_hora").copy()
    # janelas em número de linhas
    windows = [3, 6, 12]
    for w in windows:
        piece_df[f"temp_mean_{w}"] = piece_df["temperatura"].rolling(w, min_periods=1).mean()
        piece_df[f"vib_mean_{w}"]  = piece_df["vibracao"].rolling(w, min_periods=1).mean()
        piece_df[f"temp_std_{w}"]  = piece_df["temperatura"].rolling(w, min_periods=1).std().fillna(0)
        piece_df[f"vib_std_{w}"]   = piece_df["vibracao"].rolling(w, min_periods=1).std().fillna(0)
        piece_df[f"ciclos_delta_{w}"] = piece_df["ciclos"].diff(w).fillna(0)
        piece_df[f"uso_delta_{w}"]    = piece_df["tempo_uso"].diff(w).fillna(0)
    return piece_df

df_feat = (
    df_labeled.groupby("id_peca", group_keys=False)
              .apply(add_window_features)
)

# Remove as primeiras linhas
df_feat = df_feat.dropna().reset_index(drop=True)

# 70% para treino e 30% para testes
df_feat = df_feat.sort_values("leitura_data_hora")
cut_idx = int(len(df_feat) * 0.7)
train = df_feat.iloc[:cut_idx]
test  = df_feat.iloc[cut_idx:]

feature_cols = [
    "tempo_uso", "ciclos", "temperatura", "vibracao",
    "temp_mean_3","vib_mean_3","temp_std_3","vib_std_3","ciclos_delta_3","uso_delta_3",
    "temp_mean_6","vib_mean_6","temp_std_6","vib_std_6","ciclos_delta_6","uso_delta_6",
    "temp_mean_12","vib_mean_12","temp_std_12","vib_std_12","ciclos_delta_12","uso_delta_12",
]
X_train = train[feature_cols]
y_train = train["fail_next_h"]
X_test  = test[feature_cols]
y_test  = test["fail_next_h"]

# Modelo
clf = GradientBoostingClassifier(random_state=RANDOM_SEED)
clf.fit(X_train, y_train)

# Avaliação
y_prob = clf.predict_proba(X_test)[:,1]
y_pred = (y_prob >= 0.5).astype(int)

print("\n=== Classification Report (Falha próximas 24h) ===")
print(classification_report(y_test, y_pred, digits=4))

try:
    auc = roc_auc_score(y_test, y_prob)
    print(f"ROC-AUC: {auc:.4f}")
except ValueError:
    print("ROC-AUC não pôde ser calculado (talvez apenas uma classe no conjunto de teste).")

cm = confusion_matrix(y_test, y_pred, labels=[0,1])

plt.figure(figsize=(5,4))
plt.imshow(cm, interpolation='nearest')
plt.title(f'Matriz de Confusão - Falha próximas {HORIZON_H}h')
plt.colorbar()
plt.xticks([0,1], ["Sem falha", "Falha"], rotation=45)
plt.yticks([0,1], ["Sem falha", "Falha"])
plt.ylabel('Real')
plt.xlabel('Previsto')
plt.tight_layout()
plt.savefig(ASSETS_DIR / f"matriz_confusao_falha_{HORIZON_H}h.png", dpi=140)
plt.close()

# Curva ROC
try:
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.figure(figsize=(5,4))
    plt.plot(fpr, tpr, label=f"AUC={auc:.3f}")
    plt.plot([0,1], [0,1], linestyle="--")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title(f"ROC - Falha próximas {HORIZON_H}h")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / f"roc_falha_{HORIZON_H}h.png", dpi=140)
    plt.close()
except Exception as e:
    pass

# Salvar modelo
joblib.dump(clf, MODEL_DIR / f"modelo_falha_{HORIZON_H}h.joblib")
print(f"\n✅ Modelo salvo em {MODEL_DIR / f'modelo_falha_{HORIZON_H}h.joblib'}")
print(f"🖼️ Gráficos salvos em {ASSETS_DIR}/matriz_confusao_falha_{HORIZON_H}h.png e roc_falha_{HORIZON_H}h.png")
