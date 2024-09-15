import streamlit as st

st.set_page_config(
    page_title="Accueil",
    page_icon="👋",
)
st.title("Piscines :blue[Hockey Sub] :sunglasses:"  )
st.write("# 👋 Bienvenue !")

st.sidebar.success("☝️ Selectionner une des fonctinonalités de l'application.")


st.markdown(
    """
    👈 Sélectionner dans le menu à gauche l'une des deux fonctionnalités pour rechercher des bassins sportifs de natation.


    ## :blue[La carte]
    La carte affiche la liste des bassins sportifs de natation en France.
    Des filtres sont disponibles pour cibler les recherches(longueur, largeur, profondeur, etc...)
    ## :blue[Le tableau]
    Le tableau par région affiche la liste des piscines de la région sélectionnée.
    Un certain nombre de caractéristiques sont disponibles.
"""
)