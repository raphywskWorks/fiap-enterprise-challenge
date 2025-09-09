import mysql.connector
import pandas as pd

# Configurações de conexão
config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "database"
}

# Caminhos
sql_file = "src/app/database/DLL.sql"
output_csv = "src/app/database/sensores.csv"

# Conexão com o MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Carrega e executa o SQL
with open(sql_file, "r", encoding="utf-8") as f:
    sql_query = f.read()

# Usa pandas para ler o resultado diretamente
df = pd.read_sql(sql_query, conn)

# Exporta para CSV
df.to_csv(output_csv, index=False, encoding="utf-8")

# Fecha conexão
cursor.close()
conn.close()

print(f"✅ CSV gerado em {output_csv} com {len(df)} linhas.")
