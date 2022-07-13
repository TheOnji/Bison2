import logging
import json

#---------------Logger setup----------------#
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(f"Bison2.log")
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
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
    Menu = FoodMenu(1)
    Menu


class FoodMenu():
    def __init__(self, Food_ID = 1):
        with open('Food_database.json') as file:
            self.database = json.load(file)

        self.null = {'Critical Hit': 0,
                    'Determination': 0,
                    'Direct Hit Rate': 0,
                    'Skill Speed': 0,
                    'Spell Speed': 0,
                    'Tenacity': 0,
                    'Piety': 0,
                    'Vitality': 0}

        self.choices = {}

        for i, (key, val) in enumerate(self.database.items()):
            val.pop('Type')
            val.pop('iLVL')
            val.update({'Name':key})
            entry = {'Name':key}
            entry.update(val)
            self.choices.update({i:entry})

        self.__call__(Food_ID)

    def __call__(self, Food_ID):
        self.reset()
        self.__dict__.update(self.choices[Food_ID])

    def __repr__(self):
        for key, val in self.__dict__.items():
            if key == 'database' or key == 'choices' or key == 'null':
                continue
            print(f"{key}: {val}")
        return ''

    def reset(self):
        self.__dict__.update(self.null)

    def show(self):
        for key, val in self.choices.items():
            print(f"{key}: {val['Name']}")

if __name__ == '__main__':
    main()