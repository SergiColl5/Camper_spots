import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs

st.set_page_config(
     page_title="Campiquipugui",
     page_icon="🚐",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )
st.markdown("<h1 style='text-align: center;'>CAMPI QUI PUGUI!</h1>", unsafe_allow_html=True)

cover = Image.open("images/cover_camper.jpeg")
st.image(cover, use_column_width=True)
st.write('---')
st.markdown('''<h3 style='text-align: center;'>Camper lover!\n
Planning lover... not so much.\n
Don't worry, this website helps you find the best locations to visit around Spain.
But most importantly...</h3>''', unsafe_allow_html=True)

st.markdown('''<h2 style='text-align: center;'>Cool places to spend the night!</h2>''', unsafe_allow_html=True)
