import math

def Main():
    pass


class Equip():
    def __init__(self, Character, Gear, Melds, Food):
        #Add subclasses
        self.Character = Character
        self.Gear = Gear
        self.Melds = Melds
        self.Food = Food

        #Sum up main stats
        self.Strength = Character.Strength + Gear.Strength
        self.Dexterity = Character.Dexterity + Gear.Dexterity
        self.Vitality = Character.Vitality + Gear.Vitality + Food.Vitality
        self.Intelligence = Character.Intelligence + Gear.Intelligence 
        self.Mind = Character.Mind + Gear.Mind

        #5% add
        #self.Strength = self.Strength*1.05

        #Sum up substats
        self.CriticalHit = Character.CriticalHit + Gear.CriticalHit + Melds.CriticalHit 
        self.Determination = Character.Determination + Gear.Determination + Melds.Determination 
        self.DirectHitRate = Character.DirectHitRate + Gear.DirectHitRate + Melds.DirectHitRate 
        self.SkillSpeed = Character.SkillSpeed + Gear.SkillSpeed + Melds.SkillSpeed 
        self.Tenacity = Character.Tenacity + Gear.Tenacity + Melds.Tenacity 
        self.SpellSpeed = Character.SpellSpeed + Gear.SpellSpeed + Melds.SpellSpeed
        self.Piety = Character.Piety + Gear.Piety + Melds.Piety

        #Eat some food
        self.CriticalHit += math.floor(min(self.CriticalHit * Food.percent, Food.CriticalHit))
        self.Determination += math.floor(min(self.Determination * Food.percent, Food.Determination))
        self.DirectHitRate += math.floor(min(self.DirectHitRate * Food.percent, Food.DirectHitRate))
        self.SkillSpeed += math.floor(min(self.SkillSpeed * Food.percent, Food.SkillSpeed))
        self.Tenacity += math.floor(min(self.Tenacity * Food.percent, Food.Tenacity))
        self.SpellSpeed += math.floor(min(self.SpellSpeed * Food.percent, Food.SpellSpeed))
        self.Piety += math.floor(min(self.Piety * Food.percent, Food.Piety))

        #Sum up defensives
        self.Defense = Character.Defense + Gear.Defense
        self.MagicDefense = Character.MagicDefense + Gear.MagicDefense

        #Sum up Offensives
        self.AttackMagicPotency = Character.AttackMagicPotency
        self.HealingMagicPotency = Character.HealingMagicPotency
        
        #Extract weapon properties
        self.PhysicalDamage = Gear.PhysicalDamage
        self.AutoAttack = Gear.AutoAttack
        self.Delay = Gear.Delay

        #Additional attributes
        self.AttackPower = self.Strength  #Job dependant!
        self.Trait = 100.0

        #Calculate modifiers
        self.MAIN, self.SUB, self.DIV, self.HP_LV = self.LevelLv()
        self.JobMod = self.JobModifier()
        self.HP = self.HP_Tank()
        self.fCRIT, self.pCRIT = self.fCriticalHit()
        self.fDET = self.fDetermination()
        self.fDH, self.pDH = self.fDirectHit()
        self.fTEN = self.fTenacity()
        self.fSPD = self.fSpeed()
        self.fAUTO = self.fAutoAttack()
        self.fWD = self.fWeaponDamage()
        self.fATK = self.fAttack()
        self.GCD = self.fGCD(2.50)
        self.dps, self.dps_rating = self.dps()

    def TierDiff(self):
        search = 1
        steps = 1
        trigger = [0, 0, 0, 0, 0, 0, 0]
        self.ClosestTiers = {'CRIT':0, 'DET':0, 'DH':0, 'SKS':0, 'SPS':0, 'TEN':0, 'PIE':0, 'GCD':0}

        while search == 1:
            #Crit 
            fCRIT_up, _ = self.fCriticalHit(self.CriticalHit + steps)
            fCRIT_down, _ = self.fCriticalHit(self.CriticalHit - steps)

            fDET_up = self.fDetermination(self.Determination + steps)
            fDET_down = self.fDetermination(self.Determination - steps)

            _, pDH_up = self.fDirectHit(self.DirectHitRate + steps) 
            _, pDH_down = self.fDirectHit(self.DirectHitRate - steps) 

            fSKS_up = self.fSpeed(self.SkillSpeed + steps)
            fSKS_down = self.fSpeed(self.SkillSpeed - steps)

            fTEN_up = self.fTenacity(self.Tenacity + steps)
            fTEN_down = self.fTenacity(self.Tenacity - steps)

            GCD_up = self.fGCD(2.50, self.SkillSpeed + steps)
            GCD_down = self.fGCD(2.50, self.SkillSpeed - steps)


            if not fCRIT_up == self.fCRIT and trigger[0] == 0:
                self.ClosestTiers['CRIT'] = f"+{steps}"
                trigger[0] = 1

            if not fCRIT_down == self.fCRIT and trigger[0] == 0:
                self.ClosestTiers['CRIT'] = f"-{steps - 1}"
                trigger[0] = 1

            if not fDET_up == self.fDET and trigger[1] == 0:
                self.ClosestTiers['DET'] = f"+{steps}"
                trigger[1] = 1

            if not fDET_down == self.fDET and trigger[1] == 0:
                self.ClosestTiers['DET'] = f"-{steps - 1}"
                trigger[1] = 1

            if not pDH_up == self.pDH and trigger[2] == 0:
                self.ClosestTiers['DH'] = f"+{steps}"
                trigger[2] = 1

            if not pDH_down == self.pDH and trigger[2] == 0:
                self.ClosestTiers['DH'] = f"-{steps - 1}"
                trigger[2] = 1

            if not fSKS_up == self.fSPD and trigger[3] == 0:
                self.ClosestTiers['SKS'] = f"+{steps}"
                trigger[3] = 1

            if not fSKS_down == self.fSPD and trigger[3] == 0:
                self.ClosestTiers['SKS'] = f"-{steps - 1}"
                trigger[3] = 1

            if not fTEN_up == self.fTEN and trigger[4] == 0:
                self.ClosestTiers['TEN'] = f"+{steps}"
                trigger[4] = 1

            if not fTEN_down == self.fTEN and trigger[4] == 0:
                self.ClosestTiers['TEN'] = f"-{steps - 1}"
                trigger[4] = 1

            if not GCD_up == self.GCD and trigger[5] == 0:
                self.ClosestTiers['GCD'] = f"+{steps}"
                trigger[5] = 1

            if not GCD_down == self.GCD and trigger[5] == 0:
                self.ClosestTiers['GCD'] = f"-{steps - 1}"
                trigger[5] = 1

            steps += 1
            if sum(trigger) > 5 or steps > 100:
                search = 0


    def show(self, outfile = None):
        self.TierDiff()

        print("_"*26 + 'STAT SUMMARY' + "_"*26, file = outfile)
        print(f"{'Attributes':<35}", file = outfile)
        print(f"{'Strength:':<20}{self.Strength:^15}{'Intelligence:':<20}{self.Intelligence:^15}", file = outfile)
        print(f"{'Dexterity:':<20}{self.Dexterity:^15}{'Mind:':<20}{self.Mind:^15}", file = outfile)
        print(f"{'Vitality:':<20}{self.Vitality:^15}", file = outfile)
        print(" ", file = outfile)
        print(f"{'Offensive Properties':<34} {'Defensive Properties':<34}", file = outfile)
        print(f"{'Critical Hit:':<20}{self.CriticalHit:>9} ({self.ClosestTiers['CRIT']}) {'Defense:':<20}{self.Defense:^15}", file = outfile)
        print(f"{'Determination:':<20}{self.Determination:>9} ({self.ClosestTiers['DET']}) {'Magic Defense:':<20}{self.MagicDefense:^15}", file = outfile)
        print(f"{'Direct Hit Rate:':<20}{self.DirectHitRate:>9} ({self.ClosestTiers['DH']})", file = outfile)
        print(" ", file = outfile)
        print(f"{'Physical Properties':<34} {'Mental Properties':<34}", file = outfile)
        print(f"{'Attack Power:':<20}{self.AttackPower:^15}{'Attack Magic Power:':<20}{self.AttackMagicPotency:^15}", file = outfile)
        print(f"{'Skill Speed:':<20}{self.SkillSpeed:>9} ({self.ClosestTiers['SKS']}) {'Healing Magic Power:':<20}{self.HealingMagicPotency:^15}", file = outfile)
        print(f"{' ':<35}{'Spell Speed:':<20}{self.SpellSpeed:^15}", file = outfile)
        print(" ", file = outfile)
        print(f"{'Gear':<34} {'Role':<34}", file = outfile)
        print(f"{'Average Item Level:':<20}{self.Gear.iLVL:^15}{'Tenacity:':<20}{self.Tenacity:>9} ({self.ClosestTiers['TEN']}) ", file = outfile)
        print(f"{' ':<35}{'Piety:':<20}{self.Piety:^15}", file = outfile)
        print(" -"*32, file = outfile)
        print(f"{'HP:':<20}{self.HP:^15}{'GCD:':<20}{self.GCD:>9} ({self.ClosestTiers['GCD']}) ", file = outfile)
        print(f"{'DPS:':<20}{self.dps:^15}{'DPS rating':<20}{self.dps_rating:^15}", file = outfile)
        print(f"{'Critical Hit Rate:':<20}{str(self.pCRIT) + ' %':^15}{'Critical Hit Dmg':<20}{'+' + str((self.fCRIT-1000)/10) + ' %':^15}", file = outfile)
        print(f"{'Direct Hit Rate:':<20}{str(self.pDH) + ' %':^15}{'Direct Hit Dmg':<20}{'+25.0 %':^15}", file = outfile)
        print(f"{'CDH Rate:':<20}{str(round(self.pCRIT*self.pDH/100, 2)) + ' %':^15}{'CDH Dmg':<20}{'+' + str(round((self.fCRIT/1000 * 1.25 - 1)*100, 1)) + ' %':^15}", file = outfile)
        print(f"{'Food:':<5}{self.Food.Food:>25}     {' ':<12}{' ':10}", file = outfile)
        print(f"{'Food stats:':<15}{self.Food.Foodstats:>15}     {' ':<12}{' ':>19}", file = outfile)
        print("_"*64, file = outfile)

    def show_f(self):
        print(f"Main: {self.MAIN}")
        print(f"JobMod: {self.JobMod}")
        print(f"fCRIT: {self.fCRIT}")
        print(f"fDET: {self.fDET}")
        print(f"fDH: {self.fDH}")
        print(f"fTEN: {self.fTEN}")
        print(f"fSPD: {self.fSPD}")
        print(f"fAUTO: {self.fAUTO}")
        print(f"fWD: {self.fWD}")
        print(f"fATK: {self.fATK}")
        print(f"GCD: {self.GCD}")
        print(f"dps: {self.dps}")


    def Damage(self, Potency):
        Damage = (((Potency * self.fDET * self.fAP) / 100) / 1000)
        return Damage


    def LevelLv(self):
        MAIN = [202, 218, 292, 340, 390][[50, 60, 70, 80, 90].index(self.Character.Level)]
        SUB = [341, 354, 364, 380, 400][[50, 60, 70, 80, 90].index(self.Character.Level)]
        DIV = [341, 600, 900, 1300, 1900][[50, 60, 70, 80, 90].index(self.Character.Level)]
        HP = [1700, None, None, 1300, 3000][[50, 60, 70, 80, 90].index(self.Character.Level)]
        return MAIN, SUB, DIV, HP


    def JobModifier(self):
        match self.Character.Job:

            case 'CUSTOM':
                jobmod = {'HP':142.5, 'MP':100, 'STR':102.5, 'VIT':110, 'DEX':95, 'INT':60, 'MND':77.5}

            case 'GNB':
                jobmod = {'HP':120, 'MP':100, 'STR':100, 'VIT':110, 'DEX':95, 'INT':60, 'MND':100}

            case 'DRK':
                jobmod = {'HP':140, 'MP':100, 'STR':105, 'VIT':110, 'DEX':95, 'INT':60, 'MND':40}

            case 'WAR':
                jobmod = {'HP':145, 'MP':100, 'STR':105, 'VIT':110, 'DEX':95, 'INT':60, 'MND':55}

            case 'PLD':
                jobmod = {'HP':140, 'MP':100, 'STR':100, 'VIT':110, 'DEX':95, 'INT':60, 'MND':100}

        return jobmod


    def fDetermination(self, DET = -1):
        if DET < 0:
            Determination = self.Determination
        else:
            Determination = DET

        fDET = math.floor(140*(Determination - self.MAIN) / self.DIV + 1000)
        return fDET


    def fCriticalHit(self, CRIT = -1):
        if CRIT < 0:
            CriticalHit = self.CriticalHit
        else:
            CriticalHit = CRIT

        pCRIT = math.floor(200 * (CriticalHit - self.SUB)/self.DIV + 50) / 10
        fCRIT = math.floor(200 * (CriticalHit - self.SUB)/self.DIV + 1400)
        return fCRIT, pCRIT


    def fDirectHit(self, DH = -1):
        if DH < 0:
            DirectHit = self.DirectHitRate
        else:
            DirectHit = DH

        fDH = 125
        pDH = math.floor(550*(DirectHit - self.SUB)/self.DIV) / 10

        return fDH, pDH


    def fTenacity(self, TEN = -1):
        if TEN < 0:
            Tenacity = self.Tenacity
        else:
            Tenacity = TEN

        fTEN = math.floor(100 * (Tenacity - self.SUB) / self.DIV + 1000)
        return fTEN


    def fSpeed(self, SKS = -1):
        if SKS < 0:
            SkillSpeed = self.SkillSpeed
        else:
            SkillSpeed = SKS

        fSPD = math.floor(130 * (SkillSpeed - self.SUB) / self.DIV + 1000)
        return fSPD


    def fAutoAttack(self):
        fAUTO = math.floor(math.floor(self.MAIN * self.JobMod['STR'] / 1000 + self.Gear.PhysicalDamage) * self.Delay/3)
        return fAUTO


    def fWeaponDamage(self):
        fWD = math.floor(self.MAIN * self.JobMod['STR'] / 1000 + self.Gear.PhysicalDamage)
        return fWD


    def fAttack(self):
        # fAP = (165  * ( AP - 340 ) / 340 ) + 100 #Non-Tanks Level 80
        fATK = math.floor(115 * (self.AttackPower - 340) / 340) + 100  # Tanks Level 80
        return fATK

    def HP_Tank(self):
        HealthPoints = self.Character.HP + math.floor(self.HP_LV * self.JobMod['HP'] / 100) + math.floor((self.Vitality - self.MAIN) * 31.5 )
        return HealthPoints

    def GCD(self, SKS = -1):
        if SKS < 0:
            SkillSpeed = self.SkillSpeed
        else:
            SkillSpeed = SKS

        k = 1900 / 130
        mults_of_k = math.floor((SkillSpeed - 400) / k)

        if mults_of_k < 1:
            GCD = 2.50
        elif mults_of_k == 1:
            GCD = 2.50 - 0.01
        elif mults_of_k > 1:
            m = math.floor((mults_of_k - 1) / 4)
            GCD = 2.49 - 0.01 * m

        return round(GCD, 2)

    def fGCD(self, CD, SKS = -1):
        if SKS < 0:
            SkillSpeed = self.SkillSpeed
        else:
            SkillSpeed = SKS

        CD = CD * 1000
        GCD = math.floor(CD * (1000 + math.ceil(130 * (self.SUB - SkillSpeed)/ self.DIV)) / 10000) / 100 
        return GCD


    def dps(self):
        job = self.Character.Job
        gain = 1.0

        match job:

            case 'CUSTOM':
                #PLD and WAR combined for omni

                dps1_normal = 16.28 * self.AutoAtk_Damage(110, buff_1 = 1.0) + self.Direct_Damage(5584, buff_1 = 1.0) + self.DoT_Damage(677, buff_1 = 1.0) + self.DoT_Magical(459, buff_1 = 1.0)
                dps1_fof = 10.14 * self.AutoAtk_Damage(110, buff_1 = 1.25) + self.Direct_Damage(3786, buff_1 = 1.25) + self.DoT_Damage(506, buff_1 = 1.25)
                dps1 = (dps1_normal + dps1_fof) / 60
                dps1_rating = 10000 * dps1 / (5584+677+459+3786+506)

                dps2_normal = 17.81 * self.AutoAtk_Damage(110) + self.Direct_Damage(7004)
                dps2_CDH = self.Direct_Damage(3303, CDH = 1)                
                dps2 = (dps2_normal + dps2_CDH) / 60
                dps2_rating = 10000 * dps2 / (7004 + 3303)

                dps = (dps1 + dps2) / 2
                dps_rating = (dps1_rating + dps2_rating) / 2


            case 'GNB':
                dps_normal = 14.35 * self.AutoAtk_Damage(110) + self.Direct_Damage(6375)
                dps_NM = 7.04 * self.AutoAtk_Damage(110, buff_1 = 1.2) + self.Direct_Damage(5981, buff_1 = 1.2) + self.DoT_Damage(893, buff_1 = 1.2)
                dps = (dps_normal + dps_NM) / 60
                dps_rating = 10000 * dps / (6375 + 5981 + 893)

            case 'DRK':
                dps = 20.19 * self.AutoAtk_Damage(110) + self.Direct_Damage(15002)
                dps = dps / 60
                dps_rating = 10000 * dps / (15002)

            case 'WAR':
                dps_normal = 17.81 * self.AutoAtk_Damage(110) + self.Direct_Damage(7004)
                dps_CDH = self.Direct_Damage(3303, CDH = 1)
                
                dps = (dps_normal + dps_CDH) / 60
                dps_rating = 10000 * dps / (7004 + 3303)

            case 'PLD':
                dps_normal = 16.28 * self.AutoAtk_Damage(110, buff_1 = 1.0) + self.Direct_Damage(5584, buff_1 = 1.0) + self.DoT_Damage(677, buff_1 = 1.0) + self.DoT_Magical(459, buff_1 = 1.0)
                dps_fof = 10.14 * self.AutoAtk_Damage(110, buff_1 = 1.25) + self.Direct_Damage(3786, buff_1 = 1.25) + self.DoT_Damage(506, buff_1 = 1.25)
                dps = (dps_normal + dps_fof) / 60
                dps_rating = 10000 * dps / (5584+677+459+3786+506)

        return math.floor(dps), round(dps_rating, 2)


    def Direct_Damage(self, Potency, buff_1 = 1.0, buff_2 = 1.0, CalcAverage = 1, CDH = 0):
        D1 = math.floor(math.floor(math.floor(Potency * self.fATK * self.fDET) / 100) / 1000)
        D2 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D1 * self.fTEN) / 1000) * self.fWD) / 100) * self.Trait) / 100)
        if CDH == 1:
            modCRIT = self.fCRIT
            modDH = self.fDH
        elif CalcAverage == 1:
            modCRIT = (self.fCRIT * self.pCRIT + (100-self.pCRIT) * 1000) / 100
            modDH = (self.fDH * self.pDH + (100 - self.pDH) * 100) / 100
        else:
            #To be added...
            modCRIT = 1
            modDH = 1
        D3 = math.floor(math.floor(math.floor(math.floor(D2 * modCRIT) / 1000) * modDH) / 100)
        D = math.floor(math.floor(math.floor(math.floor(D3 * 100) / 100) * buff_1) * buff_2)
        return D

    def DoT_Damage(self, Potency, buff_1 = 1.0, buff_2 = 1.0, CalcAverage = 1):
        D1 = math.floor(math.floor(math.floor(Potency * self.fATK * self.fDET) / 100) / 1000)
        D2 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D1 * self.fTEN) / 1000) * self.fSPD) / 1000) * self.fWD) / 100) * self.Trait) / 100) + 1
        if CalcAverage == 1:
            modCRIT = (self.fCRIT * self.pCRIT + (100-self.pCRIT) * 1000) / 100
            modDH = (self.fDH * self.pDH + (100 - self.pDH) * 100) / 100
        else:
            #To be added...
            modCRIT = 1.0
            modDH = 1.0
        D3 = math.floor(math.floor(D2 * 100) / 100)
        D = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D3 * modCRIT) / 1000) * modDH) / 100) * buff_1) * buff_2)
        return D

    def DoT_Magical(self, Potency, buff_1 = 1.0, buff_2 = 1.0, CalcAverage = 1):
        D1 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(Potency * self.fWD)/100)*self.fATK)/100)*self.fSPD)/1000)
        D2 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D1 * self.fDET)/1000)*self.fTEN)/1000)*self.Trait)/100)+1
        D3 = math.floor(math.floor(D2 * 100)/100)
        if CalcAverage == 1:
            modCRIT = (self.fCRIT * self.pCRIT + (100-self.pCRIT) * 1000) / 100
            modDH = (self.fDH * self.pDH + (100 - self.pDH) * 100) / 100

        D = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D3*modCRIT)/1000)*modDH)/100)*buff_1)*buff_2)
        return D

    def AutoAtk_Damage(self, Potency, buff_1 = 1.0, buff_2 = 1.0, CalcAverage = 1):
        D1 = math.floor(math.floor(math.floor(Potency * self.fATK * self.fDET) /100 ) /1000 )
        D2 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D1 * self.fTEN) /1000 ) * self.fSPD ) /1000 ) * self.fAUTO ) /100 ) * self.Trait ) /100 )
        if CalcAverage == 1:
            modCRIT = (self.fCRIT * self.pCRIT + (100-self.pCRIT) * 1000) / 100
            modDH = (self.fDH * self.pDH + (100 - self.pDH) * 100) / 100
        else:
            #To be added...
            modCRIT = 1.0
            modDH = 1.0

        D3 = math.floor(math.floor(math.floor(math.floor(D2 * modCRIT ) /1000 ) * modDH ) /100 )
        D = math.floor(math.floor(math.floor(math.floor(D3 * 100 ) /100 ) * buff_1 ) * buff_2 )
        return D

if __name__ == "__main__":
    Main()
