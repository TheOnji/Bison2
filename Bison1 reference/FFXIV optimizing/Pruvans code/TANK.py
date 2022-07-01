
import os.path
import math
import time
import datetime

# Globals
LEVELMOD_MAIN = 390
LEVELMOD_SUB = 400
LEVELMOD_DIV = 1900
MATERIA_VALUE = 36

# Job modifier
# Warrior
# JOBMOD_ATR = 105
# Gunbreaker
JOBMOD_ATR = 100

RACEMOD_ATR = 2
TRAIT_ATR = 0

MIN_GCD = 0.00
MAX_GCD = 2.50

# % of DPS that already enjoys guaranteed CH's and DH's
# Warrior
# GUARANTEED_CRIT_PERCENTAGE = 0.4069
# GUARANTEED_DH_PERCENTAGE = 0.4069
# Gunbreaker
GUARANTEED_CRIT_PERCENTAGE = 0
GUARANTEED_DH_PERCENTAGE = 0

# % of DPS that are auto attacks
# Warrior
# AUTO_ATTACK_PERCENTAGE = 0.1237
# Gunbreaker
AUTO_ATTACK_PERCENTAGE = 0.1110

# % of DPS that are DoT's
# Warrior
# DOT_PERCENTAGE = 0
# Gunbreaker
DOT_PERCENTAGE = 0.0706

# Relic weapon
RELIC_WEAPON = 0
RELIC_POINTS = 0
RELIC_MAX_FREE_POINTS = 25

# Extra requirements
MINIMUM_TENACITY = 0
MAXIMIZE_TENACITY = 0


class GearPiece:
	def __init__(self, s_ATR, s_CH, s_DET, s_SS, s_DH, s_TEN, s_MAX, s_NAME, s_SLOTS = 0, s_UNIQUE = 1, s_DAMAGE = 0, s_DELAY = 0):
		self.ATR = s_ATR
		self.CH = min(s_CH, s_MAX)
		self.DET = min(s_DET, s_MAX)
		self.SS = min(s_SS, s_MAX)
		self.DH = min(s_DH, s_MAX)
		self.TEN = min(s_TEN, s_MAX)
		self.MAX = s_MAX
		self.NAME = s_NAME
		self.SLOTS = s_SLOTS
		self.UNIQUE = s_UNIQUE
		self.DAMAGE = s_DAMAGE
		self.DELAY = s_DELAY
		
		self.MAT_CH_MAX = int(min(((self.MAX - self.CH) - (self.MAX - self.CH) % MATERIA_VALUE) / MATERIA_VALUE, self.SLOTS))
		self.MAT_DET_MAX = int(min(((self.MAX - self.DET) - (self.MAX - self.DET) % MATERIA_VALUE) / MATERIA_VALUE, self.SLOTS))
		self.MAT_SS_MAX = int(min(((self.MAX - self.SS) - (self.MAX - self.SS) % MATERIA_VALUE) / MATERIA_VALUE, self.SLOTS))
		self.MAT_DH_MAX = int(min(((self.MAX - self.DH) - (self.MAX - self.DH) % MATERIA_VALUE) / MATERIA_VALUE, self.SLOTS))
		self.MAT_TEN_MAX = int(min(((self.MAX - self.TEN) - (self.MAX - self.TEN) % MATERIA_VALUE) / MATERIA_VALUE, self.SLOTS))
		
		self.MAT_MAX = [self.MAT_CH_MAX, self.MAT_DET_MAX, self.MAT_SS_MAX, self.MAT_DH_MAX, self.MAT_TEN_MAX]
		self.MAT_SLOTTED = [0, 0, 0, 0, 0]
		
		self.SLOT_SIG = ""
		
		if self.MAT_MAX[0] > 0:
			if self.SLOT_SIG != "":
				self.SLOT_SIG = self.SLOT_SIG + "_"
			self.SLOT_SIG = self.SLOT_SIG + "CH"
		
		if self.MAT_MAX[1] > 0:
			if self.SLOT_SIG != "":
				self.SLOT_SIG = self.SLOT_SIG + "_"
			self.SLOT_SIG = self.SLOT_SIG + "DET"
		
		if self.MAT_MAX[2] > 0:
			if self.SLOT_SIG != "":
				self.SLOT_SIG = self.SLOT_SIG + "_"
			self.SLOT_SIG = self.SLOT_SIG + "SS"
		
		if self.MAT_MAX[3] > 0:
			if self.SLOT_SIG != "":
				self.SLOT_SIG = self.SLOT_SIG + "_"
			self.SLOT_SIG = self.SLOT_SIG + "DH"
		
		if self.MAT_MAX[4] > 0:
			if self.SLOT_SIG != "":
				self.SLOT_SIG = self.SLOT_SIG + "_"
			self.SLOT_SIG = self.SLOT_SIG + "TEN"


WEAPONS = [
	# GearPiece(304, 269, 188, 0, 0, 0, 269, "Asphodelos War Hammer", 2, 1, 120, 3.36)
	GearPiece(304, 269, 188, 0, 0, 0, 269, "Asphodelos Bayonet", 2, 1, 120, 2.80)
	# GearPiece(266, 253, 177, 0, 0, 0, 253, "Labrys of Divine Light", 2, 1, 115, 3.36)
]

SHIELDS = [
	GearPiece(0, 0, 0, 0, 0, 0, 0, "<No Shield>")
]

HEADS = [
	GearPiece(180, 0, 162, 0, 0, 113, 162, "Asphodelos Circlet of Fending", 2),
	GearPiece(180, 162, 0, 113, 0, 0, 162, "Augmented Radiant's Helm of Fending", 2)
	# GearPiece(170, 158, 0, 111, 0, 0, 158, "Radiant's Helm of Fending", 2),
]

BODIES = [
	GearPiece(285, 257, 180, 0, 0, 0, 257, "Asphodelos Chiton of Fending", 2),
	GearPiece(285, 0, 257, 0, 0, 180, 257, "Augmented Radiant's Scale Mail of Fending", 2)
]

HANDS = [
	GearPiece(180, 0, 113, 0, 0, 162, 162, "Asphodelos Vambraces of Fending", 2),
	GearPiece(180, 162, 113, 0, 0, 0, 162, "Augmented Radiant's Gauntlets of Fending", 2)
	# GearPiece(161, 154, 108, 0, 0, 0, 154, "Limbo Vambraces of Fending", 2),
	# GearPiece(161, 154, 154, 0, 0, 0, 154, "Limbo Vambraces of Fending-DETx2", 0)
]

LEGS = [
	GearPiece(285, 0, 257, 0, 0, 180, 257, "Asphodelos Skirt of Fending", 2),
	GearPiece(285, 180, 257, 0, 0, 0, 257, "Augmented Radiant's Cuisses of Fending", 2)
	# GearPiece(270, 175, 250, 0, 0, 0, 250, "Radiant's Cuisses of Fending", 2)
]

FEET = [
	GearPiece(180, 162, 0, 113, 0, 0, 162, "Asphodelos Boots of Fending", 2),
	GearPiece(180, 113, 0, 0, 0, 162, 162, "Augmented Radiant's Sabatons of Fending", 2)
	# GearPiece(161, 108, 0, 154, 0, 0, 154, "Limbo Boots of Fending", 2),
	# GearPiece(161, 154, 0, 154, 0, 0, 154, "Limbo Boots of Fending-CHx2", 0)
]

EARRINGS = [
	GearPiece(142, 127, 89, 0, 0, 0, 127, "Asphodelos Earrings of Fending", 2),
	GearPiece(142, 0, 127, 89, 0, 0, 127, "Augmented Radiant's Earrings of Fending", 2)
	# GearPiece(127, 0, 85, 121, 0, 0, 121, "Classical Earrings of Fending", 2)
]

NECKLACES = [
	GearPiece(142, 0, 89, 127, 0, 0, 127, "Asphodelos Necklace of Fending", 2),
	GearPiece(142, 89, 0, 0, 0, 127, 127, "Augmented Radiant's Choker of Fending", 2)
	# GearPiece(127, 121, 85, 0, 0, 0, 121, "Classical Choker of Fending", 2)
]

BRACELETS = [
	GearPiece(142, 0, 89, 0, 0, 127, 127, "Asphodelos Amulet of Fending", 2),
	GearPiece(142, 89, 127, 0, 0, 0, 127, "Augmented Radiant's Bracelet of Fending", 2)
	# GearPiece(127, 0, 85, 0, 0, 121, 121, "Classical Wristband of Fending", 2)
]

RINGS = [
	GearPiece(142, 127, 89, 0, 0, 0, 127, "Asphodelos Ring of Fending", 2),
	GearPiece(142, 0, 0, 89, 0, 127, 127, "Augmented Radiant's Ring of Fending", 2),
	# GearPiece(134, 0, 0, 87, 0, 124, 124, "Radiant's Ring of Fending", 2)
	# GearPiece(127, 85, 121, 0, 0, 0, 121, "Classical Ring of Fending", 2)
]

FOODS = [
	GearPiece(0, 54, 90, 0, 0, 0, 90, "Pumpkin Potage"),		# DET > CH
	GearPiece(0, 0, 54, 0, 90, 0, 90, "Archon Burger"),			# DH > DET
	GearPiece(0, 0, 0, 90, 54, 0, 90, "Beef Stroganoff"),		# SS > DH
	GearPiece(0, 90, 0, 54, 0, 0, 90, "Pumpkin Ratatouille"),	# CH > SS
	GearPiece(0, 0, 54, 0, 0, 90, 90, "Scallop Salad"),			# TEN > DET
	GearPiece(0, 0, 90, 0, 0, 54, 90, "Scallop Curry"),			# DET > TEN
	GearPiece(0, 0, 0, 75, 0, 45, 75, "Karniyarik"),			# SS > TEN
	GearPiece(0, 45, 0, 0, 0, 75, 75, "Hamsa Curry")			# TEN > CH
]


CH_TIERS = []
total_stat = LEVELMOD_SUB
counter = 0

while(total_stat < 5000):
	CH_TIERS.append(total_stat)
	counter += 1
	total_stat = math.ceil(LEVELMOD_SUB + counter * LEVELMOD_DIV / 200)

DET_TIERS = []
total_stat = LEVELMOD_MAIN
counter = 0

while(total_stat < 5000):
	DET_TIERS.append(total_stat)
	counter += 1
	total_stat = math.ceil(LEVELMOD_MAIN + counter * LEVELMOD_DIV / 130)

SS_TIERS = []
total_stat = LEVELMOD_SUB
counter = 0

while(total_stat < 5000):
	SS_TIERS.append(total_stat)
	counter += 1
	total_stat = math.ceil(LEVELMOD_SUB + counter * LEVELMOD_DIV / 130)

DH_TIERS = []
total_stat = LEVELMOD_SUB
counter = 0

while(total_stat < 5000):
	DH_TIERS.append(total_stat)
	counter += 1
	total_stat = math.ceil(LEVELMOD_SUB + counter * LEVELMOD_DIV / 550)

TEN_TIERS = []
total_stat = LEVELMOD_SUB
counter = 0

while(total_stat < 5000):
	TEN_TIERS.append(total_stat)
	counter += 1
	total_stat = math.ceil(LEVELMOD_SUB + counter * LEVELMOD_DIV / 100)


POSSIBLE_GEAR_SETS = []

for weapon in WEAPONS:
	for shield in SHIELDS:
		for head in HEADS:
			for body in BODIES:
				for hand in HANDS:
					for leg in LEGS:
						for foot in FEET:
							for earring in EARRINGS:
								for necklace in NECKLACES:
									for bracelet in BRACELETS:
										for ring1 in RINGS:
											for ring2 in RINGS:
												
												# Rings can be unique
												if ring1 == ring2 and ring1.UNIQUE:
													continue
												
												# Rings are interchangeable
												if RINGS.index(ring2) < RINGS.index(ring1):
													continue
												
												# Tome ring can be stacked with itself
												if ring2.NAME == "Radiant's Ring of Fending" and not (ring1.NAME == "Augmented Radiant's Ring of Fending"):
													continue
												
												gear_set = [weapon, shield, head, body, hand, leg, foot, earring, necklace, bracelet, ring1, ring2]
												
												# We can filter sets that already have too much SS
												total_SS = LEVELMOD_SUB
												
												for piece in gear_set:
													total_SS += piece.SS
												
												f_SPD = math.floor(130 * (total_SS - LEVELMOD_SUB) / LEVELMOD_DIV + 1000)
												f_GCD = math.floor(math.floor((2000 - f_SPD) * 2500 / 1000)/10)/100
												
												if f_GCD < MIN_GCD:
													continue
												
												POSSIBLE_GEAR_SETS.append(gear_set)


print("-----")
print(str(len(POSSIBLE_GEAR_SETS)) + " possible gear sets found.")
input("Press ENTER to continue.")
print("-----")


COMBINATION_COUNTER = 0
BIS_SET_GCD = []
BIS_SET_MULTIPLIER = []
BIS_SET_TENACITY = []
BIS_SET_OUTPUT = []
TIMER = time.time()

for gear_set in POSSIBLE_GEAR_SETS:
	percentage_completed = 100*COMBINATION_COUNTER/len(POSSIBLE_GEAR_SETS)
	
	if percentage_completed != 0:
		elapsed_time = int(time.time() - TIMER)
		time_to_finish = int(100 * elapsed_time / percentage_completed - elapsed_time)
		
		print("Progress: " + str('{:.3f}'.format(percentage_completed)) + "% - ETA " + str(datetime.timedelta(seconds=time_to_finish)))
	
	COMBINATION_COUNTER += 1
	
	
	total_ATR = math.floor(LEVELMOD_MAIN * JOBMOD_ATR / 100) + RACEMOD_ATR + TRAIT_ATR
	gear_CH = 0
	gear_DET = 0
	gear_SS = 0
	gear_DH = 0
	gear_TEN = 0
	
	materia_total = 0
	materia_max = [0, 0, 0, 0, 0]
	
	slot_sigs = []
	slot_sigs_count = []
	slot_sigs_materia = []
	
	for piece in gear_set:
		
		total_ATR += piece.ATR
		gear_CH += piece.CH
		gear_DET += piece.DET
		gear_SS += piece.SS
		gear_DH += piece.DH
		gear_TEN += piece.TEN
		
		materia_total += piece.SLOTS
		
		for index in range(0, len(materia_max)):
			materia_max[index] += piece.MAT_MAX[index]
		
		if piece.SLOT_SIG in slot_sigs:
			sig_index = slot_sigs.index(piece.SLOT_SIG)
			slot_sigs_count[sig_index] += piece.SLOTS
			
			for index in range(0, len(piece.MAT_MAX)):
				slot_sigs_materia[sig_index][index] += piece.MAT_MAX[index]
		else:
			slot_sigs.append(piece.SLOT_SIG)
			slot_sigs_count.append(piece.SLOTS)
			slot_sigs_materia.append(piece.MAT_MAX.copy())
	
	
	mat_CH_off_DET = 0
	mat_CH_off_SS = 0
	mat_CH_off_DH = 0
	mat_CH_off_TEN = 0
	
	mat_DET_off_CH = 0
	mat_DET_off_SS = 0
	mat_DET_off_DH = 0
	mat_DET_off_TEN = 0
	
	mat_SS_off_CH = 0
	mat_SS_off_DET = 0
	mat_SS_off_DH = 0
	mat_SS_off_TEN = 0
	
	mat_DH_off_CH = 0
	mat_DH_off_DET = 0
	mat_DH_off_SS = 0
	mat_DH_off_TEN = 0
	
	mat_TEN_off_CH = 0
	mat_TEN_off_DET = 0
	mat_TEN_off_SS = 0
	mat_TEN_off_DH = 0
	
	for index in range(0, len(slot_sigs)):
		mat_CH_off_DET += min(slot_sigs_materia[index][0], slot_sigs_count[index] - slot_sigs_materia[index][1])
		mat_CH_off_SS += min(slot_sigs_materia[index][0], slot_sigs_count[index] - slot_sigs_materia[index][2])
		mat_CH_off_DH += min(slot_sigs_materia[index][0], slot_sigs_count[index] - slot_sigs_materia[index][3])
		mat_CH_off_TEN += min(slot_sigs_materia[index][0], slot_sigs_count[index] - slot_sigs_materia[index][4])
		
		mat_DET_off_CH += min(slot_sigs_materia[index][1], slot_sigs_count[index] - slot_sigs_materia[index][0])
		mat_DET_off_SS += min(slot_sigs_materia[index][1], slot_sigs_count[index] - slot_sigs_materia[index][2])
		mat_DET_off_DH += min(slot_sigs_materia[index][1], slot_sigs_count[index] - slot_sigs_materia[index][3])
		mat_DET_off_TEN += min(slot_sigs_materia[index][1], slot_sigs_count[index] - slot_sigs_materia[index][4])
		
		mat_SS_off_CH += min(slot_sigs_materia[index][2], slot_sigs_count[index] - slot_sigs_materia[index][0])
		mat_SS_off_DET += min(slot_sigs_materia[index][2], slot_sigs_count[index] - slot_sigs_materia[index][1])
		mat_SS_off_DH += min(slot_sigs_materia[index][2], slot_sigs_count[index] - slot_sigs_materia[index][3])
		mat_SS_off_TEN += min(slot_sigs_materia[index][2], slot_sigs_count[index] - slot_sigs_materia[index][4])
		
		mat_DH_off_CH += min(slot_sigs_materia[index][3], slot_sigs_count[index] - slot_sigs_materia[index][0])
		mat_DH_off_DET += min(slot_sigs_materia[index][3], slot_sigs_count[index] - slot_sigs_materia[index][1])
		mat_DH_off_SS += min(slot_sigs_materia[index][3], slot_sigs_count[index] - slot_sigs_materia[index][2])
		mat_DH_off_TEN += min(slot_sigs_materia[index][3], slot_sigs_count[index] - slot_sigs_materia[index][4])
		
		mat_TEN_off_CH += min(slot_sigs_materia[index][4], slot_sigs_count[index] - slot_sigs_materia[index][0])
		mat_TEN_off_DET += min(slot_sigs_materia[index][4], slot_sigs_count[index] - slot_sigs_materia[index][1])
		mat_TEN_off_SS += min(slot_sigs_materia[index][4], slot_sigs_count[index] - slot_sigs_materia[index][2])
		mat_TEN_off_DH += min(slot_sigs_materia[index][4], slot_sigs_count[index] - slot_sigs_materia[index][3])
	
	
	for mat_CH_slotted in range(0, materia_max[0] + 1):
		remaining_slots = materia_total - mat_CH_slotted
		
		for mat_DET_slotted in range(0, min(materia_max[1], remaining_slots) + 1):
			remaining_slots = materia_total - mat_CH_slotted - mat_DET_slotted
			
			for mat_SS_slotted in range(0, min(materia_max[2], remaining_slots) + 1):
				remaining_slots = materia_total - mat_CH_slotted - mat_DET_slotted - mat_SS_slotted
				
				for mat_DH_slotted in range(0, min(materia_max[3], remaining_slots) + 1):
					remaining_slots = materia_total - mat_CH_slotted - mat_DET_slotted - mat_SS_slotted - mat_DH_slotted
					
					for mat_TEN_slotted in range(0, min(materia_max[4], remaining_slots) + 1):
						remaining_slots = materia_total - mat_CH_slotted - mat_DET_slotted - mat_SS_slotted - mat_DH_slotted - mat_TEN_slotted
						
						if remaining_slots != 0:
							continue
						
						mat_CH_possible = materia_max[0] - max(mat_DET_slotted - mat_DET_off_CH, 0) - max(mat_SS_slotted - mat_SS_off_CH, 0) - max(mat_DH_slotted - mat_DH_off_CH, 0) - max(mat_TEN_slotted - mat_TEN_off_CH, 0)
						mat_DET_possible = materia_max[1] - max(mat_CH_slotted - mat_CH_off_DET, 0) - max(mat_SS_slotted - mat_SS_off_DET, 0) - max(mat_DH_slotted - mat_DH_off_DET, 0) - max(mat_TEN_slotted - mat_TEN_off_DET, 0)
						mat_SS_possible = materia_max[2] - max(mat_CH_slotted - mat_CH_off_SS, 0) - max(mat_DET_slotted - mat_DET_off_SS, 0) - max(mat_DH_slotted - mat_DH_off_SS, 0) - max(mat_TEN_slotted - mat_TEN_off_SS, 0)
						mat_DH_possible = materia_max[3] - max(mat_CH_slotted - mat_CH_off_DH, 0) - max(mat_DET_slotted - mat_DET_off_DH, 0) - max(mat_SS_slotted - mat_SS_off_DH, 0) - max(mat_TEN_slotted - mat_TEN_off_DH, 0)
						mat_TEN_possible = materia_max[4] - max(mat_CH_slotted - mat_CH_off_TEN, 0) - max(mat_DET_slotted - mat_DET_off_TEN, 0) - max(mat_SS_slotted - mat_SS_off_TEN, 0) - max(mat_DH_slotted - mat_DH_off_TEN, 0)
						
						if (mat_CH_slotted > mat_CH_possible) or (mat_DET_slotted > mat_DET_possible) or (mat_SS_slotted > mat_SS_possible) or (mat_DH_slotted > mat_DH_possible) or (mat_TEN_slotted > mat_TEN_possible):
							continue
						
						materia_slotted = [mat_CH_slotted, mat_DET_slotted, mat_SS_slotted, mat_DH_slotted, mat_TEN_slotted]
						materia_CH = materia_slotted[0] * MATERIA_VALUE
						materia_DET = materia_slotted[1] * MATERIA_VALUE
						materia_SS = materia_slotted[2] * MATERIA_VALUE
						materia_DH = materia_slotted[3] * MATERIA_VALUE
						materia_TEN = materia_slotted[4] * MATERIA_VALUE
						
						
						for food in FOODS:
							
							prefood_CH = LEVELMOD_SUB + gear_CH + materia_CH
							prefood_DET = LEVELMOD_MAIN + gear_DET + materia_DET
							prefood_SS = LEVELMOD_SUB + gear_SS + materia_SS
							prefood_DH = LEVELMOD_SUB + gear_DH + materia_DH
							prefood_TEN = LEVELMOD_SUB + gear_TEN + materia_TEN
							
							
							# Speed check to cut on cycles
							f_SPD = math.floor(130 * (prefood_SS - LEVELMOD_SUB) / LEVELMOD_DIV + 1000)
							f_GCD = math.floor(math.floor((2000 - f_SPD) * 2500 / 1000)/10)/100
							
							if f_GCD < MIN_GCD:
								continue
							
							
							total_DH = prefood_DH + min(food.DH, int(0.1 * prefood_DH))
							
							if RELIC_WEAPON:
								relic_MAX = gear_set[0].MAX
							else:
								relic_MAX = 0
							
							relic_CH_min = 0
							relic_CH_index = -1
							
							for relic_CH in range(relic_CH_min, relic_MAX + 1):
								
								relic_FREE = RELIC_POINTS - relic_CH
								
								if relic_FREE > (RELIC_MAX_FREE_POINTS + relic_MAX * 3):
									continue
								
								total_CH = prefood_CH + relic_CH + min(food.CH, int(0.1 * (prefood_CH + relic_CH)))
								
								if relic_CH_index == -1:
									for index in range(0, len(CH_TIERS)):
										if CH_TIERS[index] > total_CH:
											relic_CH_index = index
											break
								elif total_CH < CH_TIERS[relic_CH_index]:
									continue
								else:
									relic_CH_index += 1
								
								relic_DET_min = relic_FREE - RELIC_MAX_FREE_POINTS - relic_MAX * 2
								relic_DET_index = -1
								
								for relic_DET in range(max(relic_DET_min, 0), min(relic_MAX, relic_FREE) + 1):
									
									relic_FREE = RELIC_POINTS - relic_CH - relic_DET
									
									if relic_FREE > (RELIC_MAX_FREE_POINTS + relic_MAX * 2):
										continue
									
									total_DET = prefood_DET + relic_DET + min(food.DET, int(0.1 * (prefood_DET + relic_DET)))
									
									if relic_DET_index == -1:
										for index in range(0, len(DET_TIERS)):
											if DET_TIERS[index] > total_DET:
												relic_DET_index = index
												break
									elif total_DET < DET_TIERS[relic_DET_index]:
										continue
									else:
										relic_DET_index += 1
									
									relic_SS_min = relic_FREE - RELIC_MAX_FREE_POINTS - relic_MAX
									relic_SS_index = -1
									
									for relic_SS in range(max(relic_SS_min, 0), min(relic_MAX, relic_FREE) + 1):
										
										relic_FREE = RELIC_POINTS - relic_CH - relic_DET - relic_SS
										
										if relic_FREE > (RELIC_MAX_FREE_POINTS + relic_MAX):
											continue
										
										total_SS = prefood_SS + relic_SS + min(food.SS, int(0.1 * (prefood_SS + relic_SS)))
										
										if relic_SS_index == -1:
											for index in range(0, len(SS_TIERS)):
												if SS_TIERS[index] > total_SS:
													relic_SS_index = index
													break
										elif total_SS < SS_TIERS[relic_SS_index]:
											continue
										else:
											relic_SS_index += 1
										
										f_SPD = math.floor(130 * (total_SS - LEVELMOD_SUB) / LEVELMOD_DIV) + 1000
										f_GCD = math.floor(math.floor((2000 - f_SPD) * 2500 / 1000)/10)/100
										
										if f_GCD < MIN_GCD or f_GCD > MAX_GCD:
											continue
										
										relic_TEN_min = relic_FREE - RELIC_MAX_FREE_POINTS
										relic_TEN_index = -1
										
										for relic_TEN in range(max(relic_TEN_min, 0), min(relic_MAX, relic_FREE) + 1):
											
											relic_FREE = RELIC_POINTS - relic_CH - relic_DET - relic_SS - relic_TEN
											
											if relic_FREE > RELIC_MAX_FREE_POINTS:
												continue
											
											total_TEN = prefood_TEN + relic_TEN + min(food.TEN, int(0.1 * (prefood_TEN + relic_TEN)))
											
											if relic_TEN_index == -1:
												for index in range(0, len(TEN_TIERS)):
													if TEN_TIERS[index] > total_TEN:
														relic_TEN_index = index
														break
											elif total_TEN < TEN_TIERS[relic_TEN_index]:
												continue
											else:
												relic_TEN_index += 1
											
											if total_TEN < MINIMUM_TENACITY:
												continue
											
											f_ATK = math.floor(115 * (total_ATR - LEVELMOD_MAIN) / LEVELMOD_MAIN) + 100
											
											f_DET = math.floor(140 * (total_DET - LEVELMOD_MAIN) / LEVELMOD_DIV + 1000)
											
											f_TEN = math.floor(100 * (total_TEN - LEVELMOD_SUB) / LEVELMOD_DIV) + 1000
											
											f_WD = math.floor(LEVELMOD_MAIN * JOBMOD_ATR / 1000 + gear_set[0].DAMAGE)
											
											p_CRIT = math.floor(200 * (total_CH - LEVELMOD_SUB) / LEVELMOD_DIV + 50) / 1000
											p_CRIT = GUARANTEED_CRIT_PERCENTAGE + p_CRIT * (1 - GUARANTEED_CRIT_PERCENTAGE)
											d_CRIT = math.floor(200 * (total_CH - LEVELMOD_SUB) / LEVELMOD_DIV) + 1400
											f_CRIT = (1 - p_CRIT) * 1000 + p_CRIT * d_CRIT
											
											p_DH = math.floor(550 * (total_DH - LEVELMOD_SUB) / LEVELMOD_DIV) / 1000
											p_DH = GUARANTEED_DH_PERCENTAGE + p_DH * (1 - GUARANTEED_DH_PERCENTAGE)
											f_DH = (1 - p_DH) * 100 + p_DH * 125
											
											f_AUTO = math.floor(f_WD * gear_set[0].DELAY / 3)
											
											f_DAM1 = math.floor(math.floor(math.floor(1000 * f_ATK * f_DET) / 100) / 1000)
											
											f_DAM2_NORM = math.floor(math.floor(math.floor(math.floor(f_DAM1 * f_TEN) / 1000) * f_WD) / 100)
											f_DAM2_AA = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(f_DAM1 * f_TEN) / 1000) * f_SPD) / 1000) * f_AUTO) / 100)
											f_DAM2_DOT = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(f_DAM1 * f_TEN) / 1000) * f_SPD) / 1000) * f_WD) / 100) + 1
											
											f_DAM3_NORM = math.floor(math.floor(math.floor(math.floor(f_DAM2_NORM * f_CRIT) / 1000) * f_DH) / 100)
											f_DAM3_AA = math.floor(math.floor(math.floor(math.floor(f_DAM2_AA * f_CRIT) / 1000) * f_DH) / 100)
											f_DAM3_DOT = math.floor(math.floor(math.floor(math.floor(f_DAM2_DOT * f_CRIT) / 1000) * f_DH) / 100)
											
											DH_MUL = 0
											if p_DH > 0:
												DH_MUL = 125
											else:
												DH_MUL = 100
											
											f_DAM3_NORM_MAX = math.floor(math.floor(math.floor(math.floor(f_DAM2_NORM * d_CRIT) / 1000) * DH_MUL) / 100)
											f_DAM3_AA_MAX = math.floor(math.floor(math.floor(math.floor(f_DAM2_AA * d_CRIT) / 1000) * DH_MUL) / 100)
											f_DAM3_DOT_MAX = math.floor(math.floor(math.floor(math.floor(f_DAM2_DOT * d_CRIT) / 1000) * DH_MUL) / 100)
											
											avg_multiplier = math.floor((1 - AUTO_ATTACK_PERCENTAGE - DOT_PERCENTAGE) * f_DAM3_NORM + AUTO_ATTACK_PERCENTAGE * f_DAM3_AA + DOT_PERCENTAGE * f_DAM3_DOT) / 1000
											max_multiplier = math.floor((1 - AUTO_ATTACK_PERCENTAGE - DOT_PERCENTAGE) * f_DAM3_NORM_MAX + AUTO_ATTACK_PERCENTAGE * f_DAM3_AA_MAX + DOT_PERCENTAGE * f_DAM3_DOT_MAX) / 1000
											
											
											GCD_index = -1
											
											if f_GCD in BIS_SET_GCD:
												GCD_index = BIS_SET_GCD.index(f_GCD)
												
												if MAXIMIZE_TENACITY and f_TEN > BIS_SET_TENACITY[GCD_index]:
													BIS_SET_MULTIPLIER[GCD_index] = avg_multiplier
													BIS_SET_TENACITY[GCD_index] = f_TEN
												elif MAXIMIZE_TENACITY and f_TEN == BIS_SET_TENACITY[GCD_index] and avg_multiplier > BIS_SET_MULTIPLIER[GCD_index]:
													BIS_SET_MULTIPLIER[GCD_index] = avg_multiplier
													BIS_SET_TENACITY[GCD_index] = f_TEN
												elif (not MAXIMIZE_TENACITY) and avg_multiplier > BIS_SET_MULTIPLIER[GCD_index]:
													BIS_SET_MULTIPLIER[GCD_index] = avg_multiplier
													BIS_SET_TENACITY[GCD_index] = f_TEN
												else:
													continue
											
											
											materia_assigned = [0, 0, 0, 0, 0]
											slot_sigs_assignment = []
											
											for sig_index in range(0, len(slot_sigs)):
												slot_sigs_assignment.append([0, 0, 0, 0, 0])
											
											changes_to_be_made = 1
											
											while(changes_to_be_made):
												changes_to_be_made = 0
												materia_to_slot = [0, 0, 0, 0, 0]
												materia_max_current = [0, 0, 0, 0, 0]
												
												for mat_index in range(0, len(materia_slotted)):
													materia_to_slot[mat_index] = materia_slotted[mat_index] - materia_assigned[mat_index]
												
												for sig_index in range(0, len(slot_sigs)):
													for mat_index in range(0, len(materia_slotted)):
														materia_max_current[mat_index] += min(slot_sigs_materia[sig_index][mat_index] - slot_sigs_assignment[sig_index][mat_index], slot_sigs_count[sig_index] - sum(slot_sigs_assignment[sig_index]))
												
												# Check if the materia to assign requires all remaining slots of that type
												for mat_index in range(0, len(materia_slotted)):
													if changes_to_be_made:
														break
													
													if materia_to_slot[mat_index] > 0 and materia_to_slot[mat_index] == materia_max_current[mat_index]:
														changes_to_be_made = 1
														
														for sig_index in range(0, len(slot_sigs)):
															materia_to_add = min(slot_sigs_materia[sig_index][mat_index] - slot_sigs_assignment[sig_index][mat_index], slot_sigs_count[sig_index] - sum(slot_sigs_assignment[sig_index]))
															slot_sigs_assignment[sig_index][mat_index] += materia_to_add
															materia_assigned[mat_index] += materia_to_add
												
												if changes_to_be_made:
													continue
												
												# Assign any materia
												for mat_index in range(0, len(materia_slotted)):
													if changes_to_be_made:
														break
													
													if materia_to_slot[mat_index] > 0:
														for sig_index in range(0, len(slot_sigs)):
															if sum(slot_sigs_assignment[sig_index]) < slot_sigs_count[sig_index]:
																if slot_sigs_assignment[sig_index][mat_index] < slot_sigs_materia[sig_index][mat_index]:
																	changes_to_be_made = 1
																	slot_sigs_assignment[sig_index][mat_index] += 1
																	materia_assigned[mat_index] += 1
																	break
												
												if changes_to_be_made:
													continue
												
												# Check if any signatures require more assignments and swap with other signatures that can fit what we still need
												for sig_index in range(0, len(slot_sigs)):
													if changes_to_be_made:
														break
													
													if sum(slot_sigs_assignment[sig_index]) < slot_sigs_count[sig_index]:
														mat_index_still_need = materia_to_slot.index(max(materia_to_slot))
														
														for sig_index_2 in range(0, len(slot_sigs)):
															if changes_to_be_made:
																break
															
															if sig_index != sig_index_2:
																for mat_index in range(0, len(materia_slotted)):
																	if slot_sigs_assignment[sig_index_2][mat_index] > 0 and slot_sigs_assignment[sig_index][mat_index] < slot_sigs_materia[sig_index][mat_index]\
																	and slot_sigs_assignment[sig_index_2][mat_index_still_need] < slot_sigs_materia[sig_index_2][mat_index_still_need]:
																		changes_to_be_made = 1
																		slot_sigs_assignment[sig_index_2][mat_index] -= 1
																		slot_sigs_assignment[sig_index][mat_index] += 1
																		break
												
												if changes_to_be_made:
													continue
												
												# If any signature still requires more assignments, dump whatever we can in there from a different signature
												for sig_index in range(0, len(slot_sigs)):
													if changes_to_be_made:
														break
													
													if sum(slot_sigs_assignment[sig_index]) < slot_sigs_count[sig_index]:
														for sig_index_2 in range(0, len(slot_sigs)):
															if changes_to_be_made:
																break
															
															if sig_index != sig_index_2:
																for mat_index in range(0, len(materia_slotted)):
																	if slot_sigs_assignment[sig_index_2][mat_index] > 0 and slot_sigs_assignment[sig_index][mat_index] < slot_sigs_materia[sig_index][mat_index]:
																		changes_to_be_made = 1
																		slot_sigs_assignment[sig_index_2][mat_index] -= 1
																		slot_sigs_assignment[sig_index][mat_index] += 1
																		break
											
											
											if materia_assigned != materia_slotted:
												print("-----")
												print("Slotted", materia_slotted)
												for index in range(0, len(slot_sigs)):
													print(slot_sigs[index], slot_sigs_count[index], slot_sigs_materia[index], slot_sigs_assignment[index], sum(slot_sigs_assignment[index]))
												print("Assigned", materia_assigned)
												print("Max", materia_max_current)
												input("-----")
											
											
											gear_set_copy = []
											for piece in gear_set:
												gear_set_copy.append(GearPiece(piece.ATR, piece.CH, piece.DET, piece.SS, piece.DH, piece.TEN, piece.MAX, piece.NAME, piece.SLOTS, piece.UNIQUE, piece.DAMAGE, piece.DELAY))
											
											materia_gear = [0, 0, 0, 0, 0]
											changes_to_be_made = 1
											
											while(changes_to_be_made):
												changes_to_be_made = 0
												
												materia_max_current = []
												
												for sig_index in range(0, len(slot_sigs)):
													temp_array = [0, 0, 0, 0, 0]
													
													for mat_index in range(0, len(materia_slotted)):
														for piece in gear_set_copy:
															if piece.SLOT_SIG == slot_sigs[sig_index]:
																temp_array[mat_index] += min(piece.MAT_MAX[mat_index] - piece.MAT_SLOTTED[mat_index], piece.SLOTS - sum(piece.MAT_SLOTTED))
													
													materia_max_current.append(temp_array)
												
												# Check if the materia requires all remaining slots
												for sig_index in range(0, len(slot_sigs)):
													if changes_to_be_made:
														break
													
													for mat_index in range(0, len(materia_slotted)):
														if changes_to_be_made:
															break
														
														if slot_sigs_assignment[sig_index][mat_index] > 0 and slot_sigs_assignment[sig_index][mat_index] == materia_max_current[sig_index][mat_index]:
															changes_to_be_made = 1
															
															for piece in gear_set_copy:
																free_slots = piece.SLOTS - sum(piece.MAT_SLOTTED)
																
																if piece.SLOT_SIG == slot_sigs[sig_index] and free_slots > 0:
																	materia_to_slot = min(piece.MAT_MAX[mat_index] - piece.MAT_SLOTTED[mat_index], free_slots)
																	piece.MAT_SLOTTED[mat_index] += materia_to_slot
																	slot_sigs_assignment[sig_index][mat_index] -= materia_to_slot
																	materia_gear[mat_index] += materia_to_slot
												
												if changes_to_be_made:
													continue
												
												# Slot whatever is possible
												for sig_index in range(0, len(slot_sigs)):
													if changes_to_be_made:
														break
													
													for mat_index in range(0, len(materia_slotted)):
														if changes_to_be_made:
															break
														
														if slot_sigs_assignment[sig_index][mat_index] > 0:
															for piece in gear_set_copy:
																if changes_to_be_made:
																	break
																
																free_slots = piece.SLOTS - sum(piece.MAT_SLOTTED)
																
																if piece.SLOT_SIG == slot_sigs[sig_index] and free_slots > 0 and piece.MAT_SLOTTED[mat_index] < piece.MAT_MAX[mat_index]:
																	changes_to_be_made = 1
																	materia_to_slot = 1
																	piece.MAT_SLOTTED[mat_index] += materia_to_slot
																	slot_sigs_assignment[sig_index][mat_index] -= materia_to_slot
																	materia_gear[mat_index] += materia_to_slot
											
											
											if materia_assigned != materia_gear:
												print("-----")
												print("Slotted", materia_slotted)
												for index in range(0, len(slot_sigs)):
													print(slot_sigs[index], slot_sigs_count[index], slot_sigs_materia[index], slot_sigs_assignment[index], materia_max_current[index])
												print("Assigned", materia_assigned)
												print("Gear", materia_gear, "Sum", sum(materia_gear))
												input("-----")
											
											
											if RELIC_WEAPON:
												gear_set_copy[0].NAME = gear_set_copy[0].NAME + "-" + str(relic_CH) + " CH " + str(relic_DET) + " DET " + str(relic_SS) + " SS " + str(relic_TEN) + " TEN " + str(relic_FREE) + " FREE"
											
											for piece in gear_set_copy:
												if piece.MAT_SLOTTED[0] > 0:
													piece.NAME = piece.NAME + "-CH"
													if piece.MAT_SLOTTED[0] > 1:
														piece.NAME = piece.NAME + " x" + str(piece.MAT_SLOTTED[0])
												if piece.MAT_SLOTTED[1] > 0:
													piece.NAME = piece.NAME + "-DET"
													if piece.MAT_SLOTTED[1] > 1:
														piece.NAME = piece.NAME + " x" + str(piece.MAT_SLOTTED[1])
												if piece.MAT_SLOTTED[2] > 0:
													piece.NAME = piece.NAME + "-SS"
													if piece.MAT_SLOTTED[2] > 1:
														piece.NAME = piece.NAME + " x" + str(piece.MAT_SLOTTED[2])
												if piece.MAT_SLOTTED[3] > 0:
													piece.NAME = piece.NAME + "-DH"
													if piece.MAT_SLOTTED[3] > 1:
														piece.NAME = piece.NAME + " x" + str(piece.MAT_SLOTTED[3])
												if piece.MAT_SLOTTED[4] > 0:
													piece.NAME = piece.NAME + "-TEN"
													if piece.MAT_SLOTTED[4] > 1:
														piece.NAME = piece.NAME + " x" + str(piece.MAT_SLOTTED[4])
											
											
											str_output = ""
											
											str_output = str_output + "BIS " + str('{:.2f}'.format(f_GCD)) + " (AVG)\n"
											str_output = str_output + "\n"
											for piece in gear_set_copy:
												str_output = str_output + piece.NAME + "\n"
											str_output = str_output + "\n"
											str_output = str_output + food.NAME + "\n"
											str_output = str_output + "\n"
											str_output = str_output + "Strength-" + str(total_ATR) + "\n"
											str_output = str_output + "Critical Hit-" + str(total_CH) + "\n"
											str_output = str_output + "Determination-" + str(total_DET) + "\n"
											str_output = str_output + "Skill Speed-" + str(total_SS) + "\n"
											str_output = str_output + "Direct Hit-" + str(total_DH) + "\n"
											str_output = str_output + "Tenacity-" + str(total_TEN) + "\n"
											str_output = str_output + "\n"
											str_output = str_output + "-AVG-MAX\n"
											str_output = str_output + "Multiplier-" + str(avg_multiplier) + "-" + str(max_multiplier) + "\n"
											
											if GCD_index >= 0:
												BIS_SET_OUTPUT[GCD_index] = str_output
											else:
												BIS_SET_GCD.append(f_GCD)
												BIS_SET_MULTIPLIER.append(avg_multiplier)
												BIS_SET_TENACITY.append(f_TEN)
												BIS_SET_OUTPUT.append(str_output)


print("-----")
print(str(len(BIS_SET_GCD)) + " possible GCDs found:")
for index in range(0, len(BIS_SET_GCD)):
	print(BIS_SET_GCD[index])
print("-----")


for index in range(0, len(BIS_SET_GCD)):
	file_path = "output\\" + str('{:.2f}'.format(BIS_SET_GCD[index])) + ".txt"
	with open(file_path, "w") as file_output:
		file_output.write(BIS_SET_OUTPUT[index])


print("All done.")
