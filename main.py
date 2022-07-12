import numpy as np
import json
import itertools
import logging

#Import project files
import Gear

#---------------Logger setup----------------#
logger = logging.getLogger(__name__)

#Levels
#NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(f"{__name__}.log")
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#Disable all logging
#logging.disable(logging.CRITICAL)
#-----------Logger setup finished------------#


def main():
	config = {}
	BISON(config)
	Gear_db.main()


def BISON(config):
	print('Bison main')



if __name__ == '__main__':
	main()