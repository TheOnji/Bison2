_Debug = False

import streamlit as st
import json


#Page setting
st.set_page_config(page_title = "BISON 2.0",
					page_icon = ":ox:",
					layout = "wide")

#---Page setup---
st.info("This is the rotation page")
st.write("You selected: ")
st.write(st.session_state["Check_selection"])

st.write(st.session_state["num"])


#Configuration sidebar
with st.sidebar:
    st.header('Navigation')

    

#Apply css style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

