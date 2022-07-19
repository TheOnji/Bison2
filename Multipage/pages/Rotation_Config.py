_Debug = False

import streamlit as st
import json

from Interface_options import *




#Page setting
st.set_page_config(page_title = "BISON 2.0",
					page_icon = ":ox:",
					layout = "wide")

	#---Page setup---
st.text(logo)
st.text('---Advanced FFXIV best-in-slot optimizer---')

#Configuration sidebar
with st.sidebar:
    st.header('Navigation')

    

#Apply css style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

