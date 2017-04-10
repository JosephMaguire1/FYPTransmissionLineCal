import math
from scipy.special import ellipe
import json
from pprint import pprint
from scipy import constants

# constants
relativePermittivityOfFreeSpace = constants.epsilon_0
SpeedOfLight = constants.speed_of_light
Pi = constants.pi

# read data in
with open('conf\configMicrostrip.json') as data_file:
    data = json.load(data_file)

W = data['Transmission_Line_Plates_Info']['Width_Of_Track']
W = float(W)

# find height of layers below
a = -1;
heights = []
for section in data['Layers_Info']['Layers_Below']:
    a = a + 1;
    height = section['Height']
    height = float(height)
    heights.append(height)
OverallHeightOfLayersBelow = heights[a]

a = math.log(17.08*((W/2*OverallHeightOfLayersBelow)+0.92))
Wef = W + (2*OverallHeightOfLayersBelow/Pi)*(a)

# function for finding filling factors for Layers below
def fillingFactor1(Wef, OverallHeightOfLayersBelow, height):
    Q = (height/2)*(1+(Pi/4)-(OverallHeightOfLayersBelow/Wef)*(math.log((2*Wef/OverallHeightOfLayersBelow)*((math.sin(Pi*height/2))*(height))+math.cos(Pi*height/2))))
    return Q

def fillingFactorM(Qminus1, Wef, OverallHeightOfLayersBelow):
    Q = 1 - ((OverallHeightOfLayersBelow/(2*Wef))*(math.log(((Pi)*(Wef/OverallHeightOfLayersBelow))-1))) - Qminus1
    return Q

def fillingFactorLayersBelow(Qminus1, Wef, OverallHeightOfLayersBelow, height):
    Q = (height/2)*(1+(Pi/4)-(OverallHeightOfLayersBelow/Wef)*(math.log((2*Wef/OverallHeightOfLayersBelow)*((math.sin(Pi*height/2))*(height))+math.cos(Pi*height/2))))-Qminus1
    return Q

# function for finding filling factors for Layers above
def fillingFactorMplusone(Wef, OverallHeightOfLayersBelow, height, V):
    Q = (OverallHeightOfLayersBelow/2*Wef)*(math.log(Pi*(Wef/OverallHeightOfLayersBelow)-1)-(1+V)*(math.log((2*Wef/OverallHeightOfLayersBelow)*((math.cos((Pi/2)*(V)))/(2*height-1+V))+math.sin((Pi/2)*(V)))))
    return Q

def fillingFactorN(sumfillingFactorsLB, sumfillingFactorsLA):
    Q = 1 - sumfillingFactorsLB - sumfillingFactorsLA
    return Q

def fillingFactorLayersAbove(Qminus1, Wef, OverallHeightOfLayersBelow, height, V):
    Q = (OverallHeightOfLayersBelow/2*Wef)*(math.log(Pi*(Wef/OverallHeightOfLayersBelow)-1)-(1+V)*(math.log((2*Wef/OverallHeightOfLayersBelow)*((math.cos((Pi/2)*(V)))/(2*height-1+V))+math.sin((Pi/2)*(V))))) - Qminus1
    return Q

# function for finding filling factors for Layers below
def fillingFactor1WGH(W, OverallHeightOfLayersBelow, height, A):
    Q = ((math.log(A))/(2*(math.log(8*OverallHeightOfLayersBelow/W))))*(1+(Pi/4)-(1/2)*(math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)))))
    return Q

def fillingFactorMWGH(Qminus1, W, OverallHeightOfLayersBelow):
    Q = (1/2) + (0.9/((Pi)*(math.log((8*OverallHeightOfLayersBelow)/(W))))) - Qminus1
    return Q

def fillingFactorLayersBelowWGH(Qminus1, W, OverallHeightOfLayersBelow, height, A):
    Q = ((math.log(A))/(2*(math.log(8*OverallHeightOfLayersBelow/W))))*(1+(Pi/4)-(1/2)*(math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)))))-Qminus1
    return Q

# function for finding filling factors for Layers above
def fillingFactorMplusoneWGH(W, OverallHeightOfLayersBelow, height, B):
    Q = 0.5 + (0.9+(Pi/4)*(math.log(B))*(math.acos((1-((1-((W/8*OverallHeightOfLayersBelow)/(height))))*(math.sqrt(B)))))/((Pi)*(math.log(8*OverallHeightOfLayersBelow/W))))
    return Q

def fillingFactorNWGH(sumfillingFactorsLB, sumfillingFactorsLA):
    Q = 1 - sumfillingFactorsLB - sumfillingFactorsLA
    return Q

def fillingFactorLayersAboveWGH(Qminus1, W, OverallHeightOfLayersBelow, height, B):
    Q = 0.5 + (0.9+(Pi/4)*(math.log(B))*(math.acos((1-((1-(W/8*OverallHeightOfLayersBelow)/(height)))*(math.sqrt(B)))))/((Pi)*(math.log(8*OverallHeightOfLayersBelow/W)))) - Qminus1
    return Q

if W/OverallHeightOfLayersBelow > 1:
    print("using 1st set of equtions")
    i = 0
    effsLB = []
    heightsLB = []
    fillingFactorsLB = []
    fillingFactorsLBDividedByEff = []

    for section in data['Layers_Info']['Layers_Below']:
        eff = section['Relative_Permittivity']
        eff = float(eff)
        effsLB.append(eff)
        height = section['Height']
        height = float(height)
        heightsLB.append(height)
        i = i + 1

    j = 0
    while j < i:
        eff = effsLB[j]
        height = heightsLB[j]/OverallHeightOfLayersBelow
        if j == 0:
            Q = fillingFactor1(Wef, OverallHeightOfLayersBelow, height)
            QDividedByEff = Q/eff
        elif j == i - 1:
            Qminus1 = fillingFactorsLB[j-1]
            Q = fillingFactorM(Qminus1, Wef, OverallHeightOfLayersBelow)
            QDividedByEff = Q/eff
        else:
            Qminus1 = fillingFactorsLB[j-1]
            Q = fillingFactorLayersBelow(Qminus1, Wef, OverallHeightOfLayersBelow, height)
            QDividedByEff = Q/eff
        fillingFactorsLB.append(Q)
        fillingFactorsLBDividedByEff.append(QDividedByEff)
        j = j + 1
    sumfillingFactorsLB = sum(fillingFactorsLB)
    sumfillingFactorsLBSquared = math.pow(sumfillingFactorsLB, 2)
    sumfillingFactorsLBDividedByEff = sum(fillingFactorsLBDividedByEff)
    effectivePermittivityLBCoeff = sumfillingFactorsLBSquared/sumfillingFactorsLBDividedByEff

    # layers above
    k = 0
    effsLA = []
    heightsLA = []
    fillingFactorsLA = []
    fillingFactorsLADividedByEff = []

    for section in data['Layers_Info']['Layers_Above']:
        eff = section['Relative_Permittivity']
        eff = float(eff)
        effsLA.append(eff)
        height = section['Height']
        height = float(height)
        heightsLA.append(height)
        k = k + 1

    l = 0
    while l < k:
        eff = effsLA[l]
        height = heightsLA[l]/OverallHeightOfLayersBelow
        if l == 0:
            vj = (2*OverallHeightOfLayersBelow/Pi)*(math.atan((Pi/((Pi/2)*(Wef/OverallHeightOfLayersBelow)-2)*(height-1))))
            V = vj/OverallHeightOfLayersBelow
            Q = fillingFactorMplusone(Wef, OverallHeightOfLayersBelow, height, V)
            QDividedByEff = Q/eff
        elif l == i - 1:
            sumfillingFactorsLA = sum(fillingFactorsLA)
            sumfillingFactorsLB = sum(fillingFactorsLB)
            Q = fillingFactorN(sumfillingFactorsLB, sumfillingFactorsLA)
            QDividedByEff = Q/eff
        else:
            Qminus1 = fillingFactorsLA[l-1]
            vj = (2*OverallHeightOfLayersBelow/Pi)*(math.atan((Pi/((Pi/2)*(Wef/OverallHeightOfLayersBelow)-2)*(height-1))))
            V = vj/OverallHeightOfLayersBelow
            Q = fillingFactorLayersAbove(Qminus1, Wef, OverallHeightOfLayersBelow, height, V)
            QDividedByEff = Q/eff
        fillingFactorsLA.append(Q)
        fillingFactorsLADividedByEff.append(QDividedByEff)
        l = l + 1
    sumfillingFactorsLA = sum(fillingFactorsLA)
    sumfillingFactorsLASquared = math.pow(sumfillingFactorsLA, 2)
    sumfillingFactorsLADividedByEff = sum(fillingFactorsLADividedByEff)
    effectivePermittivityLACoeff = sumfillingFactorsLASquared/sumfillingFactorsLADividedByEff

    effRelativePermittivityForWholeStructure = effectivePermittivityLACoeff + effectivePermittivityLBCoeff
    charateristicImpedance = ((120*Pi)/(math.sqrt(effRelativePermittivityForWholeStructure)))*(OverallHeightOfLayersBelow/Wef)
    print(charateristicImpedance)
    print(effRelativePermittivityForWholeStructure)
else:
    print("using 2nd set of equtions")
    i = 0
    effsLB = []
    heightsLB = []
    fillingFactorsLB = []
    fillingFactorsLBDividedByEff = []

    for section in data['Layers_Info']['Layers_Below']:
        eff = section['Relative_Permittivity']
        eff = float(eff)
        effsLB.append(eff)
        height = section['Height']
        height = float(height)
        heightsLB.append(height)
        i = i + 1

    j = 0
    while j < i:
        eff = effsLB[j]
        height = heightsLB[j]/OverallHeightOfLayersBelow
        if j == 0:
            A = (1+height)/(1-height+(W/4*OverallHeightOfLayersBelow))
            Q = fillingFactor1WGH(W, OverallHeightOfLayersBelow, height, A)
            QDividedByEff = Q/eff
        elif j == i - 1:
            Qminus1 = fillingFactorsLB[j-1]
            Q = fillingFactorMWGH(Qminus1, W, OverallHeightOfLayersBelow)
            QDividedByEff = Q/eff
        else:
            Qminus1 = fillingFactorsLB[j-1]
            A = (1+height)/(1-height+(W/4*OverallHeightOfLayersBelow))
            Q = fillingFactorLayersBelowWGH(Qminus1, W, OverallHeightOfLayersBelow, height, A)
            QDividedByEff = Q/eff
        fillingFactorsLB.append(Q)
        fillingFactorsLBDividedByEff.append(QDividedByEff)
        j = j + 1
    sumfillingFactorsLB = sum(fillingFactorsLB)
    sumfillingFactorsLBSquared = math.pow(sumfillingFactorsLB, 2)
    sumfillingFactorsLBDividedByEff = sum(fillingFactorsLBDividedByEff)
    effectivePermittivityLBCoeff = sumfillingFactorsLBSquared/sumfillingFactorsLBDividedByEff

    # layers above
    k = 0
    effsLA = []
    heightsLA = []
    fillingFactorsLA = []
    fillingFactorsLADividedByEff = []

    for section in data['Layers_Info']['Layers_Above']:
        eff = section['Relative_Permittivity']
        eff = float(eff)
        effsLA.append(eff)
        height = section['Height']
        height = float(height)
        heightsLA.append(height)
        k = k + 1

    l = 0
    while l < k:
        eff = effsLA[l]
        height = heightsLA[l]/OverallHeightOfLayersBelow
        if l == 0:
            B = (height+1)/(height+(W/4*OverallHeightOfLayersBelow)-1)
            Q = fillingFactorMplusoneWGH(W, OverallHeightOfLayersBelow, height, B)
            QDividedByEff = Q/eff
        elif l == i - 1:
            sumfillingFactorsLA = sum(fillingFactorsLA)
            sumfillingFactorsLB = sum(fillingFactorsLB)
            Q = fillingFactorNWGH(sumfillingFactorsLB, sumfillingFactorsLA)
            QDividedByEff = Q/eff
        else:
            B = (height+1)/(height+(W/4*OverallHeightOfLayersBelow)-1)
            Qminus1 = fillingFactorsLA[l-1]
            Q = fillingFactorLayersAboveWGH(Qminus1, W, OverallHeightOfLayersBelow, height, B)
            QDividedByEff = Q/eff
        fillingFactorsLA.append(Q)
        fillingFactorsLADividedByEff.append(QDividedByEff)
        l = l + 1
    sumfillingFactorsLA = sum(fillingFactorsLA)
    sumfillingFactorsLASquared = math.pow(sumfillingFactorsLA, 2)
    sumfillingFactorsLADividedByEff = sum(fillingFactorsLADividedByEff)
    effectivePermittivityLACoeff = sumfillingFactorsLASquared/sumfillingFactorsLADividedByEff

    effRelativePermittivityForWholeStructure = effectivePermittivityLACoeff + effectivePermittivityLBCoeff
    charateristicImpedance = ((120*Pi)/(math.sqrt(effRelativePermittivityForWholeStructure)))*(OverallHeightOfLayersBelow/Wef)
    print(charateristicImpedance)
    print(effRelativePermittivityForWholeStructure)
