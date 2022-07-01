#This is the UI that connects user input to the main application

import streamlit as st
from PIL import Image


st.set_page_config(page_title = "BISON2",
					page_icon = ":bar_chart:",
					layout = "wide")

Bisonlogo = Image.open('Media/Bison2.png')
st.image(Bisonlogo, caption='Version 2.0')

#Sidebar
st.sidebar.header("Select stuff here")

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibiliry: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html = True)