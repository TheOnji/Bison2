_Debug = False

import streamlit as st
from PIL import Image
import time
import logging
import numpy as np

import main
from Interface_options import *
import GearX
import FoodX

#---------------Logger setup----------------#
logger = logging.getLogger(__name__)
logger.propagate = False

if not logger.hasHandlers():

    if _Debug == True:
        loglevel = logging.DEBUG 
    else:
        loglevel = logging.ERROR

    logger.setLevel(loglevel)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(f"Bison2.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.ERROR)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(loglevel)
    logger.addHandler(stream_handler)

#Disable all logging
#logging.disable(logging.CRITICAL)
#-----------Logger setup finished------------#

def UpdateInterface():
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

        _Update = st.button('Update database')

        st.text('Created by: Onji')

    #---Page setup---
    st.text(logo)
    st.text('---Advanced FFXIV best-in-slot optimizer---')
    st.info('How to use: \n 1. Configure race and job in the sidepanel. \n 2. Configure which gear and materia to analyze. \n 3. Select GCD range of interest. \n 4. Launch BiSON with the Optimize button. \n Less gear and materia options gives faster processing time.')

    #Load Gear object for selected job
    Gear_Set = GearX.Gearset(Job)
    Gear_Choice = {}

    with st.container():
        c1, c2 = st.columns(2)

        with c1:
            st.subheader('Mainhand')
            Gear_Choice.update({'Weapon':[], 
                                'Shield':[],
                                'Head':[],
                                'Body':[],
                                'Hands':[],
                                'Legs':[],
                                'Feet':[],
                                'Earrings':[],
                                'Necklace':[],
                                'Bracelets':[],
                                'Ring1':[],
                                'Ring2':[]})

            for key, val in Gear_Set.JobGear.items():
                for subkey, subval in val.items():
                    if 'Weapon' in key:
                        g1 = st.checkbox(subval['Name'])

                        #If gear is ticked update config file for BISON
                        if g1:
                            Gear_Choice[key] += [subkey]

        with c2:
            st.subheader('Offhand')
            for key, val in Gear_Set.JobGear.items():
                for subkey, subval in val.items():
                    if 'Shield' in key:
                        g1 = st.checkbox(subval['Name'])

                        #If gear is ticked update config file for BISON
                        if g1:
                            Gear_Choice[key] += [subkey]

    with st.container():
        c1, c2 = st.columns(2)
        
        with c1:
            st.header('Body')
            k1 = st.container()
            k2 = st.container()
            k3 = st.container()
            k4 = st.container()
            k5 = st.container()
            section = {'Head':k1, 'Body':k2, 'Hands':k3, 'Legs':k4, 'Feet':k5}

            for key, val in section.items():
                with val:
                    st.subheader(key)

            for key, val in Gear_Set.JobGear.items():
                for subkey, subval in val.items():
                    if key in section:
                        with section[key]:
                            g1 = st.checkbox(subval['Name'])
                            #If gear is ticked update config file for BISON
                            if g1:
                                Gear_Choice[key] += [subkey]

        with c2:
            st.header('Accessories')
            k1 = st.container()
            k2 = st.container()
            k3 = st.container()
            k4 = st.container()
            k5 = st.container()
            section = {'Earrings':k1, 'Necklace':k2, 'Bracelets':k3, 'Ring1':k4, 'Ring2':k5}

            for key, val in section.items():
                with val:
                    st.subheader(key)

            for key, val in Gear_Set.JobGear.items():
                for subkey, subval in val.items():

                    if key in section:
                        with section[key]:
                            g1 = st.checkbox(subval['Name'])
                            
                            #If gear is ticked update config file for BISON
                            if g1:
                                Gear_Choice[key] += [subkey]

                    if key == 'Ring':
                        for temp_key, addstr in zip(['Ring1', 'Ring2'], ['', ' ']):
                            with section[temp_key]:
                                g1 = st.checkbox(subval['Name'] + addstr)
                                
                                #If gear is ticked update config file for BISON
                                if g1:
                                    Gear_Choice[temp_key] += [subkey]

            for key, val in Gear_Choice.items():
                if len(val) < 1:
                    Gear_Choice[key] = [0]

    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        st.header('Materia')
        CRT = st.checkbox('Critical Hit')
        DET = st.checkbox('Determination')
        DH = st.checkbox('Direct hit')
        SKS = st.checkbox('Skill speed')
        SPS = st.checkbox('Spell speed')
        TEN = st.checkbox('Tenacity')
        PIE = st.checkbox('Piety')


    Menu = FoodX.Menu()
    Food_Choice = {}

    with c2:
        st.header('Food')
        for ID, Name in Menu.options().items():
            tick = st.checkbox(Name)
            Food_Choice.update({ID:tick})

    with c3:
        st.header('GCD range')
        m = st.checkbox('Select specific GCDs')

        if m:
            GCD_val = st.text_input('Type in GCDs separate by ";":')
            if GCD_val == '':
                GCD_val = [0]
            else:
                split = GCD_val.split(';')
                GCD_val = [float(s) for s in split]
            GCD_range = GCD_val
            st.write(GCD_range)
        else:
            GCD_min, GCD_max = (1.50, 2.50)
            GCD_min = st.number_input('From', 1.50, 2.50, value = 2.40)
            GCD_max = st.number_input('To', 1.50, 2.50, value = 2.50)
            GCD_range = list(range(int(GCD_min*100), int(GCD_max*100+1)))
            GCD_range = [e/100 for e in GCD_range]

    _Optimize = st.button('Optimize!')

    #Apply css style
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)
        
    #Create loading area container
    Load_area = st.container()

    #Collect data for BISON in dictionary
    BISON_config = {'Race':[Race_type, Race],
                    'Job':[Job_type, Job],
                    'Materia':{'CRT':CRT,'DET':DET,'DH': DH, 'SKS':SKS,'SPS':SPS,'TEN': TEN,'PIE':PIE},
                    'GCDs':GCD_range,
                    'Gear':Gear_Choice,
                    'Food':Food_Choice}

    flags = {'Update': _Update,
            'Optimize':_Optimize}


    return BISON_config, flags, Load_area
