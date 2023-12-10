from databricks import sql
import os
import pandas as pd

connection = sql.connect(
                        server_hostname = "adb-1767346969741129.9.azuredatabricks.net",
                        http_path = "/sql/1.0/warehouses/a20e8d116459b6d7",
                        access_token = "dapib2db61506df9e84e6e932b33e8600dd4-3")

ticker = 'AAPL' #make this dynamic in the code
rows = 1000 #decide how many rows you want to pull


cursor = connection.cursor()
query = "SELECT * FROM historical_data where Ticker = '"+ticker+"' order by timestamp desc limit "+str(rows)
cursor.execute(query)
df = pd.DataFrame(cursor.fetchall())
df.columns = [desc[0] for desc in cursor.description]


cursor.close()
connection.close()

print(df.head())