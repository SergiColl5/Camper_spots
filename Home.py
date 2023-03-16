import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs

st.set_page_config(
     page_title="Campiquipugui",
     page_icon="🚐",
     layout="wide",
     initial_sidebar_state="expanded",
     
 )
st.markdown("<h1 style='text-align: center;'>CAMPI QUI PUGUI!</h1>", unsafe_allow_html=True)

cover = Image.open("images/cover_camper.jpeg")
st.image(cover, use_column_width=True)
st.write('---')
st.markdown('''<h2 style='text-align: center;'>We are Camper lovers!</h2>''', unsafe_allow_html=True)



st.markdown('''<h3 style='text-align: center;'>I love hitting the open road and going on a good old road trip. <br>
But let's be real, planning it can be such a drag. Figuring out where to go, where to park my camper, ugh! <br>
That's why I've decided to create the ultimate route finder. With just a few basic filters, 
I can easily find the perfect spot to crash for the night without any hassle."


 </h3>''', unsafe_allow_html=True)

st.write('---')

st.markdown('''<h4 style='text-align: center;'>⬇️ Here is how I did it ⬇️
 </h4>''', unsafe_allow_html=True)


st.markdown('''<h4 style='text-align: center;'>⬇️ Here is how I did it ⬇️
 </h4>''', unsafe_allow_html=True)