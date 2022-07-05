import streamlit as st
from PIL import Image
import time

from Interface_options import *

#Page setting
st.set_page_config(page_title = "BISON 2.0",
					page_icon = ":ox:",
					layout = "wide")

#Configuration sidebar
with st.sidebar:
    st.header('Configuration')

    #Race selection
    Race_type = st.selectbox('Select race', Race_types)
    Race = st.selectbox('Select race subtype', Race_subtypes[Race_type])

    #Job selection
    Job_group = st.selectbox('Select job type', ['Tank','Healer','DPS'])
    Job = st.selectbox('Select job', Job_options[Job_group])

    st.text('Created by: Onji')

#Page setup
        
logo = ''                          
logo += "██████╗░██╗░██████╗░█████╗░███╗░░██╗    ((_,...,_))    \n"
logo += "██╔══██╗██║██╔════╝██╔══██╗████╗░██║       |o o|       \n"
logo += "██████╦╝██║╚█████╗░██║░░██║██╔██╗██║       \\   /      \n"
logo += "██╔══██╗██║░╚═══██╗██║░░██║██║╚████║        ^_^        \n"
logo += "██████╦╝██║██████╔╝╚█████╔╝██║░╚███║  V2.0"
st.text(logo)

st.text('---Advanced FFXIV best-in-slot optimizer---')

st.info('How to use: \n 1. Configure race and job in the sidepanel. \n 2. Configure which gear and materia to analyze. \n 3. Select GCD range of interest. \n 4. Launch BiSON with the Optimize button.')

with st.container():
    st.header('Gear pieces to test')
    c1, c2 = st.columns(2)
    Gear_type = Job_Gear[Job]
    Gear_options = All_gear_options[Gear_type]
    with c1:
        st.header('Body')

        for key in ['Head', 'Chest', 'Hands', 'Legs', 'Feet']:
            st.subheader(key)
            st.checkbox(Gear_options[key][0])
            st.checkbox(Gear_options[key][1])
    
    with c2:
        st.header('Accessories')

        for key in ['Ear', 'Neck', 'Braclet', 'Ring1', 'Ring2']:
            st.subheader(key)
            st.checkbox(Gear_options[key][0])
            st.checkbox(Gear_options[key][1])

c1, c2 = st.columns([1, 1])

with c1:
    st.header('Materia')
    st.checkbox('Critical Hit')
    st.checkbox('Direct hit')
    st.checkbox('Determination')
    st.checkbox('Skill speed')
    st.checkbox('Spell speed')
    st.checkbox('Tenacity')
    st.checkbox('Piety')

with c2:
    st.header('GCD range')
    st.number_input('From', 1.50, 2.50, value = 2.40)
    st.number_input('To', 1.50, 2.50, value = 2.50)

st.button('Optimize!')

#Apply css style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)