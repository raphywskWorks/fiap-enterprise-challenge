"""
Classificação do estado da peça (Saudável / Desgastada / Crítica)
- Lê src/app/database/sensores.csv
- Consolida leituras por (id_peca, leitura_data_hora)
- Usa 'risco_falha' do CSV como rótulo (mapeado para nomes de negócio)
- Treina RandomForest e avalia em holdout temporal
- Gera matriz de confusão e relatório, salva em /assets
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import joblib


# Config
CSV_PATH = Path("src/app/database/sensores.csv")
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR = Path("src/machine_learning/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
RANDOM_SEED = 42

# Carregar dados

df = pd.read_csv(CSV_PATH, parse_dates=["leitura_data_hora"])
agg_cols = ["tempo_uso", "ciclos", "temperatura", "vibracao", "falha"]
df_agg = (
    df.sort_values(["id_peca", "leitura_data_hora"])
      .groupby(["id_peca", "leitura_data_hora"], as_index=False)[agg_cols + ["risco_falha"]]
      .agg({
          "tempo_uso": "max",
          "ciclos": "max",
          "temperatura": "max",
          "vibracao": "max",
          "falha": "max",
          "risco_falha": "last"
      })
)

# Mapear rótulos para nomes de negócio
map_rotulos = {"baixo": "Saudável", "medio": "Desgastada", "alto": "Crítica"}
df_agg["estado_peca"] = df_agg["risco_falha"].map(map_rotulos)

# Features e target
X = df_agg[["tempo_uso", "ciclos", "temperatura", "vibracao"]]
y = df_agg["estado_peca"]

# 70% inicial para treino, 30% final para teste
df_agg_sorted = df_agg.sort_values("leitura_data_hora")
cut_idx = int(len(df_agg_sorted) * 0.7)
train_data = df_agg_sorted.iloc[:cut_idx]
test_data  = df_agg_sorted.iloc[cut_idx:]

X_train = train_data[["tempo_uso", "ciclos", "temperatura", "vibracao"]]
y_train = train_data["estado_peca"]
X_test  = test_data[["tempo_uso", "ciclos", "temperatura", "vibracao"]]
y_test  = test_data["estado_peca"]

# Modelo
clf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    random_state=RANDOM_SEED,
    n_jobs=-1
)
clf.fit(X_train, y_train)

# Avaliação
y_pred = clf.predict(X_test)
print("\n=== Classification Report (Estado da Peça) ===")
print(classification_report(y_test, y_pred, digits=4))

cm = confusion_matrix(y_test, y_pred, labels=["Saudável", "Desgastada", "Crítica"])

plt.figure(figsize=(5,4))
plt.imshow(cm, interpolation='nearest')
plt.title('Matriz de Confusão - Estado da Peça')
plt.colorbar()
tick_marks = np.arange(3)
plt.xticks(tick_marks, ["Saudável", "Desgastada", "Crítica"], rotation=45)
plt.yticks(tick_marks, ["Saudável", "Desgastada", "Crítica"])
plt.ylabel('Real')
plt.xlabel('Previsto')
plt.tight_layout()
plt.savefig(ASSETS_DIR / "matriz_confusao_estado.png", dpi=140)
plt.close()

# Importância das features (explicabilidade rápida)
importances = pd.Series(clf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
print("\nImportância das features:\n", importances)

plt.figure(figsize=(6,4))
importances.plot(kind="bar")
plt.title("Importância das Features - Estado da Peça")
plt.tight_layout()
plt.savefig(ASSETS_DIR / "feature_importance_estado.png", dpi=140)
plt.close()

# Salvar modelo
joblib.dump(clf, MODEL_DIR / "modelo_estado_peca.joblib")
print(f"\n✅ Modelo salvo em {MODEL_DIR / 'modelo_estado_peca.joblib'}")
print(f"🖼️ Gráficos salvos em {ASSETS_DIR}/matriz_confusao_estado.png e feature_importance_estado.png")
