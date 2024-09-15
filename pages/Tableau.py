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

piscines["Code Postal"] = piscines["Code Postal"].astype(int).astype(str)

filtered_data = piscines.copy()

# Filtre par région
region = piscines["Région Nom"].drop_duplicates().sort_values()
#filter_region = st.sidebar.multiselect("Sélectionner la région", region, default=region)
filter_region = st.sidebar.selectbox("Sélectionner la région", region,)
filtered_data = piscines[ ( piscines["Région Nom"]==filter_region ) ]

st.dataframe(data=filtered_data, #use_container_width=True
             width=1000,
             height=700,

             hide_index=True, 
             column_order=["Région Nom"
                           ,"Département Nom"
                           ,"Commune Nom"
                           ,"Code Postal"
                           ,"Numéro de l'installation sportive"
                           ,"Nom de l'installation sportive"
                           ,"Nom de l'équipement sportif"
                           ,"Adresse internet de l'équipement"
                           ,"Type de propriétaire"
                           ,"Type de gestionnaire"

                           ,"Longueur du bassin"	
                           ,"Largeur du bassin"	
                           ,"Profondeur minimale du bassin"	
                           ,"Profondeur maximale du bassin"	
                           ,"Nature du sol"
                           ,"Nombre de places assises en tribune"
                           ,"Types de locaux complémentaires"
                           ,"Accessibilité de l'installation en transport en commun des différents mode"
                           ,"Ouverture exclusivement saisonnière"
 ],
             )



