from flask import Flask, jsonify, request
import joblib
import pandas as pd

model = joblib.load("../model/RandomForest_One_Vs_All_No_Corr.pkl")
app = Flask(__name__)

@app.route('/predictions', methods=['POST'])
def predict():
    # Récupération des données JSON envoyées en POST
    data = request.get_json(force=True)
    # Transformation des données en dataframe pandas
    X = pd.DataFrame.from_dict(data, orient='index').transpose()
    # Prédiction avec le modèle chargé
    y_pred = model.predict(X)
    # Renvoi de la prédiction sous forme de réponse JSON
    return jsonify(prediction=y_pred.tolist())

if __name__ == '__main__':
    app.run(debug=True,port=9000)
