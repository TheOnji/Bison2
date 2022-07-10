import numpy as np
import json



def Main():
    database = load_json()
    return database

def load_json():
    with open('database.json') as file:
        database = json.load(file)
    return database

def get_JobGear(Job, database):
    JobGear = {}
    for key, val in database.items():
        if Job in val['Jobs']:
            JobGear.update({key:val})
    return JobGear

class Gear_base():
    def __init__(self):
        self.Strength = 0
        self.Dexterity = 0
        self.Vitality = 0
        self.Intelligence = 0
        self.Mind = 0
        self.CriticalHit = 0
        self.Determination = 0
        self.DirectHitRate = 0
        self.Defense = 0
        self.MagicDefense = 0
        self.AttackPower = 0
        self.SkillSpeed = 0

    def __add__(self, other):
        rv1 = self.__dict__.copy()
        for key in other.__dict__.keys():
            rv1.update({key:self.__dict__.get(key, 0) + other.__dict__.get(key, 0)})
        return rv

class Gearset_base():
    def __init__(self):
        self.Materia_Matrix = np.zeros([7, 7])
        self.ID = None
        self.slots = {'Weapon':None,
                    'Head':None,
                    'Chest':None,
                    'Hands':None,
                    'Legs':None,
                    'Feet':None,
                    'Ear':None,
                    'Neck':None,
                    'Braclet':None,
                    'Ring1':None,
                    'Ring2':None}
        self.options = self.slots.copy()

    def __call__(self, Gear_ID):
        assert len(Gear_ID) == 11, 'Gear ID must be a list of length 11'
        self.ID = Gear_ID

        for key, ID in zip(self.slots.keys(), Gear_ID):
            self.slots.update({key:self.options[key][ID].name})


class Fending_gear(Gearset_base):
    pass

class Healing_gear(Gearset_base):
    pass

class Striking_gear(Gearset_base):
    pass

class Maiming_gear(Gearset_base):
    pass

class Aiming_gear(Gearset_base):
    pass

class Casting_gear(Gearset_base):
    pass




if __name__ == "__main__":
    Main()
