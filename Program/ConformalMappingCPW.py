import math
from scipy.special import ellipe
import json
from pprint import pprint
from scipy import constants

from time import time
start_time = time()
print("starting")
print(time())

def print_time_from_start(msg):
    print(msg)
    print(time() - start_time)

# constants
relativePermittivityOfFreeSpace = constants.epsilon_0
SpeedOfLight = constants.speed_of_light

# read data in
with open('conf\configCPW.json') as data_file:
    data = json.load(data_file)

# Finding xa, xb and xc
S = data['Transmission_Line_Plates_Info']['Width_Of_Track']
S = float(S)
W = data['Transmission_Line_Plates_Info']['Width_Of_Gap']
W = float(W)
D = data['Transmission_Line_Plates_Info']['Width_Of_Ground']
D = float(D)
xa = S/2
xb = xa + W
xc = xb + D

print_time_from_start('done with xabc')

# Function to find C0
def findC0(xa, xb, xc):
    xasquared = xa**2
    xbsquared = math.pow(xb, 2)
    xcsquared = math.pow(xc, 2)
    kp1 = xc/xb
    kInsideSqurt = (xbsquared-xasquared)/(xcsquared-xasquared)
    kp2 = math.sqrt(kInsideSqurt)
    k = kp1*kp2
    ksquared = math.pow(k, 2)
    kder = math.sqrt(1-ksquared)
    K = ellipe(k)
    Kder = ellipe(kder)
    C0 = (4*relativePermittivityOfFreeSpace*Kder)/K
    return C0
# Function to find upper capacitances
def findCap(height, eff):
    coeffInSideBracketsa = (math.pi*xa)/(2*height)
    coeffInSideBracketsb = (math.pi*xb)/(2*height)
    coeffInSideBracketsc = (math.pi*xc)/(2*height)

    coeffa = math.sinh(coeffInSideBracketsa)
    coeffasquared = math.pow(coeffa, 2)
    coeffb = math.sinh(coeffInSideBracketsb)
    coeffbsquared = math.pow(coeffb, 2)
    coeffc = math.sinh(coeffInSideBracketsc)
    coeffcsquared = math.pow(coeffc, 2)

    kp1 = coeffc/coeffb
    kInsideSqurt = (coeffbsquared-coeffasquared)/(coeffcsquared-coeffasquared)
    kp2 = math.sqrt(kInsideSqurt)
    k = kp1*kp2
    ksquared = math.pow(k, 2)
    kder = math.sqrt(1-ksquared)
    K = ellipe(k)
    Kder = ellipe(kder)

    Kcoeff = Kder/K
    C = 2*relativePermittivityOfFreeSpace*eff*Kcoeff
    return C

####### Finding C0
C0 = findC0(xa, xb, xc)
print_time_from_start('find C0 done')

# Finding upper layer capacitances
i = 0
effs = []
heights = []
CapacitancesAbove = []

for section in data['Layers_Info']['Layers_Above']:
    eff = section['Relative_Permittivity']
    eff = float(eff)
    effs.append(eff)
    height = section['Height']
    height = float(height)
    heights.append(height)
    i = i + 1

print_time_from_start('finding caps')
j = 0
while j < i:
    eff = effs[j]
    height = heights[j]
    C = findCap(height, eff)
    CapacitancesAbove.append(C)
    j = j + 1
print_time_from_start('done finding caps')

OverallCapValueAbove = sum(CapacitancesAbove)

# Finding Lower layer capacitances
i = 0
effs = []
heights = []
CapacitancesBelow = []

for section in data['Layers_Info']['Layers_Below']:
    eff = section['Relative_Permittivity']
    eff = float(eff)
    effs.append(eff)
    height = section['Height']
    height = float(height)
    heights.append(height)
    i = i + 1

j = 0
while j < i:
    eff = effs[j]
    height = heights[j]
    C = findCap(height, eff)
    CapacitancesBelow.append(C)
    j = j + 1
print_time_from_start('done finding second caps')
OverallCapValueBelow = sum(CapacitancesBelow)

OverallLineCap = OverallCapValueBelow + OverallCapValueAbove + C0
effRelativePermittivityForWholeStructure = OverallLineCap/C0
effSquareRoot = math.sqrt(effRelativePermittivityForWholeStructure)
PhaseVelocity = SpeedOfLight/effSquareRoot
charateristicImpedance = 1/(OverallLineCap*PhaseVelocity)
print(charateristicImpedance)
print(effRelativePermittivityForWholeStructure)
print_time_from_start('finished total')
print('finished')
print(time())
