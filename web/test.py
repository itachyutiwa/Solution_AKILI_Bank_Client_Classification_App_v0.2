import config
import database_connexion
import pandas as pd
cluster =config.environ['CLUSTER']
username =config.environ['USERNAME']
dbname =config.environ['DBNAME']
password =config.environ['PASSWORD']
configs = f"mongodb+srv://{username}:{password}@{cluster}.rnawsej.mongodb.net/"

print({"Cluster":cluster,"Username":username,"Dbname":dbname,"Password":password})
print(configs)
print(database_connexion.data_copy.head())
df = pd.read_excel("../data/donnees_labelisees.xlsx")
df = df[df.columns[1:]]
print(df.head())

