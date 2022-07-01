import itertools
import copy
import time
import math
import os
import random
from sys import stdout






def Main():
    print('Compile ok')




def MeldTest_Reslot_Twice(Melds_to_meld_in, GearSet, debug = False, reverse = False, cycle = False, shuffle = False):
    printtrig = 1
    reslots = 0

    Melds_to_meld = copy.deepcopy(Melds_to_meld_in)

    #If both these lists/dictionaries have space for a meld it is allowed
    Success = True
    Total_Slots_Left = copy.deepcopy(GearSet.TotalMelds)
    Stat_Slots_Left = copy.deepcopy(GearSet.AllowedMelds)
    Slotted_Melds = [[],[],[],[],[],[],[],[],[],[],[]]
    check_summa = 0
    summa = sum(Melds_to_meld)

    if debug == True:
        print('Total stat slots in gearset')
        for kr in Stat_Slots_Left:
            print(kr)



    #Create list that cycles through the stats until all melds have been listed
    worklist = []

    if cycle == True:
        while sum(Melds_to_meld) > 0:
            i = 0
            for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
                if meldtype > 0:
                    Melds_to_meld[i] -= 1
                    worklist.append(statName)
                i += 1
    else:
        for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
            if meldtype > 0:
                for _ in range(meldtype):
                    worklist.append(statName)
        worklist.sort()


    if reverse == True:    
        worklist.reverse()

    if shuffle == True:
        random.shuffle(worklist)

    if debug == True:
        print(worklist, len(worklist))

    Stats_in_use = list(set(worklist))

    secondary_sub_allowed = True
    secondary_sub_history = []
    impossible = False
    while len(worklist) > 0 and impossible == False:
        
        stat_name = worklist.pop(0)
        idx2gear = list(range(0,11)) #1:1 list here

        possible_substat = []
        possible_subgear = []
        
        use_affinity = True
        if use_affinity == True:
            StatAffinity_inverse = []

            for aff_gear, meldslots_gear in zip(GearSet.Affinity, GearSet.AllowedMelds):

                Meldslots_inverse = 0
                for stype in Stats_in_use:
                    if not stype == stat_name:
                        Meldslots_inverse += meldslots_gear[stype]

                StatAffinity_inverse.append(Meldslots_inverse)

            if debug == 1 and printtrig == 1:
                print(stat_name)
                print(Stats_in_use)
                for mm, kk in zip(StatAffinity_inverse, GearSet.AllowedMelds):
                    print(mm, '    ',kk)
                printtrig = 0

            #Sort meld priority list for gear after the affinity listStatAffinity_inverse
            StatAffinity, idx2gear = (list(t) for t in zip(*sorted(zip(StatAffinity_inverse, idx2gear))))  
            #idx2gear.reverse()


        trying_to_meld = True
        idx = 0        
        while trying_to_meld == True:

            #Translate idx to gear index 
            gear_index = idx2gear[idx]

            if Total_Slots_Left[gear_index] > 0:
                if Stat_Slots_Left[gear_index][stat_name] > 0:
                    #Meld gear sucessfully

                    check_summa += 1
                    #Subtract from available slots
                    Total_Slots_Left[gear_index] = Total_Slots_Left[gear_index] - 1
                    Stat_Slots_Left[gear_index][stat_name] = Stat_Slots_Left[gear_index][stat_name] - 1
                    trying_to_meld = False                            
                    Slotted_Melds[gear_index].append(stat_name)                       
                    
            idx += 1
            if idx > 10 and trying_to_meld == True: #No gear can accept the meld, try reslotting
                if debug == True:
                    print(f'Unable to slot {stat_name}-materia. Trying to look for substitute slot position.')
                trying_to_remeld = True
                
                idx_sub = 0
                while trying_to_remeld == True:
                    gear_index_sub = idx_sub

                    if debug == True:
                        print(f"Checking if gear index {gear_index_sub} can meld {stat_name}:    {Stat_Slots_Left[gear_index_sub]}   {Slotted_Melds[gear_index_sub]}")

                    if Stat_Slots_Left[gear_index_sub][stat_name] > 0: #Can already fully melded gear accept the stat?                        

                        for meld_sub in Slotted_Melds[gear_index_sub]:

                            if not meld_sub == stat_name:
                                possible_subgear.append(gear_index_sub)
                                possible_substat.append(meld_sub)

                            if debug == True:
                                print(f"Checking gear index {gear_index_sub} for swapping {meld_sub}")

                            trying_to_meld_sub = True
                            idx_sub_meld = 0        
                            while trying_to_meld_sub == True:
                                gear_index_sub_meld = idx2gear[idx_sub_meld]

                                if Total_Slots_Left[gear_index_sub_meld] > 0:
                                    if Stat_Slots_Left[gear_index_sub_meld][meld_sub] > 0:
 
                                        if debug == True:
                                            print(f"Trying to meld: {stat_name}")
                                            print(f"Worklist left {worklist}")
                                            print(' ')
                                            print(f"Replace {meld_sub} with {stat_name} at index {gear_index_sub}")
                                            print(f"Move {meld_sub} from {gear_index_sub} to {gear_index_sub_meld}")
                                            print(Slotted_Melds)
                                            for yy in Stat_Slots_Left:
                                                print(yy)
                                            print(' ')

                                        #Remove sub meld from sub gear
                                        Slotted_Melds[gear_index_sub].pop(Slotted_Melds[gear_index_sub].index(meld_sub))                                          
                                        Stat_Slots_Left[gear_index_sub][meld_sub] = Stat_Slots_Left[gear_index_sub][meld_sub] + 1

                                        #Slot new meld into sub gear
                                        Slotted_Melds[gear_index_sub].append(stat_name)   
                                        Stat_Slots_Left[gear_index_sub][stat_name] = Stat_Slots_Left[gear_index_sub][stat_name] - 1

                                        #Meld substitute successfully into other gear
                                        Total_Slots_Left[gear_index_sub_meld] = Total_Slots_Left[gear_index_sub_meld] - 1
                                        Stat_Slots_Left[gear_index_sub_meld][meld_sub] = Stat_Slots_Left[gear_index_sub_meld][meld_sub] - 1
                                        Slotted_Melds[gear_index_sub_meld].append(meld_sub)   

                                        if debug == True:
                                            print(Slotted_Melds)
                                            for yy in Stat_Slots_Left:
                                                print(yy)

                                        trying_to_meld = False
                                        trying_to_remeld = False  
                                        trying_to_meld_sub = False
                                        check_summa += 1                                                            

                                idx_sub_meld += 1
                                if idx_sub_meld > 10: #This loop is looking for a place to move the materia that is blocking. 
                                    trying_to_meld_sub = False

                    idx_sub += 1 #This loop is looking for a gearslot that can accept the stat.                 
                    if idx_sub > 10 and trying_to_remeld == True and secondary_sub_allowed == True:
                    #If no place to move sub materia force the slot and pop sub back into worklist.

                    #Look at the possible subs and gearslots and remove the least used materia

                        #Remove materia type trying to be melded from sub suggestions
                        while stat_name in possible_substat:
                            possible_substat.pop(possible_substat.index(stat_name))
                            possible_subgear.pop(possible_substat.index(stat_name))

                        if debug == True:
                            print('Possible sub gear:', possible_subgear)
                            print('Possible meld stats:', possible_substat)

                        #Sort possible sub lists to put the least used sub stat first
                        possible_substat, possible_subgear = (list(t) for t in zip(*sorted(zip(possible_substat, possible_subgear))))  
                        possible_substat.reverse()
                        possible_subgear.reverse()

                        #Pick the first element and pop it back to the worklist
                        gear_index_sub = possible_subgear[0]
                        meld_sub = possible_substat[0]

                        if debug == True:
                            print(f'Remove {meld_sub} from {gear_index_sub} and send back to worklist.')

                        #Remove sub meld from sub gear
                        Slotted_Melds[gear_index_sub].pop(Slotted_Melds[gear_index_sub].index(meld_sub))                                          
                        Stat_Slots_Left[gear_index_sub][meld_sub] = Stat_Slots_Left[gear_index_sub][meld_sub] + 1

                        #Slot new meld into sub gear
                        Slotted_Melds[gear_index_sub].append(stat_name)   
                        Stat_Slots_Left[gear_index_sub][stat_name] = Stat_Slots_Left[gear_index_sub][stat_name] - 1

                        #Meld substitute successfully into other gear
                        worklist.insert(0, meld_sub)

                        secondary_sub_history.append(meld_sub)
                        reslots = len(secondary_sub_history)
                        if debug == True:
                            print('Pop to worklist history: ',secondary_sub_history)

                        trying_to_meld = False
                        trying_to_remeld = False  
                        trying_to_meld_sub = False


                    elif idx_sub > 10 and trying_to_remeld == True:
                        trying_to_remeld = False
                        trying_to_meld = False
                        impossible = True
                        Success = False                     

                    if debug == True:
                        print(worklist)

                    #If all stat types have been popped to worklist the materia combination does not work
                    if set(Stats_in_use) == set(secondary_sub_history) or len(secondary_sub_history) > 5:
                        trying_to_remeld = False
                        trying_to_meld = False
                        impossible = True
                        Success = False  



    if not summa == check_summa:
        Success = False
  
        
    return Success, Slotted_Melds#, reslots

















#This one works best at the moment (v1.04) it is not efficient since it tries multiple times to avoid
#deadlock of materia. Randomization of meld order when deadlock.
def MeldTest_Reslot_Rand(Melds_to_meld_in, GearSet, debug = False, reverse = False, cycle = False):
    shuffle = True
    tries_left = 10
    while tries_left > 0:
        #print(tries_left)
        #time.sleep(0.1)

        printtrig = 1

        Melds_to_meld = copy.deepcopy(Melds_to_meld_in)

        #If both these lists/dictionaries have space for a meld it is allowed
        Success = True
        Total_Slots_Left = copy.deepcopy(GearSet.TotalMelds)
        Stat_Slots_Left = copy.deepcopy(GearSet.AllowedMelds)
        Slotted_Melds = [[],[],[],[],[],[],[],[],[],[],[]]
        check_summa = 0
        summa = sum(Melds_to_meld)

        if debug == True:
            print('Total stat slots in gearset')
            for kr in Stat_Slots_Left:
                print(kr)



        #Create list that cycles through the stats until all melds have been listed
        worklist = []

        if cycle == True:
            while sum(Melds_to_meld) > 0:
                i = 0
                for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
                    if meldtype > 0:
                        Melds_to_meld[i] -= 1
                        worklist.append(statName)
                    i += 1
        else:
            for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
                if meldtype > 0:
                    for _ in range(meldtype):
                        worklist.append(statName)
            worklist.sort()


        if reverse == True:    
            worklist.reverse()

        if shuffle == True:
            random.shuffle(worklist)

        if debug == True:
            print(worklist, len(worklist))

        Stats_in_use = list(set(worklist))

        impossible = False
        while len(worklist) > 0 and impossible == False:
            
            stat_name = worklist.pop(0)
            idx2gear = list(range(0,11)) #1:1 list here

            use_affinity = True
            if use_affinity == True:
                StatAffinity_inverse = []

                for aff_gear, meldslots_gear in zip(GearSet.Affinity, GearSet.AllowedMelds):

                    Meldslots_inverse = 0
                    for stype in Stats_in_use:
                        if not stype == stat_name:
                            Meldslots_inverse += meldslots_gear[stype]

                    StatAffinity_inverse.append(Meldslots_inverse)

                if debug == 1 and printtrig == 1:
                    print(stat_name)
                    print(Stats_in_use)
                    for mm, kk in zip(StatAffinity_inverse, GearSet.AllowedMelds):
                        print(mm, '    ',kk)
                    printtrig = 0

                #Sort meld priority list for gear after the affinity listStatAffinity_inverse
                StatAffinity, idx2gear = (list(t) for t in zip(*sorted(zip(StatAffinity_inverse, idx2gear))))  
                idx2gear = list(range(0,11)) #1:1 list here to bypass sorting




            trying_to_meld = True
            idx = 0        
            while trying_to_meld == True:

                #Translate idx to gear index 
                gear_index = idx2gear[idx]

                if Total_Slots_Left[gear_index] > 0:
                    if Stat_Slots_Left[gear_index][stat_name] > 0:
                        #Meld gear sucessfully

                        check_summa += 1
                        #Subtract from available slots
                        Total_Slots_Left[gear_index] = Total_Slots_Left[gear_index] - 1
                        Stat_Slots_Left[gear_index][stat_name] = Stat_Slots_Left[gear_index][stat_name] - 1
                        trying_to_meld = False                            
                        Slotted_Melds[gear_index].append(stat_name)                       
                        
                idx += 1
                if idx > 10 and trying_to_meld == True: #No gear can accept the meld, try reslotting
                    if debug == True:
                        print(f'Unable to slot {stat_name}-materia. Trying to look for substitute slot position.')
                    trying_to_remeld = True
                    
                    idx_sub = 0
                    while trying_to_remeld == True:
                        gear_index_sub = idx_sub

                        if debug == True:
                            print(f"Checking if gear index {gear_index_sub} can meld {stat_name}:    {Stat_Slots_Left[gear_index_sub]}   {Slotted_Melds[gear_index_sub]}")

                        if Stat_Slots_Left[gear_index_sub][stat_name] > 0: #Can already fully melded gear accept the stat?
                            for meld_sub in Slotted_Melds[gear_index_sub]:

                                if debug == True:
                                    print(f"Checking gear index {gear_index_sub} for swapping {meld_sub}")

                                trying_to_meld_sub = True
                                idx_sub_meld = 0        
                                while trying_to_meld_sub == True:
                                    gear_index_sub_meld = idx2gear[idx_sub_meld]

                                    if Total_Slots_Left[gear_index_sub_meld] > 0:
                                        if Stat_Slots_Left[gear_index_sub_meld][meld_sub] > 0:

                                            if debug == True:
                                                print(f"Trying to meld: {stat_name}")
                                                print(f"Worklist left {worklist}")
                                                print(' ')
                                                print(f"Replace {meld_sub} with {stat_name} at index {gear_index_sub}")
                                                print(f"Move {meld_sub} from {gear_index_sub} to {gear_index_sub_meld}")
                                                print(Slotted_Melds)
                                                for yy in Stat_Slots_Left:
                                                    print(yy)
                                                print(' ')

                                            #Remove sub meld from sub gear
                                            Slotted_Melds[gear_index_sub].pop(Slotted_Melds[gear_index_sub].index(meld_sub))                                          
                                            Stat_Slots_Left[gear_index_sub][meld_sub] = Stat_Slots_Left[gear_index_sub][meld_sub] + 1

                                            #Slot new meld into sub gear
                                            Slotted_Melds[gear_index_sub].append(stat_name)   
                                            Stat_Slots_Left[gear_index_sub][stat_name] = Stat_Slots_Left[gear_index_sub][stat_name] - 1

                                            #Meld substitute successfully into other gear
                                            Total_Slots_Left[gear_index_sub_meld] = Total_Slots_Left[gear_index_sub_meld] - 1
                                            Stat_Slots_Left[gear_index_sub_meld][meld_sub] = Stat_Slots_Left[gear_index_sub_meld][meld_sub] - 1
                                            Slotted_Melds[gear_index_sub_meld].append(meld_sub)   

                                            if debug == True:
                                                print(Slotted_Melds)
                                                for yy in Stat_Slots_Left:
                                                    print(yy)

                                            trying_to_meld = False
                                            trying_to_remeld = False  
                                            trying_to_meld_sub = False
                                            check_summa += 1                                                            

                                    idx_sub_meld += 1
                                    if idx_sub_meld > 10:
                                        trying_to_meld_sub = False

                        idx_sub += 1                  
                        if idx_sub > 10 and trying_to_remeld == True: #Reslotting not possible = melds are not possible.
                            trying_to_remeld = False
                            trying_to_meld = False
                            impossible = True
                            Success = False                     


        if not summa == check_summa:
            Success = False
      
        if Success == False:
            tries_left -= 1

        if Success == True:
            tries_left = 0
    return Success, Slotted_Melds















def MeldTest_Reslot_2(Melds_to_meld_in, GearSet, debug = False, reverse = False, cycle = False, shuffle = False):
    printtrig = 1

    Melds_to_meld = copy.deepcopy(Melds_to_meld_in)

    #If both these lists/dictionaries have space for a meld it is allowed
    Success = True
    Total_Slots_Left = copy.deepcopy(GearSet.TotalMelds)
    Stat_Slots_Left = copy.deepcopy(GearSet.AllowedMelds)
    Slotted_Melds = [[],[],[],[],[],[],[],[],[],[],[]]
    check_summa = 0
    summa = sum(Melds_to_meld)

    if debug == True:
        print('Total stat slots in gearset')
        for kr in Stat_Slots_Left:
            print(kr)



    #Create list that cycles through the stats until all melds have been listed
    worklist = []

    if cycle == True:
        while sum(Melds_to_meld) > 0:
            i = 0
            for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
                if meldtype > 0:
                    Melds_to_meld[i] -= 1
                    worklist.append(statName)
                i += 1
    else:
        for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
            if meldtype > 0:
                for _ in range(meldtype):
                    worklist.append(statName)
        worklist.sort()


    if reverse == True:    
        worklist.reverse()

    if shuffle == True:
        random.shuffle(worklist)

    if debug == True:
        print(worklist, len(worklist))

    Stats_in_use = list(set(worklist))

    impossible = False
    while len(worklist) > 0 and impossible == False:
        
        stat_name = worklist.pop(0)
        idx2gear = list(range(0,11)) #1:1 list here

        use_affinity = True
        if use_affinity == True:
            StatAffinity_inverse = []

            for aff_gear, meldslots_gear in zip(GearSet.Affinity, GearSet.AllowedMelds):

                Meldslots_inverse = 0
                for stype in Stats_in_use:
                    if not stype == stat_name:
                        Meldslots_inverse += meldslots_gear[stype]

                StatAffinity_inverse.append(Meldslots_inverse)

            if debug == 1 and printtrig == 1:
                print(stat_name)
                print(Stats_in_use)
                for mm, kk in zip(StatAffinity_inverse, GearSet.AllowedMelds):
                    print(mm, '    ',kk)
                printtrig = 0

            #Sort meld priority list for gear after the affinity listStatAffinity_inverse
            StatAffinity, idx2gear = (list(t) for t in zip(*sorted(zip(StatAffinity_inverse, idx2gear))))  
            #idx2gear.reverse()


        trying_to_meld = True
        idx = 0        
        while trying_to_meld == True:

            #Translate idx to gear index 
            gear_index = idx2gear[idx]

            if Total_Slots_Left[gear_index] > 0:
                if Stat_Slots_Left[gear_index][stat_name] > 0:
                    #Meld gear sucessfully

                    check_summa += 1
                    #Subtract from available slots
                    Total_Slots_Left[gear_index] = Total_Slots_Left[gear_index] - 1
                    Stat_Slots_Left[gear_index][stat_name] = Stat_Slots_Left[gear_index][stat_name] - 1
                    trying_to_meld = False                            
                    Slotted_Melds[gear_index].append(stat_name)                       
                    
            idx += 1
            if idx > 10 and trying_to_meld == True: #No gear can accept the meld, try reslotting
                if debug == True:
                    print(f'Unable to slot {stat_name}-materia. Trying to look for substitute slot position.')
                trying_to_remeld = True
                
                idx_sub = 0
                while trying_to_remeld == True:
                    gear_index_sub = idx_sub

                    if debug == True:
                        print(f"Checking if gear index {gear_index_sub} can meld {stat_name}:    {Stat_Slots_Left[gear_index_sub]}   {Slotted_Melds[gear_index_sub]}")

                    if Stat_Slots_Left[gear_index_sub][stat_name] > 0: #Can already fully melded gear accept the stat?
                        for meld_sub in Slotted_Melds[gear_index_sub]:

                            if debug == True:
                                print(f"Checking gear index {gear_index_sub} for swapping {meld_sub}")

                            trying_to_meld_sub = True
                            idx_sub_meld = 0        
                            while trying_to_meld_sub == True:
                                gear_index_sub_meld = idx2gear[idx_sub_meld]

                                if Total_Slots_Left[gear_index_sub_meld] > 0:
                                    if Stat_Slots_Left[gear_index_sub_meld][meld_sub] > 0:

                                        if debug == True:
                                            print(f"Trying to meld: {stat_name}")
                                            print(f"Worklist left {worklist}")
                                            print(' ')
                                            print(f"Replace {meld_sub} with {stat_name} at index {gear_index_sub}")
                                            print(f"Move {meld_sub} from {gear_index_sub} to {gear_index_sub_meld}")
                                            print(Slotted_Melds)
                                            for yy in Stat_Slots_Left:
                                                print(yy)
                                            print(' ')

                                        #Remove sub meld from sub gear
                                        Slotted_Melds[gear_index_sub].pop(Slotted_Melds[gear_index_sub].index(meld_sub))                                          
                                        Stat_Slots_Left[gear_index_sub][meld_sub] = Stat_Slots_Left[gear_index_sub][meld_sub] + 1

                                        #Slot new meld into sub gear
                                        Slotted_Melds[gear_index_sub].append(stat_name)   
                                        Stat_Slots_Left[gear_index_sub][stat_name] = Stat_Slots_Left[gear_index_sub][stat_name] - 1

                                        #Meld substitute successfully into other gear
                                        Total_Slots_Left[gear_index_sub_meld] = Total_Slots_Left[gear_index_sub_meld] - 1
                                        Stat_Slots_Left[gear_index_sub_meld][meld_sub] = Stat_Slots_Left[gear_index_sub_meld][meld_sub] - 1
                                        Slotted_Melds[gear_index_sub_meld].append(meld_sub)   

                                        if debug == True:
                                            print(Slotted_Melds)
                                            for yy in Stat_Slots_Left:
                                                print(yy)

                                        trying_to_meld = False
                                        trying_to_remeld = False  
                                        trying_to_meld_sub = False
                                        check_summa += 1                                                            

                                idx_sub_meld += 1
                                if idx_sub_meld > 10:
                                    trying_to_meld_sub = False

                    idx_sub += 1                  
                    if idx_sub > 10 and trying_to_remeld == True: #Reslotting not possible = melds are not possible.
                        trying_to_remeld = False
                        trying_to_meld = False
                        impossible = True
                        Success = False                     


    if not summa == check_summa:
        Success = False
  

    return Success, Slotted_Melds












def MeldTest_Reslot(Melds_to_meld_in, GearSet, debug = False, reverse = False, cycle = False):
    printtrig = 0

    Melds_to_meld = copy.deepcopy(Melds_to_meld_in)

    #If both these lists/dictionaries have space for a meld it is allowed
    Success = True
    Total_Slots_Left = copy.deepcopy(GearSet.TotalMelds)
    Stat_Slots_Left = copy.deepcopy(GearSet.AllowedMelds)
    Slotted_Melds = [[],[],[],[],[],[],[],[],[],[],[]]
    check_summa = 0
    summa = sum(Melds_to_meld)

    if debug == True:
        print('Total stat slots in gearset')
        for kr in Stat_Slots_Left:
            print(kr)



    #Create list that cycles through the stats until all melds have been listed
    worklist = []

    if cycle == True:
        while sum(Melds_to_meld) > 0:
            i = 0
            for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
                if meldtype > 0:
                    Melds_to_meld[i] -= 1
                    worklist.append(statName)
                i += 1
    else:
        for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
            if meldtype > 0:
                for _ in range(meldtype):
                    worklist.append(statName)
        worklist.sort()


    if reverse == True:    
        worklist.reverse()

    if debug == True:
        print(worklist, len(worklist))

    impossible = False
    while len(worklist) > 0 and impossible == False:
        
        stat_name = worklist.pop(0)
        idx2gear = list(range(0,11)) #1:1 list here

        trying_to_meld = True
        idx = 0        
        while trying_to_meld == True:

            #Translate idx to gear index 
            gear_index = idx2gear[idx]

            if Total_Slots_Left[gear_index] > 0:
                if Stat_Slots_Left[gear_index][stat_name] > 0:
                    #Meld gear sucessfully

                    check_summa += 1
                    #Subtract from available slots
                    Total_Slots_Left[gear_index] = Total_Slots_Left[gear_index] - 1
                    Stat_Slots_Left[gear_index][stat_name] = Stat_Slots_Left[gear_index][stat_name] - 1
                    trying_to_meld = False                            
                    Slotted_Melds[gear_index].append(stat_name)                       
                    
            idx += 1
            if idx > 10 and trying_to_meld == True: #No gear can accept the meld, try reslotting
                if debug == True:
                    print(f'Unable to slot {stat_name}-materia. Trying to look for substitute slot position.')
                trying_to_remeld = True
                
                idx_sub = 0
                while trying_to_remeld == True:
                    gear_index_sub = idx_sub

                    if debug == True:
                        print(f"Checking if gear index {gear_index_sub} can meld {stat_name}:    {Stat_Slots_Left[gear_index_sub]}   {Slotted_Melds[gear_index_sub]}")

                    if Stat_Slots_Left[gear_index_sub][stat_name] > 0: #Can already fully melded gear accept the stat?
                        for meld_sub in Slotted_Melds[gear_index_sub]:

                            if debug == True:
                                print(f"Checking gear index {gear_index_sub} for swapping {meld_sub}")

                            trying_to_meld_sub = True
                            idx_sub_meld = 0        
                            while trying_to_meld_sub == True:
                                gear_index_sub_meld = idx2gear[idx_sub_meld]

                                if Total_Slots_Left[gear_index_sub_meld] > 0:
                                    if Stat_Slots_Left[gear_index_sub_meld][meld_sub] > 0:

                                        if debug == True:
                                            print(f"Trying to meld: {stat_name}")
                                            print(f"Worklist left {worklist}")
                                            print(' ')
                                            print(f"Replace {meld_sub} with {stat_name} at index {gear_index_sub}")
                                            print(f"Move {meld_sub} from {gear_index_sub} to {gear_index_sub_meld}")
                                            print(Slotted_Melds)
                                            for yy in Stat_Slots_Left:
                                                print(yy)
                                            print(' ')

                                        #Remove sub meld from sub gear
                                        Slotted_Melds[gear_index_sub].pop(Slotted_Melds[gear_index_sub].index(meld_sub))                                          
                                        Stat_Slots_Left[gear_index_sub][meld_sub] = Stat_Slots_Left[gear_index_sub][meld_sub] + 1

                                        #Slot new meld into sub gear
                                        Slotted_Melds[gear_index_sub].append(stat_name)   
                                        Stat_Slots_Left[gear_index_sub][stat_name] = Stat_Slots_Left[gear_index_sub][stat_name] - 1

                                        #Meld substitute successfully into other gear
                                        Total_Slots_Left[gear_index_sub_meld] = Total_Slots_Left[gear_index_sub_meld] - 1
                                        Stat_Slots_Left[gear_index_sub_meld][meld_sub] = Stat_Slots_Left[gear_index_sub_meld][meld_sub] - 1
                                        Slotted_Melds[gear_index_sub_meld].append(meld_sub)   

                                        if debug == True:
                                            print(Slotted_Melds)
                                            for yy in Stat_Slots_Left:
                                                print(yy)

                                        trying_to_meld = False
                                        trying_to_remeld = False  
                                        trying_to_meld_sub = False
                                        check_summa += 1                                                            

                                idx_sub_meld += 1
                                if idx_sub_meld > 10:
                                    trying_to_meld_sub = False

                    idx_sub += 1                  
                    if idx_sub > 10 and trying_to_remeld == True: #Reslotting not possible = melds are not possible.
                        trying_to_remeld = False
                        trying_to_meld = False
                        impossible = True
                        Success = False                     


    if not summa == check_summa:
        Success = False
  

    return Success, Slotted_Melds
















def MeldTest_Cycle_Affinity(Melds_to_meld_in, GearSet, debug = False, reverse = False):
    printtrig = 0

    Melds_to_meld = copy.deepcopy(Melds_to_meld_in)

    #If both these lists/dictionaries have space for a meld it is allowed
    Success = True
    Total_Slots_Left = copy.deepcopy(GearSet.TotalMelds)
    Stat_Slots_Left = copy.deepcopy(GearSet.AllowedMelds)
    Slotted_Melds = [[],[],[],[],[],[],[],[],[],[],[]]
    check_summa = 0
    summa = sum(Melds_to_meld)

    #Create list that cycles through the stats until all melds have been listed
    worklist = []
    while sum(Melds_to_meld) > 0:
        i = 0
        for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
            if meldtype > 0:
                Melds_to_meld[i] -= 1
                worklist.append(statName)
            i += 1
    if reverse == True:
        worklist.reverse()

    #Calculate which gearpiece to prioritize first for the stat thats is being melded
    Stats_in_use = list(set(worklist))

    for stat_name in worklist:

        StatAffinity = []
        StatAffinity_inverse = []

        for aff_gear, meldslots_gear in zip(GearSet.Affinity, GearSet.AllowedMelds):
            StatAffinity.append(aff_gear[stat_name])

            Meldslots_inverse = 0
            for stype in Stats_in_use:
                if not stype == stat_name:
                    Meldslots_inverse += meldslots_gear[stype]

            StatAffinity_inverse.append(Meldslots_inverse)

        if printtrig == 1:
            print(stat_name)
            print(Stats_in_use)
            for nn, mm, kk in zip(StatAffinity, StatAffinity_inverse, GearSet.AllowedMelds):
                print(nn,'    ',mm, '    ',kk)
            printtrig = 0

        #Sort meld priority list for gear after the affinity listStatAffinity_inverse
        idx2gear = list(range(0,11))
        StatAffinity, idx2gear = (list(t) for t in zip(*sorted(zip(StatAffinity_inverse, idx2gear), reverse = False)))  

        #Bypass affinity sorting
        #idx2gear = list(range(11)) 
        #print(idx2gear, stat_name)

        trying_to_meld = True
        idx = 0        
        while trying_to_meld == True:

            #Translate idx to hear index according to stat affinity
            gear_index = idx2gear[idx]

            if Total_Slots_Left[gear_index] > 0:
                if Stat_Slots_Left[gear_index][stat_name] > 0:
                    #Meld gear sucessfully
                    check_summa += 1
                    #Subtract from available slots
                    Total_Slots_Left[gear_index] = Total_Slots_Left[gear_index] - 1
                    Stat_Slots_Left[gear_index][stat_name] = Stat_Slots_Left[gear_index][stat_name] - 1
                    trying_to_meld = False                            
                    Slotted_Melds[gear_index].append(stat_name)                       
                    

            idx += 1
            if idx > 10 and trying_to_meld == True:
                trying_to_meld = False
                Success = False
                if debug == True:
                    print(f"Failed to meld {stat_name}")

    if not summa == check_summa:
        Success = False
  

    return Success, Slotted_Melds












def MeldTest_Randomized(Melds_to_meld_in, GearSet, debug = False):

    Melds_to_meld = copy.deepcopy(Melds_to_meld_in)

    #If both these lists/dictionaries have space for a meld it is allowed
    Total_Slots_Left = copy.deepcopy(GearSet.TotalMelds)
    Stat_Slots_Left = copy.deepcopy(GearSet.AllowedMelds)

    Slotted_Melds = [[],[],[],[],[],[],[],[],[],[],[]]
    check_summa = 0
    summa = sum(Melds_to_meld)

    worklist = []
    for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
        if meldtype > 0:
            for i in range(meldtype):
                worklist.append(statName)
    random.shuffle(worklist)

    tries_left = 100
    while tries_left > 0:
        Success = True
        #If both these lists/dictionaries have space for a meld it is allowed
        Total_Slots_Left = copy.deepcopy(GearSet.TotalMelds)
        Stat_Slots_Left = copy.deepcopy(GearSet.AllowedMelds)

        Slotted_Melds = [[],[],[],[],[],[],[],[],[],[],[]]
        check_summa = 0
        summa = sum(Melds_to_meld)

        worklist = []
        for meldtype, statName in zip(Melds_to_meld, list(GearSet.AllowedMelds[0])):
            if meldtype > 0:
                for i in range(meldtype):
                    worklist.append(statName)
        random.shuffle(worklist)

        for stat_name in worklist:
            #Meld according to affinity
            idx2gear = list(range(0,11))
            StatAffinity = []
            for aff_gear in GearSet.Affinity:
                StatAffinity.append(aff_gear[stat_name])
            StatAffinity, idx2gear = (list(t) for t in zip(*sorted(zip(StatAffinity, idx2gear), reverse = True)))  

            idx2gear = list(range(11)) #Bypass affinity sorting

            trying_to_meld = True
            idx = 0
            while trying_to_meld == True:

                #Translate idx to hear index according to stat affinity
                gear_index = idx2gear[idx]

                if Total_Slots_Left[gear_index] > 0:
                    if Stat_Slots_Left[gear_index][stat_name] > 0:
                        #Meld gear sucessfully
                        check_summa += 1
                        #Subtract from available slots
                        Total_Slots_Left[gear_index] = Total_Slots_Left[gear_index] - 1
                        Stat_Slots_Left[gear_index][stat_name] = Stat_Slots_Left[gear_index][stat_name] - 1
                        trying_to_meld = False                            
                        Slotted_Melds[gear_index].append(stat_name)                       
                        

                idx += 1
                if idx > 10 and trying_to_meld == True:
                    trying_to_meld = False
                    Success = False
                    if debug == True:
                        print(f"Failed to meld {stat_name}")

        if not summa == check_summa:
            Success = False
            tries_left -= 1

        if Success == True:
            tries_left = 0        

    return Success, Slotted_Melds

def MeldTest(Melds_to_meld_in, GearSet):

    Melds_to_meld = copy.deepcopy(Melds_to_meld_in)

    #If both these lists/dictionaries have space for a meld it is allowed
    Total_Slots_Left = copy.deepcopy(GearSet.TotalMelds)
    Stat_Slots_Left = copy.deepcopy(GearSet.AllowedMelds)
    #print(Total_Slots_Left, sum(Total_Slots_Left))
    #print(Melds_to_meld, sum(Melds_to_meld))

    Slotted_Melds = [[],[],[],[],[],[],[],[],[],[],[]]
    check_summa = 0
    summa = sum(Melds_to_meld)
    Success = True

    for number_of_Melds, stat_name in zip(Melds_to_meld, GearSet.AllowedMelds[0]):

        if number_of_Melds > 0:   

            for single_meld in range(1, number_of_Melds + 1):
                #print(list(range(1, number_of_Melds + 1)))                
                trying_to_meld = True
                gear_index = 0
                while trying_to_meld == True:
                    
                    if Total_Slots_Left[gear_index] > 0:
                        if Stat_Slots_Left[gear_index][stat_name] > 0:
                            #Meld gear sucessfully
                            check_summa += 1
                            #Subtract from available slots
                            Total_Slots_Left[gear_index] = Total_Slots_Left[gear_index] - 1
                            Stat_Slots_Left[gear_index][stat_name] = Stat_Slots_Left[gear_index][stat_name] - 1
                            trying_to_meld = False                            
                            Slotted_Melds[gear_index].append(stat_name)                            
                            

                    gear_index += 1
                    if gear_index > 10 and trying_to_meld == True:
                        trying_to_meld = False
                        Success = False
                        

    if not summa == check_summa:
        Success = False
    #if Success == True:
    #    print(Total_Slots_Left, sum(Total_Slots_Left))

    return Success, Slotted_Melds



if __name__ == "__main__":
    Main()
