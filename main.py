'''
BISON 2
External dependencies:  FFXIV lodestone database - data, formatting
                        Names of raid gear eg 'Asphodelos' 


'''
_Debug = False

import numpy as np
import json
import itertools
import logging
import streamlit as st
import time

#Import project files
import Gear
import Food
import get_Geardata as getdb
import Interface

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

def main():
    BISON_config, flags, Load_area = Interface.UpdateInterface()

    if flags['Update'] == True:
        getdb.UpdateData(600, 580, Load_area)

    if flags['Optimize'] == True:
        BISON(BISON_config, Load_area)


def BISON(config, Load_area):
    print(config)
    logger.debug('-> Bison function called')
    GearSet = Gear.Gearset(config['Job'][1])
    Menu = Food.FoodMenu()

    Gear_list = list(config['Gear'].values())
    Gear_IDs = itertools.product(*Gear_list)

    Food_list = list(config['Food'].values())
    Food_IDs = [ID for ID, tick in enumerate(Food_list) if tick]

    for Gear_ID in Gear_IDs:
        GearSet(Gear_ID)

        Materia_Allowance = [int(limit * tick) for limit, tick in zip(np.diagonal(GearSet.Materia_Matrix), config['Materia'].values())]
        Materia_list = [list(range(int(limit) + 1)) for limit in Materia_Allowance]
        Materia_IDs = itertools.product(*Materia_list)

        k = [0, 0]
        for Materia_ID in Materia_IDs:
            k[0] += 1
            if GearSet.Test_Materia(Materia_ID) == False:
                continue
            k[1] += 1

            for Food_ID in Food_IDs:
                Menu(Food_ID)

        logger.debug(f"{k[1]} allowed sets of Materia ({k[0]} tested...)")
                


#---------------------------------#

def BISON_DEMO(config, Load_area):
    print('Bison main')

    i = (i for i in np.linspace(0, 100, len(config)))
    st.markdown("""---""") 
    st.text('Optimizing (DEMO)...')
    testbar = st.progress(0)

    for key, val in config.items():
        print(key)
        print(val)

        with Load_area:
            testbar.progress(int(next(i)))
            time.sleep(0.5)


if __name__ == '__main__':
    main()