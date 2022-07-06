import streamlit as st
from PIL import Image
import time

import main
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
    Job_type = st.selectbox('Select job type', ['Tank','Healer','DPS'])
    Job = st.selectbox('Select job', Job_options[Job_type])

    st.text('Created by: Onji')

#---Page setup---
st.text(logo)
st.text('---Advanced FFXIV best-in-slot optimizer---')
st.info('How to use: \n 1. Configure race and job in the sidepanel. \n 2. Configure which gear and materia to analyze. \n 3. Select GCD range of interest. \n 4. Launch BiSON with the Optimize button. \n Less gear and materia options gives faster processing time.')

with st.container():
    st.header('Gear pieces to test')
    c1, c2 = st.columns(2)
    Gear_type = Job_Gear[Job]
    Gear_options = All_gear_options[Gear_type]
    Gear = {}
    with c1:
        st.header('Body')

        for key in ['Head', 'Chest', 'Hands', 'Legs', 'Feet']:
            st.subheader(key)
            g1 = st.checkbox(Gear_options[key][0])
            g2 = st.checkbox(Gear_options[key][1])
            Gear.update({key:[g1, g2]})

    with c2:
        st.header('Accessories')

        for key in ['Ear', 'Neck', 'Braclet', 'Ring1', 'Ring2']:
            st.subheader(key)
            g1 = st.checkbox(Gear_options[key][0])
            g2 = st.checkbox(Gear_options[key][1])
            Gear.update({key:[g1, g2]})

c1, c2 = st.columns([1, 1])

with c1:
    st.header('Materia')
    CRT = st.checkbox('Critical Hit')
    DET = st.checkbox('Determination')
    DH = st.checkbox('Direct hit')
    SKS = st.checkbox('Skill speed')
    SPS = st.checkbox('Spell speed')
    TEN = st.checkbox('Tenacity')
    PIE = st.checkbox('Piety')

with c2:
    st.header('GCD range')
    GCD_min, GCD_max = (1.50, 2.50)
    GCD_min = st.number_input('From', 1.50, 2.50, value = 2.40)
    GCD_max = st.number_input('To', 1.50, 2.50, value = 2.50)

Optimize_pressed = st.button('Optimize!')

#Apply css style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


if Optimize_pressed:
    st.markdown("""---""") 
    st.text(logo2)
    st.text('Processing...')
    testbar = st.progress(0)
    for i in range(101):
        testbar.progress(i)
        time.sleep(0.01)

    #Collect data for BISON in dictionary
    BISON_config = {'Race':[Race_type, Race],
                    'Job':[Job_type, Job],
                    'Materia':{'CRT':CRT,'DET':DET,'DH': DH, 'SKS':SKS,'SPS':SPS,'TEN': TEN,'PIE':PIE},
                    'GCD':{'GCD_min':GCD_min, 'GCD_max':GCD_max},
                    'Gear':Gear}

    main.BISON(BISON_config)