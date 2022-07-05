#This is the UI that connects user input to the main application

import streamlit as st
from PIL import Image
import time

#Page setting
st.set_page_config(page_title = "BISON 2.0",
					page_icon = ":ox:",
					layout = "wide")

#Configuration sidebar
with st.sidebar:
    st.header('Configuration')
    #Race selection
    Race_group = st.selectbox('Select race', ['Hyur','Elezen','Lalafell', 'Miqo\'te', 
                                'Roegadyn', 'Au Ra', 'Hrothgar', 'Viera'])
    Race_options = {'Hyur':['Midlander', 'Highlander'], 
                    'Elezen':['Wildwood', 'Duskwight'], 
                    'Lalafell':['Plainsfolk', 'Dunesfolk'],
                    'Miqo\'te':['Seekers of the sun', 'Keepers of the moon'],
                    'Roegadyn':['Sea wolves', 'Hellsguard'], 
                    'Au Ra':['Raen', 'Xaela'],
                    'Hrothgar':['Helions', 'The lost'],
                    'Viera':['Rava', 'Veena']}
    Race = st.selectbox('Select race subtype', Race_options[Race_group])

    #Job selection
    Job_group = st.selectbox('Select job type', ['Tank','Healer','DPS'])
    Job_options = {'Tank':['PLD', 'DRK', 'WAR', 'GNB'], 
                 'Healer':['WHM', 'AST', 'SCH', 'SGE'], 
                    'DPS':['SAM','RPR','MNK','DRG','DNC','MCH','BRD','BLM','RDM','SMN']}
    Job = st.selectbox('Select job', Job_options[Job_group])

pressed = st.button('Press to load...')
if pressed:
    pressed = False

    with st.progress(0):
        for i in range(1,11):
            time.sleep(1)
            st.progress(i*10)


#Apply css style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)