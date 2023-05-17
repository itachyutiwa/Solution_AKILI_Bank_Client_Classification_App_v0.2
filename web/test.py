import config
import database_connexion

cluster =config.environ['CLUSTER']
username =config.environ['USERNAME']
dbname =config.environ['DBNAME']
password =config.environ['PASSWORD']
configs = f"mongodb+srv://{username}:{password}@{cluster}.rnawsej.mongodb.net/"

print({"Cluster":cluster,"Username":username,"Dbname":dbname,"Password":password})
print(configs)
print(database_connexion.data_copy.head())

