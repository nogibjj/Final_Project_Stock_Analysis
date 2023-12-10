from databricks import sql
import os
import pandas as pd

connection = sql.connect(
    server_hostname="adb-4423504648358422.2.azuredatabricks.net",
    http_path="/sql/1.0/warehouses/7d72b517b57b8469",
    access_token="dapic9d7c95828eadc03c905d560bc7de436-3",
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM songs")
df = pd.DataFrame(cursor.fetchall())
df.columns = [desc[0] for desc in cursor.description]

print(df.head())
cursor.close()
connection.close()
