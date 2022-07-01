import itertools
import copy
import time
import math
import os
import random
from sys import stdout

from Gear import *
from Character import *
from Functions import *
from Food import *
from MeldFunctions import *


def Main():
    setJob = 'GNB'
    Onji = Character(Name = 'Onji',
                    Job = setJob,
                    Level = 90,
                    HP = 7897,
                    Strength = 392, 
                    Dexterity = 373, 
                    Vitality = 429, 
                    Intelligence = 233, 
                    Mind = 389, 
                    CriticalHit = 400, 
                    Determination = 390, 
                    DirectHitRate = 400,
                    Defense = 0, 
                    MagicDefense = 0, 
                    AttackPower = 658, 
                    SkillSpeed = 400, 
                    AttackMagicPotency = 233, 
                    HealingMagicPotency = 389, 
                    SpellSpeed = 400, 
                    Tenacity = 400, 
                    Piety = 390)


    dothis = 0
    if dothis == 1: #Checking single gearsets

        CurrentGear = Gearset_Fending(setJob, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1)
        #Warrior Omni melds
        CurrentMelds = Melds(6, 11, 5, 0, 0, 0, 0)

        #Other tanks Omni melds
        CurrentMelds = Melds(6, 11, 5, 0, 0, 0, 0)

        success, Slotted_melds  = MeldTest_Reslot_Twice([6, 11, 5, 0, 0, 0, 0], CurrentGear)
        print(success, Slotted_melds)
        CurrentFood = Food(3)
        FullSet = Equip(Onji, CurrentGear, CurrentMelds, CurrentFood)   

        FullSet.show()
        for k, b in zip(CurrentGear.Gearslot.__dict__.values(), Slotted_melds):
                print(f"{k:50} {b}")



    #Debug melding algorithm
    #melds2test = [4, 1, 17, 0, 0, 0, 0]
    #melds2test = [1, 1, 0, 5, 0, 15, 0]
    #s, sets = MeldTest_Randomized(melds2test, CurrentGear, debug = False)
    #print(s, sets)
    #s, sets = MeldTest_Reslot_Twice(melds2test, CurrentGear, debug = False, reverse = True)
    #print(s, sets)

    #success, slotted = MeldTest([0, 0, 0, 15, 0, 2, 0], CurrentGear)
    #print(success, slotted)

    #Single run
    #BiSON(Onji, [1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1], runSingle = 1)
    #OPTIMIZE!
    #BiSON(Onji, [1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1], runFresh = True)
    BiSON(Onji, [1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1], runFresh = True, runSingle = True)
    #BiSON(Onji, [1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1], runFresh = True, runSingle = True)

    #OPTIMIZE all tanks
    optall = False
    if optall == True:
        print('Optimizing all tanks!')
        Onji.Job = 'GNB'
        BiSON(Onji, [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1], runFresh = 0)
        Onji.Job = 'DRK'
        BiSON(Onji, [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1], runFresh = 0)
        Onji.Job = 'WAR'
        BiSON(Onji, [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1], runFresh = 0)
        Onji.Job = 'PLD'
        BiSON(Onji, [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1], runFresh = 0)












def BiSON(Char, GearList, runSingle = False, runFresh = False):   
    version = '1.10'
    logo(version)

    benchmark = False

    strange_melds = []

    #Check for log file or optimize from start
    runTAG = f"{Char.Name}_{Char.Job}_"
    for testindex in GearList:
        runTAG += str(testindex)

    #Check/Create outputs folder
    Folder = f"Saved Results\\{version}"
    logpath = f"{Folder}\\{runTAG}.txt"
    if not os.path.exists(Folder):
        os.mkdir(Folder)

    #Print log if exists of initialize log file
    if os.path.exists(logpath) and runFresh == False:
        print('Optimization ID found in previous results!')
        print(' ')
        file = open(logpath, 'r')
        lines = file.readlines()
        for line in lines:
            print(line, end="")
        file.close()
        Optimize = False
        bis = None
        bis_melds = None
    else:
        file = open(logpath, 'w')
        Optimize = True


    #Check if to run single gear set or all combinations
    if runSingle == False:
        make_noise = False
        make_lots_of_noise = False
    else:
        make_noise = False
        make_lots_of_noise = False

    if make_noise == True:
        import vlc 
        scifi1 = vlc.MediaPlayer('Scifi1.mp3')
        scifi3 = vlc.MediaPlayer('Scifi3.mp3')
        scifi4 = vlc.MediaPlayer('Scifi4.mp3')
        Volume = 70
        scifi1.audio_set_volume(Volume)
        scifi3.audio_set_volume(Volume)
        scifi4.audio_set_volume(Volume)
        scifi1.play()
    
    #Generate all combinations of input scope
    def GenerateCombinations(scope, floorLim):
        srange = []
        for k in scope:
            srange.append(list(range(floorLim, k + 1)))
        Combinations = list(itertools.product(*srange))
        return Combinations


    if Optimize == True:
        penalty = 0 #Number to keep track of performance

        #Variables for performance testing
        s1 = 0
        s2 = 0
        s3 = 0
        s4 = 0
        s5 = 0
        m1 = []
        m2 = [0, 0, 0]


        #Generate all possible gear combinations
        print(f"Job: {Char.Job}")
        print("Generating gear combinations...")
        if runSingle == True:
            AllGearCombinations = [tuple(GearList)]
            print(f"Single gearset enabled. Optimizing melds and food only")
        else:
            AllGearCombinations = GenerateCombinations(GearList, 1)
            print(f"{len(AllGearCombinations)} gear combinations generated.")
        print(" ")
        print("Initializing...")

        #Placeholders for the results
        bis = type('empty', (object,), {})()
        bis_melds = []
        init = True
        Starting_Time = time.time()
        Number_of_sets = len(AllGearCombinations)
        divcheck = 70
        loadcheck = int(Number_of_sets / divcheck)

        #Loop through all gear combinations
        for X, gset in enumerate(AllGearCombinations):        #Gearset loop (OUTER)

            #Time estimation
            if X == 10:
                Current_Time = time.time()
                Elapsed_Time = Current_Time - Starting_Time
                Completed_Sets = float(X)
                Time_per_set = Elapsed_Time / Completed_Sets
                Sets_left = Number_of_sets - Completed_Sets
                time_left = Sets_left * Time_per_set

                hours_left = math.floor(time_left / (60 * 60))
                seconds_left = time_left - hours_left * 60 * 60
                minutes_left = math.floor(seconds_left / 60)
                seconds_left = math.floor(seconds_left) - minutes_left * 60
                print(f"Estimated calculation time: {str(hours_left).zfill(2)}:{str(minutes_left).zfill(2)}:{str(seconds_left).zfill(2)}  (hh:mm:ss)")
                print("_"*(divcheck + 3))

                if make_lots_of_noise == True:
                    scifi1.stop()
                    scifi4.play()

            if (X > 10 and not X % max(1, loadcheck)) or X == 11:
                stdout.write("=")
                stdout.flush()

            if X == len(AllGearCombinations) - 10 and make_noise == True:
                scifi4.stop()
                scifi3.play()

            GearSet = Gearset_Fending(Char.Job, *gset)
            AllowedMeldList = GearSet.AllowedMelds
            SlotSum = sum(GearSet.TotalMelds)

            #Calculate all stat combinations from melds
            Allowance = [0, 0, 0, 0, 0, 0, 0]
            for dict_i in AllowedMeldList:
                Allowance = [a + b for a, b in zip(list(dict_i.values()), Allowance)]

            #Generate all possibly feasable meld combinations
            AllMeldCombinations = GenerateCombinations(Allowance, 0)

            #Filter out invalid meld combinations
            ValidMeldCombinations = []
            GearMeldRef = []
            statCombinations = []
            for Mld in AllMeldCombinations:
                Melds_comb = list(Mld)
                Meld_Sum = sum(Melds_comb)
                m2[0] += 1


                #Check if all slots are used
                if Meld_Sum == SlotSum:
                    m2[1] += 1

                    #Check if melds are possible with gearset
                    if benchmark == True:
                        t00 = time.time()
                    success, Slotted_melds  = MeldTest_Reslot_Twice(Melds_comb, GearSet)
                    if benchmark == True:
                        t01 = time.time()

                    if benchmark == True:
                        #Comparisons with other algorithms (benchmarking)
                        t1 = time.time()
                        success1, Slotted_melds1 = MeldTest_Randomized(Melds_comb, GearSet)
                        t2 = time.time()
                        success2, Slotted_melds2 = MeldTest_Reslot_2(Melds_comb, GearSet, cycle = True, reverse = True)
                        t3 = time.time()
                        success3, Slotted_melds3 = MeldTest_Reslot(Melds_comb, GearSet, reverse = False)
                        t4 = time.time()
                        success4, Slotted_melds4 = MeldTest_Reslot(Melds_comb, GearSet, reverse = True, cycle = True)
                        t5 = time.time()
                        success5, Slotted_melds5 = MeldTest_Reslot_Rand(Melds_comb, GearSet, reverse = False, cycle = False)
                        t6 = time.time()


                        if success == True:
                            penalty += 1
                        if success1 == True:
                            s1 += 1
                        if success2 == True:
                            s2 += 1
                        if success3 == True:
                            s3 += 1
                        if success4 == True:
                            s4 += 1
                        if success5 == True:
                            s5 += 1
                            if success == False:
                                m1.append(Slotted_melds5)


                    #Try alternative settings if fail
                    #if success == False:
                    #    penalty += 1
                    #    success, Slotted_melds = MeldTest_Reslot(Melds_comb, GearSet, reverse = True)
                    #    if success == False:
                    #        success, Slotted_melds = MeldTest_Reslot(Melds_comb, GearSet, cycle = True)
                    #        penalty += 1

                    
                    if success == True and Melds_comb not in ValidMeldCombinations:
                        ValidMeldCombinations.append(Melds_comb)
                        GearMeldRef.append(Slotted_melds)

                    
            m2[2] = len(ValidMeldCombinations)
            if init == True:
                print(f"(Approximately {len(ValidMeldCombinations)} valid meld combinations per gearset)")

            for idx, mset in enumerate(ValidMeldCombinations):     #Meld loop (MIDDLE)
                Meld_obj = Melds(*mset)

                for meal in range(1, 7):                            #Food loop (INNER)

                    #6 kinds of food to check
                    Food_Obj = Food(meal)

                    #Equip and check dps, save bis for each GCD tier
                    Equipped = Equip(Char, GearSet, Meld_obj, Food_Obj)
                    if init == True:
                        bis = {str(Equipped.GCD) : copy.deepcopy(Equipped)}
                        bis_melds = {str(Equipped.GCD) : copy.deepcopy(GearMeldRef[idx])}
                        init = False
                    elif not str(Equipped.GCD) in bis.keys():
                        bis.update({str(Equipped.GCD) : copy.deepcopy(Equipped)})
                        bis_melds.update({str(Equipped.GCD) : copy.deepcopy(GearMeldRef[idx])})
                    else:
                        #f_avg_new = Equipped.dps
                        #f_avg_old = bis[str(Equipped.GCD)].dps

                        f_avg_new = Equipped.dps_rating
                        f_avg_old = bis[str(Equipped.GCD)].dps_rating


                        if f_avg_new > f_avg_old:
                            bis.update({str(Equipped.GCD) : copy.deepcopy(Equipped)})
                            bis_melds.update({str(Equipped.GCD) : copy.deepcopy(GearMeldRef[idx])})

        #print results
        print(' ')
        print('Optimization Completed!')    
        print(' ')

        keyz = list(bis.keys())
        keyz.sort()

        top = []
        maxlist = []
        for gcd in keyz:
            top.append(bis[gcd].dps)
            maxlist.append(' ')
        idx_max = top.index(max(top))
        idx_min = top.index(min(top))
        maxlist[idx_max] = '  <- Highest'
        maxlist[idx_min] = '  <- Lowest'

        print('_'*27 + 'GCD Tiers' + '_'*27)      
        print(f"{'GCD:':<10}{'Estimated DPS:':>15}")

        file.write('_'*27 + 'GCD Tiers' + '_'*27 + '\n')
        file.write(f"{'GCD:':<10}{'Estimated DPS:':>15} \n")

        for idx, gcd in enumerate(keyz):
            print(f"{gcd:<10}{bis[gcd].dps:>15}{maxlist[idx]:10}")
            file.write(f"{gcd:<10}{bis[gcd].dps:>15}{maxlist[idx]:10} \n")

        print('_'*64)        
        print(' ')

        file.write('_'*64 + '\n')
        file.write(' \n')

        for gcd in keyz:
            bis[gcd].show()    
            bis[gcd].show(file)   
            print(f"{'Gear:':51}{'Melds:':20}")
            file.write(f"{'Gear:':51}{'Melds:':20} \n")

            for k, b in zip(bis[gcd].Gear.Gearslot.__dict__.values(), bis_melds[gcd]):
                print(f"{k:50} {b}")
                file.write(f"{k:50} {b} \n")

            print(' ')
            print(' -' * 64)
            print(' ')

            file.write(' \n')
            file.write(' -' * 64 + '\n')
            file.write(' \n')

        if make_noise == True:
            scifi3.stop()

            file.close()

        if benchmark == True:
            print(' ')
            print(f"Baseline: {penalty} time to complete: {t01-t00}")
            print(f"s1: {s1} time to complete: {t2-t1}")
            print(f"s2: {s2} time to complete: {t3-t2}")
            print(f"s3: {s3} time to complete: {t4-t3}")
            print(f"s4: {s4} time to complete: {t5-t4}")
            print(f"s5: {s5} time to complete: {t6-t5}")
            print(' ')
            print('Memory slots')
            for mm in m1:
                print(mm)

            print(f"Max number of reslots yielding true {max(m2)}")
            print(f"Average {sum(m2)/len(m2)}")

        #print(m2)

    return bis, bis_melds




def logo(version):
    print(r"                                                 _.-````'-,_")
    print(r"                                       _,.,_ ,-'`           `'-.,_")
    print(r"                                     /}     {\                   '``-.")
    print(r"                                    ({      } }                      `\ ")
    print(r"                                     \)    {_/                        }\ ")
    print(r"                                     \|       /}           '    ,'    / \ ")
    print(r"                                      `\    ^'            '     {    /  }} ")
    print(r"██████╗░██╗░██████╗░█████╗░███╗░░██╗    \|      _/\ ,     /    ,,`\   {   ")
    print(r"██╔══██╗██║██╔════╝██╔══██╗████╗░██║     \,   \|  \  \  \| ````\| / \_ \ ")
    print(r"██████╦╝██║╚█████╗░██║░░██║██╔██╗██║       `}_/    \  \ \|     { >   {  > ")
    print(r"██╔══██╗██║░╚═══██╗██║░░██║██║╚████║                \( \(      \|/   \|/ ")
    print(r"██████╦╝██║██████╔╝╚█████╔╝██║░╚███║"+ f"{'V' + version:^12}" + r"    /_(/_(     /_{  /_{ ")
    print(" ")
    print(" ")



if __name__ == "__main__":
    Main()
















