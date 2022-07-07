import numpy as np

def Main():
    ID = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    Geartest = Fending_gear()
    Geartest(ID)
    print(Geartest.ID)

class Gear_base():
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

    def __call__(self, Gear_ID):
        assert len(Gear_ID) == 12, 'Gear ID must be a list with length 12'
        self.ID = Gear_ID

class Fending_gear(Gear_base):
    def __init__(self):
        super().__init__()


class Healing_gear(Gear_base):
    pass

class Striking_gear(Gear_base):
    pass

class Maiming_gear(Gear_base):
    pass

class Aiming_gear(Gear_base):
    pass

class Casting_gear(Gear_base):
    pass


























































class Gearslot():
    def __init__(self):
        self.Weapon = None
        self.Head = None
        self.Chest = None
        self.Hands = None
        self.Legs = None
        self.Feet = None
        self.Ear = None
        self.Neck = None
        self.Bracelet = None
        self.Ring1 = None
        self.Ring2 = None

    def show(self):
        for k in self.__dict__:
            exec(f"print(self.{k})")

class Gearset_Fending():

    def __init__(self, Job, Weapon, Head, Chest, Hands, Legs, Feet, Ear, Neck, Bracelet, Ring1, Ring2):
        self.Gearslot = Gearslot()

        self.TotalMelds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.AllowedMelds = [{'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0}]

        self.Affinity = [{'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0},
                            {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0}]


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
        self.AttackMagicPotency = 0
        self.HealingMagicPotency = 0
        self.SpellSpeed = 0
        self.Tenacity = 0
        self.Piety = 0
        self.iLVL = 0
        self.PhysicalDamage = 0
        self.AutoAttack = 0
        self.Delay = 0

        match Job:

            case 'CUSTOM':
                match Weapon:
                    case 1:
                        self.Gearslot.Weapon = "Asphodelos Longsword & Shield"      
                        self.AllowedMelds[0].update({'CRIT':0, 'DET':1, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 304
                        self.Vitality += 320
                        self.CriticalHit += 269
                        self.Determination += 188
                        self.iLVL += 605
                        self.PhysicalDamage = 120
                        self.AutoAttack = 89.60
                        self.Delay = 2.24
                        

            case 'WAR':
                match Weapon:
                    case 1:
                        self.Gearslot.Weapon = "Asphodelos War Hammer"      
                        self.AllowedMelds[0].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 304
                        self.Vitality += 320
                        self.CriticalHit += 269
                        self.Determination += 188
                        self.iLVL += 605
                        self.PhysicalDamage = 120
                        self.AutoAttack = 134.40
                        self.Delay = 3.36

                    case 2:
                        self.Gearslot.Weapon = "Augmented Radiant's Battleaxe"      
                        self.AllowedMelds[0].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 296
                        self.Vitality += 310
                        self.CriticalHit += 186
                        self.Determination += 266
                        self.iLVL += 600
                        self.PhysicalDamage = 119
                        self.AutoAttack = 133.28
                        self.Delay = 3.36

            case 'PLD':
                match Weapon:
                    case 1:
                        self.Gearslot.Weapon = "Asphodelos Longsword & Shield"      
                        self.AllowedMelds[0].update({'CRIT':0, 'DET':1, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 304
                        self.Vitality += 320
                        self.CriticalHit += 269
                        self.Determination += 188
                        self.iLVL += 605
                        self.PhysicalDamage = 120
                        self.AutoAttack = 89.60
                        self.Delay = 2.24

                    case 2:
                        self.Gearslot.Weapon = "Augmented Radiant's Bastard Sword & Shield"      
                        self.AllowedMelds[0].update({'CRIT':1, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 296
                        self.Vitality += 310
                        self.CriticalHit += 186
                        self.Determination += 266
                        self.iLVL += 600
                        self.PhysicalDamage = 119
                        self.AutoAttack = 88.85
                        self.Delay = 2.24

            case 'DRK':
                match Weapon:
                    case 1:
                        self.Gearslot.Weapon = "Asphodelos Claymore"      
                        self.AllowedMelds[0].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 304
                        self.Vitality += 320
                        self.CriticalHit += 269
                        self.Determination += 188
                        self.iLVL += 605
                        self.PhysicalDamage = 120
                        self.AutoAttack = 118.40
                        self.Delay = 2.96

                    case 2:
                        self.Gearslot.Weapon = "Augmented Radiant's Greatsword"      
                        self.AllowedMelds[0].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 296
                        self.Vitality += 310
                        self.CriticalHit += 186
                        self.Determination += 266
                        self.iLVL += 600
                        self.PhysicalDamage = 119
                        self.AutoAttack = 117.41
                        self.Delay = 2.96

            case 'GNB':
                match Weapon:
                    case 3:
                        self.Gearslot.Weapon = "Classical Gunblade"      
                        self.AllowedMelds[0].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 266
                        self.Vitality += 272
                        self.CriticalHit += 177
                        self.Determination += 253 
                        self.iLVL += 580
                        self.PhysicalDamage = 115
                        self.AutoAttack = 107.33
                        self.Delay = 2.80

                    case 2:
                        self.Gearslot.Weapon = "Augmented Radiant's Bayonet"      
                        self.AllowedMelds[0].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 296
                        self.Vitality += 310
                        self.CriticalHit += 186
                        self.Determination += 266
                        self.iLVL += 600
                        self.PhysicalDamage = 119
                        self.AutoAttack = 111.06
                        self.Delay = 2.80

                    case 1:
                        self.Gearslot.Weapon = "Asphodelos Bayonet"      
                        self.AllowedMelds[0].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                        self.TotalMelds[0] = 2
                        self.Strength += 304
                        self.Vitality += 320
                        self.CriticalHit += 269
                        self.Determination += 188
                        self.iLVL += 605
                        self.PhysicalDamage = 120
                        self.AutoAttack = 112.00
                        self.Delay = 2.80


        match Head:
            case 3:
                self.Gearslot.Head = "Radiant's Helm of Fending"
                self.AllowedMelds[1].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':1, 'SPS':0, 'TEN':2, 'PIE':0})
                self.TotalMelds[1] = 2
                self.Strength += 170
                self.Vitality += 176
                self.CriticalHit += 158
                self.SkillSpeed += 111
                self.iLVL += 590
                self.Defense += 765
                self.MagicDefense += 765

            case 2:
                self.Gearslot.Head = "Augmented Radiant's Helm of Fending"
                self.AllowedMelds[1].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':1, 'SPS':0, 'TEN':2, 'PIE':0})
                self.TotalMelds[1] = 2
                self.Strength += 180
                self.Vitality += 188
                self.CriticalHit += 162
                self.SkillSpeed += 113
                self.iLVL += 600
                self.Defense += 780
                self.MagicDefense += 780

            case 1:
                self.Gearslot.Head = "Asphodelos Circlet of Fending"
                self.AllowedMelds[1].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':1, 'PIE':0})
                self.TotalMelds[1] = 2
                self.Strength += 180
                self.Vitality += 188
                self.Determination += 162
                self.Tenacity += 113
                self.iLVL += 600
                self.Defense += 780
                self.MagicDefense += 780

        match Chest:
            case 3:
                self.Gearslot.Chest = "Classical Hoplomachus's Lorica"      
                self.AllowedMelds[2].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                self.TotalMelds[2] = 2
                self.Strength += 256
                self.Vitality += 262
                self.CriticalHit += 244
                self.Determination += 171 
                self.iLVL += 580
                self.Defense += 1006
                self.MagicDefense += 1006

            case 2:
                self.Gearslot.Chest = "Augmented Radiant's Scale Mail of Fending"      
                self.AllowedMelds[2].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                self.TotalMelds[2] = 2
                self.Strength += 285
                self.Vitality += 299
                self.Determination += 257
                self.Tenacity += 180
                self.iLVL += 600
                self.Defense += 1046
                self.MagicDefense += 1046

            case 1:
                self.Gearslot.Chest = "Asphodelos Chiton of Fending"      
                self.AllowedMelds[2].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                self.TotalMelds[2] = 2
                self.Strength += 285
                self.Vitality += 299
                self.CriticalHit += 257
                self.Determination += 180
                self.iLVL += 600
                self.Defense += 1046
                self.MagicDefense += 1046

        match Hands:
            case 3:
                self.Gearslot.Hands = "Limbo Vambraces of Fending"      
                self.AllowedMelds[3].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0}) 
                self.TotalMelds[3] = 2 
                self.Strength += 161
                self.Vitality += 165
                self.CriticalHit += 154
                self.Determination += 108 
                self.iLVL += 580
                self.Defense += 750
                self.MagicDefense += 750

            case 2:
                self.Gearslot.Hands = "Augmented Radiant's Gauntlets of Fending"      
                self.AllowedMelds[3].update({'CRIT':0, 'DET':1, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0}) 
                self.TotalMelds[3] = 2 
                self.Strength += 180
                self.Vitality += 188
                self.CriticalHit += 162
                self.Determination += 113 
                self.iLVL += 600
                self.Defense += 780
                self.MagicDefense += 780

            case 1:
                self.Gearslot.Hands = "Asphodelos Vambraces of Fending"      
                self.AllowedMelds[3].update({'CRIT':2, 'DET':1, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':0, 'PIE':0}) 
                self.TotalMelds[3] = 2 
                self.Strength += 180
                self.Vitality += 188
                self.Tenacity += 162
                self.Determination += 113 
                self.iLVL += 600
                self.Defense += 780
                self.MagicDefense += 780

        match Legs:
            case 3:
                self.Gearslot.Legs = "Classical Hoplomachus's Loincloth"      
                self.AllowedMelds[4].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                self.TotalMelds[4] = 2
                self.Strength += 256
                self.Vitality += 262
                self.CriticalHit += 171
                self.Determination += 244 
                self.iLVL += 580
                self.Defense += 1006
                self.MagicDefense += 1006

            case 2:
                self.Gearslot.Legs = "Augmented Radiant's Cuisses of Fending"      
                self.AllowedMelds[4].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                self.TotalMelds[4] = 2
                self.Strength += 285
                self.Vitality += 299
                self.CriticalHit += 180
                self.Determination += 257 
                self.iLVL += 600
                self.Defense += 1046
                self.MagicDefense += 1046

            case 1:
                self.Gearslot.Legs = "Asphodelos Skirt of Fending"      
                self.AllowedMelds[4].update({'CRIT':2, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                self.TotalMelds[4] = 2
                self.Strength += 285
                self.Vitality += 299
                self.Tenacity += 180
                self.Determination += 257 
                self.iLVL += 600
                self.Defense += 1046
                self.MagicDefense += 1046

        match Feet:
            case 1:
                self.Gearslot.Feet = "Asphodelos Boots of Fending"
                self.AllowedMelds[5].update({'CRIT':0, 'DET':2, 'DH':2, 'SKS':1, 'SPS':0, 'TEN':2, 'PIE':0})
                self.TotalMelds[5] = 2
                self.Strength += 180
                self.Vitality += 188
                self.CriticalHit += 162
                self.SkillSpeed += 113
                self.iLVL += 600
                self.Defense += 780
                self.MagicDefense += 780

            case 2:
                self.Gearslot.Feet = "Augmented Radiant's Sabatons of Fending"
                self.AllowedMelds[5].update({'CRIT':1, 'DET':2, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':0, 'PIE':0})
                self.TotalMelds[5] = 2
                self.Strength += 180
                self.Vitality += 188
                self.CriticalHit += 113
                self.Tenacity += 162
                self.iLVL += 600
                self.Defense += 780
                self.MagicDefense += 780

        match Ear:
            case 3:
                self.Gearslot.Ear = "Eternal Dark Earrings of Fending"      
                self.AllowedMelds[6].update({'CRIT':0, 'DET':1, 'DH':1, 'SKS':1, 'SPS':0, 'TEN':1, 'PIE':0})  
                self.TotalMelds[6] = 1
                self.Strength += 127
                self.Vitality += 130
                self.CriticalHit += 121
                self.Determination += 85 
                self.iLVL += 580
                self.Defense += 1
                self.MagicDefense += 1

            case 2:
                self.Gearslot.Ear = "Augmented Radiant's Earrings of Fending"      
                self.AllowedMelds[6].update({'CRIT':2, 'DET':2, 'DH':2, 'SKS':1, 'SPS':0, 'TEN':2, 'PIE':0})  
                self.TotalMelds[6] = 2
                self.Strength += 142
                self.Vitality += 148
                self.Determination += 127
                self.SkillSpeed += 89 
                self.iLVL += 600
                self.Defense += 1
                self.MagicDefense += 1

            case 1:
                self.Gearslot.Ear = "Asphodelos Earrings of Fending"      
                self.AllowedMelds[6].update({'CRIT':0, 'DET':1, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})  
                self.TotalMelds[6] = 2
                self.Strength += 142
                self.Vitality += 148
                self.CriticalHit += 127
                self.Determination += 89 
                self.iLVL += 600
                self.Defense += 1
                self.MagicDefense += 1

        match Neck:
            case 3:
                self.Gearslot.Neck = "Classical Choker of Fending"      
                self.AllowedMelds[7].update({'CRIT':0, 'DET':1, 'DH':1, 'SKS':1, 'SPS':0, 'TEN':1, 'PIE':0})    
                self.TotalMelds[7] = 1
                self.Strength += 127
                self.Vitality += 130
                self.CriticalHit += 121
                self.Determination += 85 
                self.iLVL += 580
                self.Defense += 1
                self.MagicDefense += 1

            case 2:
                self.Gearslot.Neck = "Augmented Radiant's Choker of Fending"      
                self.AllowedMelds[7].update({'CRIT':1, 'DET':2, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':0, 'PIE':0})    
                self.TotalMelds[7] = 2
                self.Strength += 142
                self.Vitality += 148
                self.CriticalHit += 89
                self.Tenacity += 127 
                self.iLVL += 600
                self.Defense += 1
                self.MagicDefense += 1

            case 1:
                self.Gearslot.Neck = "Asphodelos Necklace of Fending"      
                self.AllowedMelds[7].update({'CRIT':2, 'DET':1, 'DH':2, 'SKS':0, 'SPS':0, 'TEN':2, 'PIE':0})    
                self.TotalMelds[7] = 2
                self.Strength += 142
                self.Vitality += 148
                self.Determination += 89
                self.SkillSpeed += 127 
                self.iLVL += 600
                self.Defense += 1
                self.MagicDefense += 1

        match Bracelet:
            case 2:
                self.Gearslot.Bracelet = "Augmented Radiant's Bracelet of Fending"      
                self.AllowedMelds[8].update({'CRIT':1, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})    
                self.TotalMelds[8] = 2
                self.Strength += 142
                self.Vitality += 148
                self.CriticalHit += 89
                self.Determination += 127 
                self.iLVL += 600
                self.Defense += 1
                self.MagicDefense += 1

            case 1:
                self.Gearslot.Bracelet = "Asphodelos Amulet of Fending"      
                self.AllowedMelds[8].update({'CRIT':2, 'DET':1, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':0, 'PIE':0})    
                self.TotalMelds[8] = 2
                self.Strength += 142
                self.Vitality += 148
                self.Determination += 89
                self.Tenacity += 127 
                self.iLVL += 600
                self.Defense += 1
                self.MagicDefense += 1

        match Ring1:
            case 2:
                self.Gearslot.Ring1 = "Augmented Classical Ring of Fending"      
                self.AllowedMelds[9].update({'CRIT':1, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0}) 
                self.TotalMelds[9] = 2  
                self.Strength += 134
                self.Vitality += 139
                self.CriticalHit += 87
                self.Determination += 124 
                self.iLVL += 590
                self.Defense += 1
                self.MagicDefense += 1

            case 1:
                self.Gearslot.Ring1 = "Augmented Radiant's Ring of Fending"      
                self.AllowedMelds[9].update({'CRIT':2, 'DET':2, 'DH':2, 'SKS':1, 'SPS':0, 'TEN':0, 'PIE':0})   
                self.TotalMelds[9] = 2
                self.Strength += 142
                self.Vitality += 148
                self.SkillSpeed += 89
                self.Tenacity += 127 
                self.iLVL += 600
                self.Defense += 1
                self.MagicDefense += 1

        match Ring2:
            case 2:
                self.Gearslot.Ring2 = "Augmented Classical Ring of Fending"      
                self.AllowedMelds[10].update({'CRIT':1, 'DET':0, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0}) 
                self.TotalMelds[10] = 2  
                self.Strength += 134
                self.Vitality += 139
                self.CriticalHit += 87
                self.Determination += 124 

                self.iLVL += 590
                self.Defense += 1
                self.MagicDefense += 1

            case 1:
                self.Gearslot.Ring2 = "Asphodelos Ring of Fending"      
                self.AllowedMelds[10].update({'CRIT':0, 'DET':1, 'DH':2, 'SKS':2, 'SPS':0, 'TEN':2, 'PIE':0})   
                self.TotalMelds[10] = 2
                self.Strength += 142
                self.Vitality += 148
                self.Determination += 89
                self.CriticalHit += 127 
                self.iLVL += 600
                self.Defense += 1
                self.MagicDefense += 1

        self.iLVL = round(self.iLVL/11)
        #self.CalcAffinity()


    def ShowMeldSlots(self):
        print("Available meld slots in gearset")
        print(" ")
        for i,j in zip(self.Gearslot.__dict__.values(), self.AllowedMelds):
            print(f"{i:<50}{j}")

    def CalcAffinity(self):
        for stat in self.AllowedMelds[0].keys():
            for gearidx in range(len(self.AllowedMelds)):
                total = sum(self.AllowedMelds[gearidx].values())
                specific = self.AllowedMelds[gearidx][stat]
                self.Affinity[gearidx][stat] = math.floor(10000 * (specific + 1) / total) 





class Melds():
    def __init__(self, CRIT, DET, DH, SKS, SPS, TEN, PIE):
        self.CriticalHit = CRIT * 36
        self.Determination = DET * 36
        self.DirectHitRate = DH * 36
        self.SkillSpeed = SKS * 36
        self.SpellSpeed = SPS * 36
        self.Tenacity = TEN * 36
        self.Piety = PIE * 36

    def show(self):
        pass



if __name__ == "__main__":
    Main()
