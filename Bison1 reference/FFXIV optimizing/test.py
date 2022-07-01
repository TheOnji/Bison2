

def Main():
    pass


class Equip():
    def __init__(self, Character, Gear, Melds):

        def Damage(self, Potency):
            fDET = Determination(self.Determination)
            fAP = AttackPower(self.AttackPower)
            Damage = (((Potency * fDET * fAP) / 100) / 1000)
            return Damage


        def LevelLv(self):
            MAIN = [202, 218, 292, 340, 390][[50, 60, 70, 80, 90].index(self.Character.Level)]
            SUB = [341, 354, 364, 380, 400][[50, 60, 70, 80, 90].index(self.Character.Level)]
            DIV = [341, 600, 900, 1300, 1900][[50, 60, 70, 80, 90].index(self.Character.Level)]
            HP = [1700, None, None, 1300, 3000][[50, 60, 70, 80, 90].index(self.Character.Level)]
            return MAIN, SUB, DIV, HP


        def JobModifier(self):
            match self.Character.Job:
                case 'GNB':
                    jobmod = {'HP':120, 'MP':100, 'STR':100, 'VIT':110, 'DEX':95, 'INT':60, 'MND':100}
            return jobmod


        def Determination(self):
            MAIN, SUB, DIV = LevelLv(self.Character.Level)
            fDET = (130*(self.Determination - MAIN) / DIV + 1000)
            return fDET


        def CriticalHit(self):
            MAIN, SUB, DIV = LevelLv(self.Character.Level)
            pCRIT = ((200*(self.CriticalHit - SUB)/DIV) + 50)/10
            fCRIT = 1400 + (200*(self.CriticalHit - SUB)/DIV)
            return fCRIT, pCRIT


        def DirectHit(self):
            MAIN, SUB, DIV = LevelLv(self.Character.Level)
            fDH = 125
            pDH = (550*(self.DirectHit - SUB)/DIV) / 10
            return fDH, pDH


        def Tenacity(self):
            MAIN, SUB, DIV = LevelLv(self.Character.Level)
            fTEN = 100 * (self.Tenacity - SUB) / DIV + 1000
            return fTEN


        def Speed(self):
            MAIN, SUB, DIV = LevelLv(self.Character.Level)
            fSPD = 130 * (self.SkillSpeed - SUB) / DIV + 1000
            return fSPD


        def AutoAttack(self):
            MAIN, SUB, DIV = LevelLv(self.Character.Level)
            JobMod = JobModifier(self.Character.Job)
            fAUTO = ((MAIN * JobMod['STR'] / 1000) + self.WeaponDamage) * (self.Delay / 3)
            return fAUTO


        def WeaponDamage(self):
            MAIN, SUB, DIV = LevelLv(self.Character.Level)
            JobMod = JobModifier(self.Character.Job)
            fWD = ((MAIN * JobMod['STR'] / 1000) + self.WeaponDamage)
            return fWD


        def AttackPower(self):
            # fAP = (165  * ( AP - 340 ) / 340 ) + 100 #Non-Tanks Level 80
            fAP = (115 * (self.AttackPower - 340) / 340) + 100  # Tanks Level 80
            return fAP

        def HP_Tank(self):
            #MAIN, SUB, DIV, HP = LevelLv(self.Character.Level)
            JobMod = JobModifier(self.Character.Job)
            HealthPoints = round((self.HP * (JobMod['HP'] / 100) ) + ( (self.Vitality - self.MAIN) * 31.5 ))
            return HealthPoints

        def Direct_Damage(self, Potency, buff_1 = 1.0, buff_2 = 1.0):
            fATK = WeaponDamage(self.Character.Job, self.WeaponDamage, self.Character.Level)
            fDET = Determination(self.Determination)

            D1 = ((Potency * fATK * fDET) / 100) / 1000
            D2 = (((((D1 * fTEN) / 1000) * fWD) / 100) * Trait) / 100
            D3 = ((((D2 * modCRIT) / 1000) * modDH) / 100)
            D = ((((D3 * np.randint(95, 105)) / 100) * buff_1) * buff_2)
            return D

        def DoT_Damage(self, buff_1 = 1.0, buff_2 = 1.0):
            D1 = (((Potency * fATK * fDET) / 100) / 1000)
            D2 = ((((((((D1 * fTEN) / 1000) * fSPD) / 1000) * fWD) / 100) * Trait) / 100) + 1
            D3 = ((D2 * np.randint(95, 105)) / 100)
            D = ((((((D3 * modCRIT) / 1000) * modDH) / 100) * buff_1) * buff_2)
            return D

        def AutoAtk_Damage(self, buff_1 = 1.0, buff_2 = 1.0):
            D1 = (((Potency * fATK * fDET ) /100 ) /1000 )
            D2 = ((((((((D1 * fTEN ) /1000 ) * fSPD ) /1000 )* fAUTO ) /100 ) * Trait ) /100 )
            D3 = ((((D2 * modCRIT ) /1000 ) * modDH ) /100 )
            D = ((((D3 * np.randint(95,105) ) /100 ) * buff_1 ) * buff_2 )
            return D


        #Raw Stats
        self.Level = Character.Level
        self.Strength = Character.Strength + Gear.Strength
        self.Dexterity = Character.Dexterity + Gear.Dexterity
        self.Vitality = Character.Vitality + Gear.Vitality
        self.Intelligence = Character.Intelligence + Gear.Intelligence 
        self.Mind = Character.Mind + Gear.Mind
        self.CriticalHit = Character.CriticalHit + Gear.CriticalHit + Melds.CriticalHit
        self.Determination = Character.Determination + Gear.Determination + Melds.Determination
        self.DirectHitRate = Character.DirectHitRate + Gear.DirectHitRate + Melds.DirectHitRate
        self.Defense = Character.Defense + Gear.Defense
        self.MagicDefense = Character.MagicDefense + Gear.MagicDefense
        self.AttackPower = Character.AttackPower
        self.SkillSpeed = Character.SkillSpeed + Gear.SkillSpeed + Melds.SkillSpeed
        self.AttackMagicPotency = Character.AttackMagicPotency
        self.HealingMagicPotency = Character.HealingMagicPotency
        self.SpellSpeed = Character.SpellSpeed + Gear.SpellSpeed + Melds.SpellSpeed
        self.Tenacity = Character.Tenacity + Gear.Tenacity + Melds.Tenacity
        self.Piety = Character.Piety + Gear.Piety + Melds.Piety
        self.iLVL = Gear.iLVL
        self.PhysicalDamage = Gear.AttackPower
        self.AutoAttack = Gear.AutoAttack
        self.Delay = Gear.Delay
        self.AttackPower = self.Strength

        #Calculated stats
        self.MAIN, self.SUB, self.DIV, self.HP = self.LevelLv()
        self.HP = self.HP_Tank()
        self.fCRIT, self.pCRIT = self.CriticalHit()
        self.fDET = self.Determination()
        self.fDH, self.pDH = self.DirectHit()
        self.fTEN = self.Tenacity()
        self.fSPD = self.Speed()
        self.fAUTO = self.AutoAttack()
        self.fWD = self.WeaponDamage()
        self.AP = self.AttackPower()


    def show(self):
        print("_"*26 + 'STAT SUMMARY' + "_"*26)
        print(f"{'Attributes':<35}{'HP:':<20}{self.HP:^15}")
        print(f"{'Strength:':<20}{self.Strength:^15}{'Intelligence:':<20}{self.Intelligence:^15}")
        print(f"{'Dexterity:':<20}{self.Dexterity:^15}{'Mind:':<20}{self.Mind:^15}")
        print(f"{'Vitality:':<20}{self.Vitality:^15}")
        print(" ")
        print(f"{'Offensive Properties':<34} {'Defensive Properties':<34}")
        print(f"{'Critical Hit:':<20}{self.CriticalHit:^15}{'Defense:':<20}{self.Defense:^15}")
        print(f"{'Determination:':<20}{self.Determination:^15}{'Magic Defense:':<20}{self.MagicDefense:^15}")
        print(f"{'Direct Hit Rate:':<20}{self.DirectHitRate:^15}")
        print(" ")
        print(f"{'Physical Properties':<34} {'Mental Properties':<34}")
        print(f"{'Attack Power:':<20}{self.AttackPower:^15}{'Attack Magic Power:':<20}{self.AttackMagicPotency:^15}")
        print(f"{'Skill Speed:':<20}{self.SkillSpeed:^15}{'Healing Magic Power:':<20}{self.HealingMagicPotency:^15}")
        print(f"{' ':<35}{'Spell Speed:':<20}{self.SpellSpeed:^15}")
        print(" ")
        print(f"{'Gear':<34} {'Role':<34}")
        print(f"{'Average Item Level:':<20}{self.iLVL:^15}{'Tenacity:':<20}{self.Tenacity:^15}")
        print(f"{' ':<35}{'Piety:':<20}{self.Piety:^15}")
        print("_"*64)


    

if __name__ == "__main__":
    Main()
