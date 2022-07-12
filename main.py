import numpy as np
import json
import itertools
import logging

#Import project files
import Gear
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
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#Disable all logging
#logging.disable(logging.CRITICAL)
#-----------Logger setup finished------------#


def main():
	#text = Interface.UpdateInterface()
	Gear.main()
	print('start')
	logger.error('test')


def BISON(config):
	print('Bison main')



if __name__ == '__main__':
	main()