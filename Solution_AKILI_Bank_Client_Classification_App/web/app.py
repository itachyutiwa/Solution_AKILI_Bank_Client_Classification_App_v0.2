import streamlit as st
import requests
import pandas as pd
import json
from io import BytesIO
import base64
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import altair as alt
# URL de l'API
url = ['http://localhost:8000/predictions','http://localhost:9000/predictions']
df = pd.read_excel("../data/donnees_labelisees.xlsx") 
# Chargement des données
data = df.copy()

#Quelques statistiques descriptives
# calculer la moyenne de la balance
balance_mean = round(data['BALANCE'].mean(),2)
# calculer le taux de fréquence d'achat moyen
purchases_freq_mean = round(data['PURCHASES_FREQUENCY'].mean()*100,2)
# calculer le nombre total d'achats
purchases_trx_sum = round(float(data['PURCHASES_TRX'].sum()),2)
# calculer le montant des paiements moyens
payments_mean = round(data['PAYMENTS'].mean(),2)


# KPI 1 : Solde moyen des comptes
avg_balance = data['BALANCE'].mean()
# Calcul du ratio d'achats ponctuels
oneoff_purchase_ratio = data['ONEOFF_PURCHASES'].sum() / data['PURCHASES'].sum()
# Calcul du nombre total de transactions pour chaque groupe de clients
grouped_df = data.groupby('cluster_result')['PURCHASES_TRX'].sum()
# Calcul du solde moyen quotidien (ADB)
data['ADB'] = data['BALANCE'] / data['TENURE']
# Calcul du montant total des achats
data['TOTAL_PURCHASES'] = data['ONEOFF_PURCHASES'] + data['INSTALLMENTS_PURCHASES']

# Préparer les données pour la prédiction
cols = [['BALANCE','BALANCE_FREQUENCY','PURCHASES','ONEOFF_PURCHASES','INSTALLMENTS_PURCHASES','CASH_ADVANCE','PURCHASES_FREQUENCY','ONEOFF_PURCHASES_FREQUENCY','PURCHASES_INSTALLMENTS_FREQUENCY','CASH_ADVANCE_FREQUENCY','CASH_ADVANCE_TRX','PURCHASES_TRX','CREDIT_LIMIT','PAYMENTS','MINIMUM_PAYMENTS','PRC_FULL_PAYMENT','TENURE'],['BALANCE','BALANCE_FREQUENCY','PURCHASES','INSTALLMENTS_PURCHASES','CASH_ADVANCE','ONEOFF_PURCHASES_FREQUENCY','PURCHASES_INSTALLMENTS_FREQUENCY','CASH_ADVANCE_TRX','PURCHASES_TRX','CREDIT_LIMIT','PAYMENTS','MINIMUM_PAYMENTS','PRC_FULL_PAYMENT','TENURE']]
# Fonction pour envoyer la requête POST à l'API
def predict_client_classification(data):
    #data.to_dict(orient='records')
    response = requests.post(url[0], json=data)
    if response.ok:
        result = response.json()
        return result['prediction']
    else:
        st.error('Erreur lors de la prédiction.')

def predict_client_classification_no_corr(data):
    response = requests.post(url[1], json=data)
    if response.ok:
        result = response.json()
        return result['prediction']
    else:
        st.error('Erreur lors de la prédiction.')

def download_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_file_download_link(processed_data, file_name, file_label):
    b64 = base64.b64encode(processed_data)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{file_name}">{file_label}</a>'
    return href
# Volet de navigation
menu = ["Dashboard", "Formulaire", "Fichier Excel ou CSV"]
choice = st.sidebar.selectbox("Sélectionner une option", menu)

# Titre de l'application
st.title("Application de classification de clients bancaires")

# Affichage du formulaire si l'utilisateur a choisi l'option "Formulaire"
if choice == "Formulaire":

    # Formulaire pour saisir les données du client
    st.write("BALANCE *")
    balance = st.number_input('Solde du compte du client',  min_value=0.0, max_value=1000000.0, value=120.0,step=0.01, format="%.2f")

    st.write("BALANCE FREQUENCY *")
    balance_freq = st.number_input('Fréquence à laquelle le client vérifie son solde, exprimée en nombre de fois par mois', min_value=0.0, max_value=1.0, step=0.01, format="%.2f", value=0.50)

    st.write("PURCHASES *")
    purchases = st.number_input('Montant total des achats effectués par le client sur son compte', min_value=0.0, max_value=1000000.0, value=120.0,step=0.01, format="%.2f")

    st.write("ONEOFF PURCHASES")
    oneoff_purchases = st.number_input('Montant total des achats effectués en une seule fois par le client', min_value=0.0, max_value=1000000.0, value=0.0,step=0.01, format="%.2f")

    st.write("INSTALLMENTS PURCHASES *")
    installements_purchases = st.number_input('Montant total des achats effectués en plusieurs fois par le client', min_value=0.0, max_value=1000000.0, value=200.0,step=0.01, format="%.2f")

    st.write("CASH ADVANCE *")
    cash_advance = st.number_input('Montant total des avances de fonds effectuées par le client sur son compte', min_value=0.0, max_value=1000000.0, value=300.0,step=0.01, format="%.2f")

    st.write("PURCHASES FREQUENCY")
    purchases_freq = st.number_input('Fréquence à laquelle le client effectue des achats sur son compte', min_value=0.0, max_value=1.0, value=0.0,step=0.01, format="%.2f")

    st.write("ONEOFF PURCHASES FREQUENCY *")
    oneoff_purchases_freq = st.number_input('Fréquence à laquelle le client effectue des achats en une seule fois sur son compte.', min_value=0.0, max_value=1.0, value=0.30,step=0.01, format="%.2f")

    st.write("PURCHASES INSTALLMENTS FREQUENCY *")
    purchases_installments_freq = st.number_input('Fréquence à laquelle le client effectue des achats en plusieurs fois sur son compte.', min_value=0.0, max_value=1.0, value=0.30,step=0.01, format="%.2f")

    st.write("CASH ADVANCE FREQUENCY")
    cash_advance_freq = st.number_input('Fréquence à laquelle le client effectue des avances de fonds sur son compte.', min_value=0.0, max_value=1.0, value=0.0,step=0.01, format="%.2f")

    st.write("CASH ADVANCE TRANSACTION *")
    cash_advance_trx = st.number_input("Nombre total de transactions d'avance de fonds effectuées par le client sur son compte", min_value=0.0, max_value=1000000.0, value=3000.0,step=0.01, format="%.2f")

    st.write("PURCHASES TRANSACTION *")
    purchases_trx = st.number_input("Nombre total de transactions d'achat effectuées par le client sur son compte", min_value=0.0, max_value=1000000.0, value=700.0,step=0.01, format="%.2f")


    st.write("CREDIT LIMIT *")
    credit_limit = st.number_input("Limite de crédit du client, c'est-à-dire le montant maximum qu'il peut dépenser sur son compte", min_value=0.0, max_value=1000000.0, value=10.0,step=0.01, format="%.2f")

    st.write("PAYMENTS *")
    payment = st.number_input('Montant total des paiements effectués par le client sur son compte', min_value=0.0, max_value=1000000.0, value=5000.0,step=0.01, format="%.2f")

    st.write("MINIMUM PAYMENTS *")
    minimum_payment = st.number_input("Montant minimum des paiements que le client doit effectuer chaque mois sur son compte", min_value=0.0, max_value=1000000.0, value=6000.0,step=0.01, format="%.2f")

    st.write("PERCENTAGE OF FULL PAYMENT *")
    pct_full_payment = st.number_input("Pourcentage du solde du compte qui est payé en entier chaque mois par le client", min_value=0.0, max_value=1000000.0, value=50000.0,step=0.01, format="%.2f")

    st.write("TENURE *")
    tenure = st.slider('Nombre de mois pendant lesquels le client a été client de la banque.', min_value=1, max_value=12, value=7)


    data = {
            'BALANCE': balance,
            'BALANCE_FREQUENCY': balance_freq,
            'PURCHASES': purchases,
            'ONEOFF_PURCHASES': oneoff_purchases,
            'INSTALLMENTS_PURCHASES': installements_purchases,
            'CASH_ADVANCE': cash_advance,
            'PURCHASES_FREQUENCY': purchases_freq,
            'ONEOFF_PURCHASES_FREQUENCY': oneoff_purchases_freq,
            'PURCHASES_INSTALLMENTS_FREQUENCY': purchases_installments_freq,
            'CASH_ADVANCE_FREQUENCY': cash_advance_freq,
            'CASH_ADVANCE_TRX': cash_advance_trx,
            'PURCHASES_TRX': purchases_trx,
            'CREDIT_LIMIT': credit_limit,
            'PAYMENTS': payment,
            'MINIMUM_PAYMENTS': minimum_payment,
            'PRC_FULL_PAYMENT': pct_full_payment,
            'TENURE': tenure
            }


    data_no_corr = {
                'BALANCE': balance,
            'BALANCE_FREQUENCY': balance_freq,
            'PURCHASES': purchases,
            'INSTALLMENTS_PURCHASES': installements_purchases,
            'CASH_ADVANCE': cash_advance,
            'ONEOFF_PURCHASES_FREQUENCY': oneoff_purchases_freq,
            'PURCHASES_INSTALLMENTS_FREQUENCY': purchases_installments_freq,
            'CASH_ADVANCE_TRX': cash_advance_trx,
            'PURCHASES_TRX': purchases_trx,
            'CREDIT_LIMIT': credit_limit,
            'PAYMENTS': payment,
            'MINIMUM_PAYMENTS': minimum_payment,
            'PRC_FULL_PAYMENT': pct_full_payment,
            'TENURE': tenure
            }


    # Bouton pour lancer la prédiction
    if st.button('Prédire la catégorie de ce client'):
    # Conversion des données en dictionnaire
        if oneoff_purchases != 0.0 or  purchases_freq != 0 or cash_advance_freq != 0:
            prediction = predict_client_classification(data)
        elif oneoff_purchases == 0.0 and  purchases_freq == 0 and cash_advance_freq == 0:
            prediction = predict_client_classification_no_corr(data_no_corr)
        if prediction:
        # Affichage de la prédiction
            st.success(f"Le client est classé dans la catégorie {prediction}")

elif choice == "Fichier Excel ou CSV":
    # Charger le fichier CSV
    file = st.file_uploader("Sélectionner un fichier Excel(.xlsx)", type=["xlsx"])
    
    if file is not None:
        data = pd.read_excel(file)
        data_corr = data.copy()
        data_corr = data_corr[cols[0]] 
                 
        # Conversion du DataFrame en dictionnaire Python
        data_dict = data_corr.to_dict()
        # Conversion du dictionnaire en format JSON
        #data_corr = json.dumps(data_corr)
        


        #data_no_corr = data.copy()
        #data_no_corr = data_no_corr[cols[1]]
        #data_no_corr = data_no_corr.to_dict(orient='records')
        #Bouton pour lancer la prédiction

 
        if st.button('Prédire la catégorie de chaque client du fichier .xlsx'):            
            prediction_corr = predict_client_classification(data_dict)
            #prediction_n_c = predict_client_classification_no_corr(data_no_corr)
            df = pd.DataFrame({"Prédictions":prediction_corr})
            if prediction_corr:
            # Affichage de la prédiction
                st.write(df.head())
        # créer un bouton de téléchargement pour le DataFrame au format Excel
                file_name = "predictions.xlsx"
                file_label = "Télécharger les prédictions au format .xlsx"
                data_to_download = download_excel(df)
                st.markdown(get_file_download_link(data_to_download, file_name, file_label), unsafe_allow_html=True)




elif choice == "Dashboard":
    
   # Création des panels avec des couleurs de fond différentes
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div style="background-color: #F0F8FF; padding: 10px; text-align:center;font-weight:bold">SOLDE MOYEN : {:.2f}</div>'.format(balance_mean), unsafe_allow_html=True)
    col2.markdown('<div style="background-color: #FFE4E1; padding: 10px;text-align:center;font-weight:bold">FREQUENCE ACHAT : {:.2f}</div>'.format(purchases_freq_mean), unsafe_allow_html=True)
    col3.markdown('<div style="background-color: #E0FFFF; padding: 10px;text-align:center;font-weight:bold">TOTAL ACHAT : {:.2f}</div>'.format(purchases_trx_sum), unsafe_allow_html=True)
    col4.markdown('<div style="background-color: #F5F5DC; padding: 10px;text-align:center;font-weight:bold">PAYEMENT MOYEN : {:.2f}</div>'.format(purchases_freq_mean), unsafe_allow_html=True)

    # Affichage des statistiques dans chaque panel
    with col1:
        st.subheader('')

    with col2:
        st.subheader('')

    with col3:
        st.subheader('')

    with col4:
        st.subheader('')

            


    # Affichage de l'histogramme du solde des comptes dans le
    fig = px.histogram(data, x='BALANCE', nbins=20, title='Solde des comptes',
                        labels={'BALANCE':'Solde', 'Nombre':'Fréquence'})
    fig.add_vline(x=avg_balance, line_color='red', line_dash='dash', line_width=2,
                    annotation_text=f'Solde moyen: {avg_balance:.2f}', annotation_position='top left')
    st.plotly_chart(fig)



    # Affichage du graphique du ratio d'achats ponctuels dans le dashboard

    fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
    # Ajout du graphique camembert
    brown_colors = ['#8B0000', ' #DC143C']
    fig.add_trace(go.Pie(labels=['Achats ponctuels', 'Achats en plusieurs fois'],
                         values=[oneoff_purchase_ratio, 1-oneoff_purchase_ratio],
                         textposition='inside',
                         hole=0.6,
                         showlegend=False,marker=dict(colors=brown_colors)), 1, 1)
    # Ajout du titre
    fig.update_layout(title={'text': "Ratio d'achats ponctuels",
                              'y':0.90,
                              'x':0.50,
                              'xanchor': 'center',
                              'yanchor': 'top'})
    # Ajout de l'annotation
    fig.add_annotation(text='Majorité des achats: Achats ponctuels',
                       x=0.70,
                       y=0.60,
                       showarrow=True,
                       arrowhead=1,
                       arrowcolor='black',
                       arrowsize=1.5,
                       arrowwidth=2,
                       ax=80,
                       ay=-70)

    st.plotly_chart(fig)


    # Tri des clusters par ordre croissant du nombre total de transactions
    sorted_clusters = grouped_df.sort_values().index
    cluster_map = {cluster: i for i, cluster in enumerate(sorted_clusters)}

    # Définir la palette de couleurs pour chaque cluster
    colors = ['red', 'blue', 'purple', 'orange']

    # Création du graphique en barres groupées pour le nombre de transactions par groupe de clients
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[cluster_map[cluster] for cluster in grouped_df.index], 
        y=grouped_df.values,
        marker_color=[colors[cluster_map[cluster]] for cluster in grouped_df.index]
    ))

    # Configuration des axes et du titre
    fig.update_layout(
        xaxis_title='Groupe de clients',
        yaxis_title='Nombre total de transactions',
        title='Nombre de transactions par groupe de clients'
    )

    # Ajout de la légende pour les couleurs de chaque cluster
    for i in cluster_map.values():
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=10, color=colors[i]), name='Cluster {}'.format(i+1)))

    # Affichage du graphique interactif
    st.plotly_chart(fig)


    # Tracer un nuage de points du montant total des achats par rapport à l'ADB
    # Création d'un scatter plot du montant total des achats par rapport à l'ADB
    fig = px.scatter(data, x='ADB', y='TOTAL_PURCHASES', color='cluster_result', color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(title='Montant total des achats par rapport au solde moyen quotidien',
                    xaxis_title='Solde moyen quotidien (ADB)',
                    yaxis_title='Montant total des achats')

    # Affichage du graphique interactif dans Streamlit
    st.plotly_chart(fig)








               

