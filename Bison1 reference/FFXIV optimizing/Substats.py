import math
import pandas as pd
import openpyxl, xlrd
import numpy as np
from matplotlib import pyplot as plt
import time

StatData = pd.read_excel ('Substats.xlsx', engine='openpyxl')
StatData = StatData.loc[:,~StatData.columns.str.match("Unnamed")]

class data():
	def __init__(self, CRIT, DET, DH, TEN, CRIT_DH_mod = True):
		#Record the stats
		self.CRIT = CRIT
		self.DET = DET
		self.DH = DH
		self.TEN = TEN 
		self.CRIT_DH_mod = CRIT_DH_mod

		#Read data from the spreadsheet
		self.f_CRIT, self.CRITrate, self.CRITmult = CRITmod(CRIT)
		self.f_DH, self.DHrate, self.DHmult = DHmod(DH)
		self.f_DET = DETmod(DET)
		self.f_TEN = TENmod(TEN)

		#Calcualtions for Critical Directs hits
		self.CRIT_DHrate = self.CRITrate * self.DHrate
		self.CRIT_DHmult = (1 + self.CRITmult) * (1 + self.DHmult) - 1

		if CRIT_DH_mod == True:
			#Adjust multipliers
			pureCRITrate = self.CRITrate - self.CRIT_DHrate
			pureDHrate = self.DHrate - self.CRIT_DHrate 
			self.f_CRIT = 1 + pureCRITrate * self.CRITmult
			self.f_DH = 1 + pureDHrate * self.DHmult
			self.f_CRIT_DH = 1 + self.CRIT_DHrate * self.CRIT_DHmult
		else:
			self.f_CRIT_DH = 1.0

		self.f_tot = self.f_CRIT * self.f_DH * self.f_CRIT_DH * self.f_DET * self.f_TEN

	def show(self):
		spacer = 20
		num2show = 5
		print('Stat results ')
		print(f"Crit DH modified: {self.CRIT_DH_mod}")
		print(' ')
		print(f"{'CRIT':<7}{'DET':<7}{'DH':<7}{'TEN':<7}")
		print(f"{self.CRIT:<7}{self.DET:<7}{self.DH:<7}{self.TEN:<7}")
		print(' ')
		print(f"{' ':<20}  {'Average multiplier':<20}  {'Hitrate (%)':<20}  {'Hit multiplier (%)':<20}")
		print(f"{'CRIT:':>20}  {round(self.f_CRIT, num2show):<20}  {round(self.CRITrate*100, num2show):<20}  +{round(self.CRITmult*100, num2show):<20}")
		print(f"{'DET:':>20}  {round(self.f_DET, num2show):<20}  {' ':<20}  {' ':<20}")
		print(f"{'DH:':>20}  {round(self.f_DH, num2show):<20}  {round(self.DHrate*100, num2show):<20}  +{round(self.DHmult*100, num2show):<20}")
		print(f"{'TEN:':>20}  {round(self.f_TEN, num2show):<20}  {' ':<20}  {' ':<20}")
		if self.CRIT_DH_mod == True:
			print(f"{'CRIT DH:':>20}  {round(self.f_CRIT_DH, num2show):<20}  {round(self.CRIT_DHrate*100, num2show):<20}  +{round(self.CRIT_DHmult*100, num2show):<20}")
		else:
			print(f"{'CRIT DH:':>20}  {'Not used':<20}  {round(self.CRIT_DHrate*100, num2show):<20}  +{round(self.CRIT_DHmult*100, num2show):<20}")
		print("-"*83)
		print(f"{'Total avg mult:':>20}  {round(self.f_tot, 5):<20}")
		print(' ')

#Functions to read the data in the spreadsheet
def DHmod(DH):
	f_DH = StatData.loc[StatData["DH stat"] <= DH, "f(DH) avg"].max()
	hitrate = StatData.loc[StatData["DH stat"] <= DH, "DH rate"].max()
	multiplier = 0.25
	return f_DH, hitrate, multiplier
	
def CRITmod(CRIT):
	f_CRIT = StatData.loc[StatData["CRIT stat"] <= CRIT, "f(CRIT) avg"].max()
	hitrate = StatData.loc[StatData["CRIT stat"] <= CRIT, "CRIT rate"].max()
	multiplier = StatData.loc[StatData["CRIT stat"] <= CRIT, "CRIT dmg"].max()
	return f_CRIT, hitrate, multiplier

def DETmod(DET):
	f_DET = StatData.loc[StatData["DET stat"] <= DET, "f(DET)"].max()
	return f_DET

def TENmod(TEN):
	if TEN < 400:
		f_TEN = 1.0
	else: 
		f_TEN = StatData.loc[StatData["TEN stat"] <= TEN, "f(TEN)"].max()
	return f_TEN

def RandDistfcn(Baseline, Distributable, Weights):
	divSet = np.random.randint(0, 1001, size=len(Baseline))
	divSet = [d * W for d, W in zip(divSet, Weights)]
	divSet = divSet/sum(divSet)

	RandDist = [Distributable * div for div in divSet]
	TotalStats = [B + R for B, R in zip(Baseline, RandDist)]
	TotalStats = [math.floor(num) for num in TotalStats]

	return TotalStats

def randOptimize(Baseline, Distributable, Weights, iterations, CRIT_DH_mod = True):
	f_tot = 0
	loadcheck = iterations / 10

	Start_time = time.time()
	print('Simulation start!')
	for i in range(1, iterations):

		if not i % loadcheck or i == 10000:
			Current_time = time.time()
			Elapsed_time = Current_time - Start_time
			time_per_tick = Elapsed_time / i
			ticks_left = iterations - i 
			time_left = ticks_left * time_per_tick
			prog = i/loadcheck * 10
			print(f"Progress: {prog}%")
			hours_left = math.floor(time_left / (60 * 60))
			seconds_left = time_left - hours_left * 60 * 60
			minutes_left = math.floor(seconds_left / 60)
			seconds_left = math.floor(seconds_left) - minutes_left * 60
			print(f"Estimated time left: {hours_left}:{minutes_left}:{seconds_left}")
			print(' ')
			print('Current best result: ')
			OptimalStats.show()


		TotalStats = RandDistfcn(Baseline, Distributable, Weights)

		#Max stat limit re-distribution
		StatLimits = [2994, 2996, 2998, 2984]
		outside_limit = True
		while outside_limit == True:
			redist_weight = [1, 1, 1, 1]
			redist = 0
			for i, m in enumerate(TotalStats):
				if m > StatLimits[i]:
					redist_weight[i] = 0
					redist += m - StatLimits[i]
					TotalStats[i] -= m - StatLimits[i]
			if redist > 0:
				TotalStats = RandDistfcn(TotalStats, redist, redist_weight)
			else:
				outside_limit = False

		if abs(sum(TotalStats) - (sum(Baseline) + Distributable)) > 10:
			print('Warning - Loss of stats during distribution!')

		res = data(*TotalStats, CRIT_DH_mod)
		new = res.f_tot

		if new > f_tot:
			f_tot = new
			OptimalStats = res

	print('-----Optimized stats-----')
	print(' ')
	OptimalStats.show()
	return OptimalStats

def DET_DH_balancer(Baseline, Distributable, CRIT_DH_mod = True):
	f_tot = 0
	loadcheck = Distributable / 10

	record = [[],[],[]]

	Start_time = time.time()
	print('Simulation start!')
	for i in range(0, Distributable + 1):

		if not i % loadcheck or i == 10000:
			Current_time = time.time()
			Elapsed_time = Current_time - Start_time
			time_per_tick = Elapsed_time / max(i,1)
			ticks_left = Distributable - i 
			time_left = ticks_left * time_per_tick
			prog = i/loadcheck * 10
			print(f"Progress: {prog}%")
			hours_left = math.floor(time_left / (60 * 60))
			seconds_left = time_left - hours_left * 60 * 60
			minutes_left = math.floor(seconds_left / 60)
			seconds_left = math.floor(seconds_left) - minutes_left * 60
			print(f"Estimated time left: {hours_left}:{minutes_left}:{seconds_left}")

		#Distribute stats
		DET = i 
		DH = Distributable - i

		TotalStats = [ B + D for B, D in zip(Baseline, [0, DET, DH, 0])]

		#Max stat limit re-distribution
		StatLimits = [2994, 2996, 2998, 2984]
		outside_limit = True
		while outside_limit == True:
			redist_weight = [1, 1, 1, 1]
			redist = 0
			for i, m in enumerate(TotalStats):
				if m > StatLimits[i]:
					redist_weight[i] = 0
					redist += m - StatLimits[i]
					TotalStats[i] -= m - StatLimits[i]
			if redist > 0:
				TotalStats = RandDistfcn(TotalStats, redist, redist_weight)
			else:
				outside_limit = False

		if abs(sum(TotalStats) - (sum(Baseline) + Distributable)) > 10:
			print('Warning - Loss of stats during distribution!')

		res = data(*TotalStats, CRIT_DH_mod)
		new = res.f_tot

		record[0].append(DET)
		record[1].append(DH)
		record[2].append(new)

		if new > f_tot:
			f_tot = new
			OptimalStats = res

	print('-----Optimized DET/DH ratio-----')
	print(' ')
	OptimalStats.show()
	return OptimalStats, record


#----------------------------------Main--------------------------------------#

#Stat library
DETBUILD = [2097, 1443, 436, 759]
CRITBUILD = [2097, 1119, 760, 759]
TESTBUILD = [2000, 1200, 2500,400] 

Weapon = [253, 177, 0, 0]
Naked = [653, 567, 472, 400]
Equipped = [2108, 1296, 928, 521]
Weights = [10, 1, 1, 0]


#DET/DH Balancer
Baseline = [2205, 400, 400, 527]
Distributable = 1612-400 + 868-400
DETDH_opt, record = DET_DH_balancer(Baseline, Distributable, CRIT_DH_mod = True)

plt.plot(record[0], record[2], '*')
plt.grid()
plt.show()

#RandOptimizer
#Baseline = [N - W for N, W in zip(Naked, Weapon)]
#Distributable = sum(Equipped) - sum(Baseline)
#OptimalStats = randOptimize(Baseline, Distributable, Weights, 100000, CRIT_DH_mod = True)


#Single instance
#s = data(696, 1657, 1673, 708, CRIT_DH_mod = False)
#s.show()



