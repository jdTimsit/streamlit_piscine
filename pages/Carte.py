import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium, folium_static


import pandas as pd
pd.options.display.max_columns = 500
pd.options.display.max_rows = 500

piscines = pd.read_csv("./bassins sportifs de natation.csv", sep=";", low_memory=False)

##############################################
# Filtres non paramétables
##############################################

# Zoom sur les piscines dont les latitudes et longitudes sont renseignées
piscines = piscines[ ~( piscines["Longitude (WGS84)"].isna() & piscines["Latitude (WGS84)"].isna() )
                    & ( piscines["Longueur du bassin"]>= 25 )
]

#zoom sur les longueur classiques
piscines["Code Postal"] = piscines["Code Postal"].astype(int)


##############################################
# Filtres paramétables
##############################################

# Paramètres
longueur = piscines["Longueur du bassin"].drop_duplicates().sort_values()
largeur = piscines["Largeur du bassin"].drop_duplicates().sort_values()
sol = piscines["Nature du sol"].drop_duplicates().sort_values()
max_tribune = int(piscines["Nombre de places assises en tribune"].max())
nature_equipement = piscines["Nature de l'équipement sportif"].drop_duplicates().sort_values()
proprietaire = piscines["Type de propriétaire"].drop_duplicates().sort_values()
gestionaire = piscines["Type de gestionnaire"].drop_duplicates().sort_values()
#locaux_en_plus = piscines["Types de locaux complémentaires"].drop_duplicates().sort_values()

# Configuration de la page
st.set_page_config(layout="wide")

# Titre de la page
st.title("Piscines :blue[Hockey Sub] :sunglasses:"  )

# Titre des filtres paramétables
st.sidebar.title("Critères de sélection")

# Création des filtres
filter_longueur = st.sidebar.multiselect("Sélectionner la longueur du bassin", longueur, default=longueur)
filter_largeur = st.sidebar.slider("Selectionner la largeur du bassin", largeur.min(), largeur.max(), (10.0, 20.0))
filter_sol = st.sidebar.multiselect("Selectionner la nature du sol", sol.to_list(),default="Carrelage")
profondeur = st.sidebar.slider("Selectionner les profondeurs min et max du bassin", 0.0, 10.0, (2.0, 4.0))
filter_tribune = st.sidebar.slider("Selectionner un minimum de places en tribunes", min_value=0, max_value=max_tribune , step=10)
filter_nature_equipement = st.sidebar.multiselect("Selectionner la nature de l'équipement", nature_equipement.to_list(),default=nature_equipement)
filter_proprietaire = st.sidebar.multiselect("Selectionner le type de propriétaire", proprietaire.to_list(),default=proprietaire)
filter_gestionaire = st.sidebar.multiselect("Selectionner le type de gestionnaire", gestionaire.to_list(),default=gestionaire)
#fileter_locaux_en_plus = st.sidebar.multiselect("Selectionner le confort", locaux_en_plus.to_list(),default=locaux_en_plus)

# Filtre du dataset
filtered_data = piscines.copy()

filtered_data = filtered_data[
    ( filtered_data["Longueur du bassin"].isin(filter_longueur) )
    & ( filtered_data["Largeur du bassin"] >= filter_largeur[0]) & (filtered_data["Largeur du bassin"] <= filter_largeur[1])
    & ( filtered_data["Nature du sol"].isin(filter_sol) )
    & ( filtered_data["Profondeur minimale du bassin"] >= profondeur[0]) & (filtered_data["Profondeur maximale du bassin"] <= profondeur[1]) 
    & ( filtered_data["Nombre de places assises en tribune"] >= filter_tribune )
    & ( filtered_data["Nature de l'équipement sportif"].isin(filter_nature_equipement) )
    & ( filtered_data["Type de propriétaire"].isin(filter_proprietaire) )
    & ( filtered_data["Type de gestionnaire"].isin(filter_gestionaire) )
]



# Génération de la map
# Centrer la map sur la France
m = folium.Map(
      location = [43.7640, 7.8357]
      ,zoom_start=6
      ,tiles='cartodbpositron'
      ,width=1500
      ,height=1500
   )
# Ajout de popup sur la carte
for i in range(0,len(filtered_data)):

   df = filtered_data.iloc[i][[
      "Nom de l'installation sportive"
      ,"Code Postal"
      ,"Commune Nom"
      ,"Nombre de places assises en tribune"
      ,"Profondeur minimale du bassin"	
      ,"Profondeur maximale du bassin"
      ,"Accessibilité de l'installation en transport en commun des différents mode"
      ,"Ouverture exclusivement saisonnière"
      ,"Type de gestionnaire"]].to_frame()


   df = df.rename({
      "Nom de l'installation sportive" :"Nom:"
      ,"Code Postal":"Code Postal"
      ,"Commune Nom":"Ville"
      ,"Nombre de places assises en tribune":"Place en tribunes: "
      ,"Profondeur minimale du bassin": "Profondeur max: "
      ,"Profondeur maximale du bassin": "Profondeur min: "
      ,"Accessibilité de l'installation en transport en commun des différents mode":"transports en commun"
      ,"Ouverture exclusivement saisonnière": "ouverture exclu saisonnière"
      ,"Type de gestionnaire":"Type de gestionnaire"
      })

   html = df.to_html(
      classes="table table-striped table-hover table-condensed table-responsive"
   )   
   
   iframe = folium.IFrame(str(html))
   popup = folium.Popup(iframe,
                     min_width=500,
                     max_width=500
                     ) 


   folium.Marker(
      location=[filtered_data.iloc[i]["Latitude (WGS84)"], filtered_data.iloc[i]["Longitude (WGS84)"]],
      popup=popup,
      icon=folium.Icon(color='blue',icon_color='white',icon='info-sign')
   ).add_to(m)
st_data = folium_static(m, width=1000, height=1000)
