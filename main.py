'''
BISON 2
External dependencies:  FFXIV lodestone database - data, formatting
                        Names of raid gear eg 'Asphodelos' 


'''
_Debug = True

#Import modules
import numpy as np
import json
import itertools
import logging
import streamlit as st
from time import time, strftime, gmtime

#Import project files
import GearX
import MateriaX
import FoodX
import get_data
import Interface
import Allagan_functions

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

#---------------------------------Main Function-------------------------------#

def main():
    
    BISON_config, flags, Load_area = Interface.UpdateInterface()

    if flags['Update'] == True:
        get_data.UpdateData(600, 580, Load_area)

    if flags['Optimize'] == True:
        BIS_IDs = BISON(BISON_config, Load_area)

#-----------------------------------------------------------------------------#

#---Decorators---#
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        logger.debug(f"-> {func.__name__}")
        res = func(*args, **kwargs)
        logger.debug(f"<- {func.__name__}")
        end_time = time()
        elapsed = strftime("%H:%M:%S",gmtime(end_time - start_time))
        print(func.__name__, elapsed)
        return res, elapsed
    return wrapper
#----------------#

@timer
def BISON(config, Load_area):
    _init = True

    #Create callable equipent objects
    Gear = GearX.Gearset(config['Job'][1])
    Food = FoodX.Menu()
    Materia = MateriaX.Materia()

    #Gear IDs to check
    Gear_list = list(config['Gear'].values())
    Gear_IDs = itertools.product(*Gear_list)

    #Food IDs to check
    Food_list = list(config['Food'].values())
    Food_IDs = [ID for ID, tick in enumerate(Food_list) if tick]

    #BIS_IDs for storing results
    BIS_IDs = {}

    #Display progress in loading area
    with Load_area:
        info = st.empty()
        Bison_loader = st.progress(0)
        static = st.empty()
        cbutton = st.empty()
        counter = 0

        for Gear_ID in Gear_IDs:
            counter += 1

            Gear(Gear_ID)

            #Materia IDs to check
            Materia_Allowance = [int(limit * tick) for limit, tick in zip(np.diagonal(Gear.Materia_Matrix), config['Materia'].values())]
            Materia_list = [list(range(int(limit) + 1)) for limit in Materia_Allowance]
            Materia_IDs = itertools.product(*Materia_list)

            if _init:
                Gearsets_ref = len(list(itertools.product(*Gear_list)))
                Materia_ref = len(list(itertools.product(*Materia_list)))
                Food_ref = len(Food_IDs)

                Total_iter = Gearsets_ref*Materia_ref*Food_ref
                logger.info(f"\n Gearsets: {Gearsets_ref} \n Materia sets per gearset:{Materia_ref} \n Food types: {Food_ref} \n")
                logger.info(f"Total iterations: {Total_iter:,d} \n")
                
                static.info(f"Total iterations: {Total_iter:,d} -> Gearsets: {Gearsets_ref} | Materia sets / Gearset: {Materia_ref} | Food types / Materia set: {Food_ref}")

                interval = max(round(Gearsets_ref/10, -2), 10)
                cancel = cbutton.button('Cancel')
                if cancel:
                    break
                _init = False

            elif counter%interval == 0:
                Bison_loader.progress(int(100*counter/Gearsets_ref))
                info.subheader(f"Working... - Gearsets checked: {counter} / {Gearsets_ref}")

            for Materia_ID in Materia_IDs:
                if Gear.Test_Materia(Materia_ID) == False:
                    continue

                Materia(Materia_ID)

                for Food_ID in Food_IDs:
                    Food(Food_ID)

                    GCD = Allagan_functions.Speedtest(0, 
                                                    getattr(Gear, 'Skill Speed'),
                                                    getattr(Materia, 'Skill Speed'),
                                                    getattr(Food, 'Skill Speed'),
                                                    getattr(Food, 'percentage'))
                    if GCD in config['GCDs']:
                        BIS_IDs.update({GCD:{'Gear_ID':Gear_ID,
                                                'Materia_ID':Materia_ID,
                                                'Food_ID':Food_ID}})

                        #Allagan_functions.Equipper(None, Gear, Materia, Food)

        #Write finishing text to interface
        Bison_loader.progress(100)
        info.subheader(f"Finished: {Gearsets_ref} / {Gearsets_ref}")


    return BIS_IDs


if __name__ == '__main__':
    main()