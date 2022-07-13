'''
BISON 2
External dependencies:  FFXIV lodestone database - data, formatting
                        Names of raid gear eg 'Asphodelos' 


'''
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

file_handler = logging.FileHandler(f"Bison2.log")
stream_handler = logging.StreamHandler()

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

#Levels
#NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.setLevel(logging.DEBUG)
file_handler.setLevel(logging.ERROR)
stream_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
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