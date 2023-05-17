import pandas as pd
import json

# Assuming you have a DataFrame named 'df'
df = pd.read_excel("../data/donnees_labelisees.xlsx") 
df['cluster_result'] = df['cluster_result'].replace({'Cluster 1.0': 1, 'Cluster 2.0': 2, 'Cluster 3.0': 3, 'Cluster 4.0': 4})

# Iterate over each column
for column in df.columns:
    # Create a dictionary from the column values
    column_dict = df[column].to_dict()
    
    # Convert the dictionary to JSON
    json_data = json.dumps(column_dict)
    
    # Save the JSON data to a file
    file_path = f"../collections/{column}.json"  
    with open(file_path, "w") as file:
        file.write(json_data)
