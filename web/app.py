import streamlit as st
import pandas as pd
import database_connexion
import statistiques_et_kpi
import generate_graphics
import use_api
import download_files

# URL de l'API
st.set_page_config(page_title="Classification Clients Banque", page_icon=":chart_with_upwards_trend:", layout="wide")

#local data file url 
file = "../data/donnees_labelisees.xlsx"
df = pd.read_excel(file)
df = df[df.columns[1:]]

#Database connexion via mongodb cluster
#df = database_connexion.data_copy

# Chargement des données
data = df.copy()
cols_seg = [
                    "BALANCE","BALANCE_FREQUENCY","PURCHASES",
                    "ONEOFF_PURCHASES","INSTALLMENTS_PURCHASES","CASH_ADVANCE","PURCHASES_FREQUENCY",
                    "ONEOFF_PURCHASES_FREQUENCY",
                    "PURCHASES_INSTALLMENTS_FREQUENCY","CASH_ADVANCE_FREQUENCY","CASH_ADVANCE_TRX",
                    "PURCHASES_TRX","CREDIT_LIMIT","PAYMENTS","MINIMUM_PAYMENTS","PRC_FULL_PAYMENT", "TENURE"
                    ,"cluster_result"
                    ]

##Quelques Keys Performances Indicators

# Calcul du solde moyen quotidien (ADB)
data['ADB'] = data['BALANCE'] / data['TENURE']

# Calcul du montant total des achats
data['TOTAL_PURCHASES'] = data['ONEOFF_PURCHASES'] + data['INSTALLMENTS_PURCHASES']

# Préparer les données pour la prédiction
cols = [['BALANCE','BALANCE_FREQUENCY','PURCHASES','ONEOFF_PURCHASES','INSTALLMENTS_PURCHASES','CASH_ADVANCE','PURCHASES_FREQUENCY','ONEOFF_PURCHASES_FREQUENCY','PURCHASES_INSTALLMENTS_FREQUENCY','CASH_ADVANCE_FREQUENCY','CASH_ADVANCE_TRX','PURCHASES_TRX','CREDIT_LIMIT','PAYMENTS','MINIMUM_PAYMENTS','PRC_FULL_PAYMENT','TENURE'],['BALANCE','BALANCE_FREQUENCY','PURCHASES','INSTALLMENTS_PURCHASES','CASH_ADVANCE','ONEOFF_PURCHASES_FREQUENCY','PURCHASES_INSTALLMENTS_FREQUENCY','CASH_ADVANCE_TRX','PURCHASES_TRX','CREDIT_LIMIT','PAYMENTS','MINIMUM_PAYMENTS','PRC_FULL_PAYMENT','TENURE']]


# Volet de navigation
menu = ["Dashboard", "Formulaire", "Importer un fichier Excel"]
# Options du dashboard
options_dashboard = ["Indicateurs", "Segments", "Marketing"]
choice = st.sidebar.selectbox("Sélectionner une option", menu)

# Titre de l'application
st.title("Application de classification de clients bancaires")

# Affichage du formulaire si l'utilisateur a choisi l'option "Formulaire"
if choice == "Formulaire":

    # Formulaire pour saisir les données du client

    st.markdown("<br><br> NB: Les champs précedés du symbole (<span style='color:red;'>*</span>) sont obligatoires.", unsafe_allow_html=True)
    st.markdown('SOLDE <span style="color:red;">*</span>', unsafe_allow_html=True)
    balance = st.number_input('Solde du compte du client',  min_value=0.0, max_value=1000000.0, value=120.0,step=0.01, format="%.2f")

    
    st.markdown('FRÉQUENCE DE SOLDE <span style="color:red;">*</span>', unsafe_allow_html=True)
    balance_freq = st.number_input('Fréquence à laquelle le client vérifie son solde, exprimée en nombre de fois par mois', min_value=0.0, max_value=1.0, step=0.01, format="%.2f", value=0.50)

    
    st.markdown('ACHATS <span style="color:red;">*</span>', unsafe_allow_html=True)
    purchases = st.number_input('Montant total des achats effectués par le client sur son compte', min_value=0.0, max_value=1000000.0, value=120.0,step=0.01, format="%.2f")

    st.write("ACHATS UNIQUES")
    oneoff_purchases = st.number_input('Montant total des achats effectués en une seule fois par le client', min_value=0.0, max_value=1000000.0, value=0.0,step=0.01, format="%.2f")

    st.write("ACHATS ÉCHELONNÉS ")
    st.markdown('ANCIENNETE <span style="color:red;">*</span>', unsafe_allow_html=True)
    installements_purchases = st.number_input('Montant total des achats effectués en plusieurs fois par le client', min_value=0.0, max_value=1000000.0, value=200.0,step=0.01, format="%.2f")

    
    st.markdown('AVANCE DE FONDS <span style="color:red;">*</span>', unsafe_allow_html=True)
    cash_advance = st.number_input('Montant total des avances de fonds effectuées par le client sur son compte', min_value=0.0, max_value=1000000.0, value=300.0,step=0.01, format="%.2f")
    
    st.write("FRÉQUENCE D'ACHATS")
    purchases_freq = st.number_input('Fréquence à laquelle le client effectue des achats sur son compte', min_value=0.0, max_value=1.0, value=0.0,step=0.01, format="%.2f")

   
    st.markdown("FRÉQUENCE D'ACHATS UNIQUES <span style='color:red;'>*</span>", unsafe_allow_html=True)
    oneoff_purchases_freq = st.number_input('Fréquence à laquelle le client effectue des achats en une seule fois sur son compte.', min_value=0.0, max_value=1.0, value=0.30,step=0.01, format="%.2f")

   
    st.markdown("FRÉQUENCE D'ACHATS ÉCHELONNÉS <span style='color:red;'>*</span>", unsafe_allow_html=True)
    purchases_installments_freq = st.number_input('Fréquence à laquelle le client effectue des achats en plusieurs fois sur son compte.', min_value=0.0, max_value=1.0, value=0.30,step=0.01, format="%.2f")

    st.write("FRÉQUENCE D'AVANCE DE FONDS")
    cash_advance_freq = st.number_input('Fréquence à laquelle le client effectue des avances de fonds sur son compte.', min_value=0.0, max_value=1.0, value=0.0,step=0.01, format="%.2f")

    
    st.markdown("TRANSACTIONS D'AVANCE DE FONDS <span style='color:red;'>*</span>", unsafe_allow_html=True)
    cash_advance_trx = st.number_input("Nombre total de transactions d'avance de fonds effectuées par le client sur son compte", min_value=0.0, max_value=1000000.0, value=3000.0,step=0.01, format="%.2f")

    
    st.markdown("TRANSACTIONS D'ACHATS <span style='color:red;'>*</span>", unsafe_allow_html=True)
    purchases_trx = st.number_input("Nombre total de transactions d'achat effectuées par le client sur son compte", min_value=0.0, max_value=1000000.0, value=700.0,step=0.01, format="%.2f")

  
    st.markdown("LIMITE DE CRÉDIT <span style='color:red;'>*</span>", unsafe_allow_html=True)
    credit_limit = st.number_input("Limite de crédit du client, c'est-à-dire le montant maximum qu'il peut dépenser sur son compte", min_value=0.0, max_value=1000000.0, value=10.0,step=0.01, format="%.2f")

    
    st.markdown("PAIEMENTS <span style='color:red;'>*</span>", unsafe_allow_html=True)
    payment = st.number_input('Montant total des paiements effectués par le client sur son compte', min_value=0.0, max_value=1000000.0, value=5000.0,step=0.01, format="%.2f")

    
    st.markdown("PAIEMENTS MINIMUM <span style='color:red;'>*</span>", unsafe_allow_html=True)
    minimum_payment = st.number_input("Montant minimum des paiements que le client doit effectuer chaque mois sur son compte", min_value=0.0, max_value=1000000.0, value=6000.0,step=0.01, format="%.2f")

   
    st.markdown("TAUX DE PAIEMENT INTÉGRAL <span style='color:red;'>*</span>", unsafe_allow_html=True)
    pct_full_payment = st.number_input("Pourcentage du solde du compte qui est payé en entier chaque mois par le client", min_value=0.0, max_value=1000000.0, value=50000.0,step=0.01, format="%.2f")

    st.markdown('ANCIENNETE <span style="color:red;">*</span>', unsafe_allow_html=True)
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
            prediction = use_api.predict_client_classification(data)
        elif oneoff_purchases == 0.0 and  purchases_freq == 0 and cash_advance_freq == 0:
            prediction = use_api.predict_client_classification_no_corr(data_no_corr)
        if prediction:

        # Affichage de la prédiction
            st.success(f"Le client est classé dans la catégorie {prediction}")

elif choice == "Importer un fichier Excel":

    # Charger le fichier CSV
    file = st.file_uploader("Sélectionner un fichier Excel(.xlsx)", type=["xlsx"])
    
    if file is not None:
        data = pd.read_excel(file)
        data_corr = data.copy()
        data_corr = data_corr[cols[0]] 
                 
        # Conversion du DataFrame en dictionnaire Python
        data_dict = data_corr.to_dict()
     
        if st.button('Prédire la catégorie de chaque client du fichier .xlsx'):            
            prediction_corr = use_api.predict_client_classification(data_dict)

            #prediction_n_c = predict_client_classification_no_corr(data_no_corr)
            df = pd.DataFrame({"Prédictions":prediction_corr})
            if prediction_corr:

            # Affichage de la prédiction
                st.write(df.head())

        # créer un bouton de téléchargement pour le DataFrame au format Excel
                file_name = "predictions.xlsx"
                file_label = "Exporter les prédictions au format .xlsx"
                data_to_download = download_files.download_excel(df)
                st.markdown(download_files.get_file_download_link(data_to_download, file_name, file_label), unsafe_allow_html=True)

elif choice == "Dashboard":
    dashboard_choice = st.sidebar.radio("Sélectionner une option", options_dashboard)
    if dashboard_choice == "Indicateurs":

        # Création des panels avec des couleurs de fond différentes
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown('<div style="background-color: #F0F8FF; padding: 10px; text-align:center;font-weight:bold">SOLDE MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.balance_mean(data)), unsafe_allow_html=True)
        col2.markdown('<div style="background-color: #FFE4E1; padding: 10px;text-align:center;font-weight:bold">FREQUENCE ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_freq_mean(data)), unsafe_allow_html=True)
        col3.markdown('<div style="background-color: #E0FFFF; padding: 10px;text-align:center;font-weight:bold">TOTAL ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_trx_sum(data)), unsafe_allow_html=True)
        col4.markdown('<div style="background-color: #F5F5DC; padding: 10px;text-align:center;font-weight:bold">PAIEMENT MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.payments_mean(data)), unsafe_allow_html=True)

    

        # Affichage de l'histogramme du solde des comptes dans le
        generate_graphics.hist_solde_compte(data)

        # Affichage du graphique du ratio d'achats ponctuels dans le dashboard
        generate_graphics.pie_ratio_achats_ponctuels(data)

        # Création du graphique en barres groupées pour le nombre de transactions par groupe de clients
        generate_graphics.barr_transaction_par_grp_client(data)

        # Tracer un nuage de points du montant total des achats par rapport à l'ADB
        generate_graphics.nuage_de_points_montant_total_des_achats(data)

    elif dashboard_choice == "Segments":
        st.subheader("Segments")

        # Création des panels avec des couleurs de fond différentes
        clusters = ["Cluster 1.0", "Cluster 2.0", "Cluster 3.0", "Cluster 4.0"]

        # Cases à cocher pour les  multiple choix
        choix_clusters = st.multiselect("Choisissez le(s) cluster(s):", clusters, default=["Cluster 1.0"])
        
        #----------------Cluster 1.0------------------------------------------------
        if len(choix_clusters) == 1:
            c1 = choix_clusters[0]
            cluster = data[data["cluster_result"] == c1]
            
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown('<div style="background-color: #F0F8FF; padding: 10px; text-align:center;font-weight:bold">SOLDE MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.balance_mean(cluster)), unsafe_allow_html=True)
            col2.markdown('<div style="background-color: #FFE4E1; padding: 10px;text-align:center;font-weight:bold">FREQUENCE ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_freq_mean(cluster)), unsafe_allow_html=True)
            col3.markdown('<div style="background-color: #E0FFFF; padding: 10px;text-align:center;font-weight:bold">TOTAL ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_trx_sum(cluster)), unsafe_allow_html=True)
            col4.markdown('<div style="background-color: #F5F5DC; padding: 10px;text-align:center;font-weight:bold">PAIEMENT MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.payments_mean(cluster)), unsafe_allow_html=True)

        if len(choix_clusters) == 2:
            c1 = choix_clusters[0]
            c2 = choix_clusters[-1]
            d1 = data[data["cluster_result"] == c1]
            d2 = data[data["cluster_result"] == c2]
            cluster = pd.concat([d1,d2])
            
        
            # calculer le montant des paiements moyens
            payments_mean = round(cluster['PAYMENTS'].mean(),2)
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown('<div style="background-color: #F0F8FF; padding: 10px; text-align:center;font-weight:bold">SOLDE MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.balance_mean(cluster)), unsafe_allow_html=True)
            col2.markdown('<div style="background-color: #FFE4E1; padding: 10px;text-align:center;font-weight:bold">FREQUENCE ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_freq_mean(cluster)), unsafe_allow_html=True)
            col3.markdown('<div style="background-color: #E0FFFF; padding: 10px;text-align:center;font-weight:bold">TOTAL ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_trx_sum(cluster)), unsafe_allow_html=True)
            col4.markdown('<div style="background-color: #F5F5DC; padding: 10px;text-align:center;font-weight:bold">PAIEMENT MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.payments_mean(cluster)), unsafe_allow_html=True)

        if len(choix_clusters) == 3:
            c1 = choix_clusters[0]
            c2 = choix_clusters[1]
            c3 = choix_clusters[-1]
            d1 = data[data["cluster_result"] == c1]
            d2 = data[data["cluster_result"] == c2]
            d3 = data[data["cluster_result"] == c3]
            cluster = pd.concat([d1,d2,d3])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown('<div style="background-color: #F0F8FF; padding: 10px; text-align:center;font-weight:bold">SOLDE MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.balance_mean(cluster)), unsafe_allow_html=True)
            col2.markdown('<div style="background-color: #FFE4E1; padding: 10px;text-align:center;font-weight:bold">FREQUENCE ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_freq_mean(cluster)), unsafe_allow_html=True)
            col3.markdown('<div style="background-color: #E0FFFF; padding: 10px;text-align:center;font-weight:bold">TOTAL ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_trx_sum(cluster)), unsafe_allow_html=True)
            col4.markdown('<div style="background-color: #F5F5DC; padding: 10px;text-align:center;font-weight:bold">PAIEMENT MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.payments_mean(cluster)), unsafe_allow_html=True)


        if len(choix_clusters) == 4:
            c1 = choix_clusters[0]
            c2 = choix_clusters[1]
            c3 = choix_clusters[2]
            c4 = choix_clusters[-1]
            d1 = data[data["cluster_result"] == c1]
            d2 = data[data["cluster_result"] == c2]
            d3 = data[data["cluster_result"] == c3]
            d4 = data[data["cluster_result"] == c4]
            cluster = pd.concat([d1,d2,d3,d4])
            
        
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown('<div style="background-color: #F0F8FF; padding: 10px; text-align:center;font-weight:bold">SOLDE MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.balance_mean(cluster)), unsafe_allow_html=True)
            col2.markdown('<div style="background-color: #FFE4E1; padding: 10px;text-align:center;font-weight:bold">FREQUENCE ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_freq_mean(cluster)), unsafe_allow_html=True)
            col3.markdown('<div style="background-color: #E0FFFF; padding: 10px;text-align:center;font-weight:bold">TOTAL ACHAT  {:.2f}</div>'.format(statistiques_et_kpi.purchases_trx_sum(cluster)), unsafe_allow_html=True)
            col4.markdown('<div style="background-color: #F5F5DC; padding: 10px;text-align:center;font-weight:bold">PAIEMENT MOYEN  {:.2f}</div>'.format(statistiques_et_kpi.payments_mean(cluster)), unsafe_allow_html=True)

        
        
        
        
        if choix_clusters:
            data = data[cols_seg]
            if len(choix_clusters) == 1:
                cluster = data[data["cluster_result"] == choix_clusters[0]]
                st.dataframe(cluster.style.highlight_max(axis=0))

                # créer un bouton de téléchargement pour le DataFrame au format Excel
                file_name = f"{choix_clusters[0]}.xlsx"
                file_label = "Exporter les données au format .xlsx"
                data_to_download = download_files.download_excel(cluster)
                st.markdown(download_files.get_file_download_link(data_to_download, file_name, file_label), unsafe_allow_html=True)

            if len(choix_clusters) == 2:
                c1 = choix_clusters[0]
                c2 = choix_clusters[-1]
                d1 = data[data["cluster_result"] == c1]
                d2 = data[data["cluster_result"] == c2]
                clusters = pd.concat([d1,d2])
                clusters = clusters.sample(frac=1, random_state=42, axis=0).reset_index(drop=True)
                st.dataframe(clusters.style.highlight_max(axis=0))
                
                # créer un bouton de téléchargement pour le DataFrame au format Excel
                file_name = f"{c1} - {c2}.xlsx"
                file_label = "Exporter les données au format .xlsx"
                data_to_download = download_files.download_excel(clusters)
                st.markdown(download_files.get_file_download_link(data_to_download, file_name, file_label), unsafe_allow_html=True)

            if len(choix_clusters) == 3:
                c1 = choix_clusters[0]
                c2 = choix_clusters[1]
                c3 = choix_clusters[-1]
                d1 = data[data["cluster_result"] == c1]
                d2 = data[data["cluster_result"] == c2]
                d3 = data[data["cluster_result"] == c3]
                clusters = pd.concat([d1,d2,d3])
                clusters = clusters.sample(frac=1, random_state=42, axis=0).reset_index(drop=True)
                st.dataframe(clusters.style.highlight_max(axis=0))

                 # créer un bouton de téléchargement pour le DataFrame au format Excel
                file_name = f"{c1} - {c2} - {c3}.xlsx"
                file_label = "Exporter les données au format .xlsx"
                data_to_download = download_files.download_excel(clusters)
                st.markdown(download_files.get_file_download_link(data_to_download, file_name, file_label), unsafe_allow_html=True)

            if len(choix_clusters) == 4:
                c1 = choix_clusters[0]
                c2 = choix_clusters[1]
                c3 = choix_clusters[2]
                c4 = choix_clusters[-1]
                d1 = data[data["cluster_result"] == c1]
                d2 = data[data["cluster_result"] == c2]
                d3 = data[data["cluster_result"] == c3]
                d4 = data[data["cluster_result"] == c4]
                clusters = pd.concat([d1,d2,d3,d4])
                clusters = clusters.sample(frac=1, random_state=42, axis=0).reset_index(drop=True)
                st.dataframe(clusters.style.highlight_max(axis=0))

                # créer un bouton de téléchargement pour le DataFrame au format Excel
                file_name = f"{c1} - {c2} - {c3} - {c4}.xlsx"
                file_label = "Exporter les données au format .xlsx"
                data_to_download = download_files.download_excel(clusters)
                st.markdown(download_files.get_file_download_link(data_to_download, file_name, file_label), unsafe_allow_html=True)
    
    elif dashboard_choice == "Marketing":
        st.write("Affichage des données marketing ici...")  
    




               

