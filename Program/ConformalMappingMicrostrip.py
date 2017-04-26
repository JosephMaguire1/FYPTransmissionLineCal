import math
from scipy.special import ellipe
import json
from scipy import constants

# constants
relativePermittivityOfFreeSpace = constants.epsilon_0
SpeedOfLight = constants.speed_of_light
Pi = constants.pi

# Functions for finding filling factors for Layers below when the width of the
# conductor is greater than the height of all the dielectric layers below the
# conductor
def fillingFactor1(Wef, OverallHeightOfLayersBelow, height):
    Q = (height/2)*(1+(Pi/4)-(OverallHeightOfLayersBelow/Wef)*(math.log(((2*Wef)/(OverallHeightOfLayersBelow))*((math.sin((Pi/2)*(height)))/(height))+math.cos((Pi/2)*(height)))))
    return Q

def fillingFactorM(Qminus1, Wef, OverallHeightOfLayersBelow):
    Q = 1 - ((OverallHeightOfLayersBelow/(2*Wef))*(math.log(((Pi)*(Wef/OverallHeightOfLayersBelow))-1))) - Qminus1
    return Q

def fillingFactorLayersBelow(Qminus1, Wef, OverallHeightOfLayersBelow, height):
    Q = (height/2)*(1+(Pi/4)-(OverallHeightOfLayersBelow/Wef)*(math.log(((2*Wef)/(OverallHeightOfLayersBelow))*((math.sin((Pi/2)*(height)))/(height))+math.cos((Pi/2)*(height)))))-Qminus1
    return Q

# Functions for finding filling factors for Layers above when the width of the
# conductor is greater than the height of all the dielectric layers below the
# conductor
def fillingFactorMplusone(Wef, OverallHeightOfLayersBelow, height, V):
    Q = (OverallHeightOfLayersBelow/(2*Wef))*(math.log((Pi)*(Wef/OverallHeightOfLayersBelow)-1)-(1+V)*(math.log(((2*Wef)/OverallHeightOfLayersBelow)*((math.cos((Pi/2)*(V)))/(2*height-1+V))+math.sin((Pi/2)*(V)))))
    return Q

def fillingFactorN(sumfillingFactorsLB, sumfillingFactorsLA):
    Q = 1 - sumfillingFactorsLB - sumfillingFactorsLA
    return Q

def fillingFactorLayersAbove(Qminus1, Wef, OverallHeightOfLayersBelow, height, V):
    Q = (OverallHeightOfLayersBelow/(2*Wef))*(math.log(Pi*(Wef/OverallHeightOfLayersBelow)-1)-(1+V)*(math.log(((2*Wef)/OverallHeightOfLayersBelow)*((math.cos((Pi/2)*(V)))/(2*height-1+V))+math.sin((Pi/2)*(V))))) - Qminus1
    return Q

# Functions for finding filling factors for Layers below when the width of the
# conductor is less than the height of all the dielectric layers below the
# conductor
def fillingFactor1WGH(W, OverallHeightOfLayersBelow, height, A):
    Q = ((math.log(A))/(2*(math.log((8*OverallHeightOfLayersBelow)/W))))*(1+(Pi/4)-(1/2)*(math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(abs(A))))))
    return Q

def fillingFactorMWGH(Qminus1, W, OverallHeightOfLayersBelow):
    Q = (1/2) + (0.9/((Pi)*(math.log((8*OverallHeightOfLayersBelow)/(W))))) - Qminus1
    return Q

def fillingFactorLayersBelowWGH(Qminus1, W, OverallHeightOfLayersBelow, height, A):
    Q = ((math.log(A))/(2*(math.log((8*OverallHeightOfLayersBelow)/W))))*(1+(Pi/4)-(1/2)*(math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)))))-Qminus1
    return Q

# Functions for finding filling factors for Layers above when the width of the
# conductor is less than the height of all the dielectric layers below the
# conductor
def fillingFactorMplusoneWGH(W, OverallHeightOfLayersBelow, height, B):
    Q = 0.5 - (0.9+((Pi/4)*(math.log(B))*(math.acos((1-((1-((W)/(8*OverallHeightOfLayersBelow)))/(height)))*(math.sqrt(B))))))/((Pi)*(math.log((8*OverallHeightOfLayersBelow)/W)))
    return Q

def fillingFactorNWGH(sumfillingFactorsLB, sumfillingFactorsLA):
    Q = 1 - sumfillingFactorsLB - sumfillingFactorsLA
    return Q

def fillingFactorLayersAboveWGH(Qminus1, W, OverallHeightOfLayersBelow, height, B):
    Q = 0.5 - (0.9+((Pi/4)*(math.log(B))*(math.acos((1-((1-((W)/(8*OverallHeightOfLayersBelow)))/(height)))*(math.sqrt(B))))))/((Pi)*(math.log((8*OverallHeightOfLayersBelow)/W))) - Qminus1
    return Q

# Function to calculate the charateristic impedance and relative permittivity
# for Microstrip transmission line
def ConfomalMappingMicrostripCalculate(heights_above, heights_below, effsLA, effsLB, Width_Of_Track, Thickness_Of_Conductor):
    W = Width_Of_Track

    # Calculate heights of layers below from ground plate
    heightsLB = []
    heights_below_length = len(heights_below)
    for i in range(0, heights_below_length):
        if i == 0:
            height = heights_below[i]
            heightsLB.append(height)
        else:
            height = heightsLB[i-1] + heights_below[i]
            heightsLB.append(height)

    # If there is only one dielectric layer present below the conductor split
    # that dielectric layer into two dielectric layers with each having a
    # height equal to half the height of the orginal dielectric layer and each
    # having a the same dielectric constant as the orginal dielectric layer
    if heights_below_length == 1:
        height = heightsLB[0]
        heightDiv2 = height/2
        heightsLB = []
        heightsLB.append(heightDiv2)
        heightsLB.append(height)
        eff = effsLB[0]
        effsLB.append(eff)
        heights_below_length = 2

    OverallHeightOfLayersBelow = heightsLB[heights_below_length-1]

    # Calculate heights of layers above from ground plate
    heightsLA = []
    heights_above_length = len(heights_above)
    for j in range(0, heights_above_length):
        if j == 0:
            height = OverallHeightOfLayersBelow + heights_above[j]
            heightsLA.append(height)
        else:
            height = heightsLA[j-1] + heights_above[j]
            heightsLA.append(height)

    # If the Thickness of the conductor is included use the modified formulation
    if Thickness_Of_Conductor > 0:
        Wef = W + (2*OverallHeightOfLayersBelow/Pi)*(math.log(17.08*((W/(2*OverallHeightOfLayersBelow))+0.92))) + (1.25/Pi)*(Thickness_Of_Conductor)*(1+math.log((2*OverallHeightOfLayersBelow)/(Thickness_Of_Conductor)))
    else:
        Wef = W + (2*OverallHeightOfLayersBelow/Pi)*(math.log(17.08*((W/(2*OverallHeightOfLayersBelow))+0.92)))

    if W/OverallHeightOfLayersBelow > 1:
        i = len(heightsLB)
        fillingFactorsLB = []
        fillingFactorsLBDividedByEff = []

        # Find filling factors of dielectric layers below the conductor
        j = 0
        while j < i:
            eff = effsLB[j]
            height = heightsLB[j]/OverallHeightOfLayersBelow
            if j == 0:
                Q = fillingFactor1(Wef, OverallHeightOfLayersBelow, height)
                QDividedByEff = Q/eff
            elif j == i - 1:
                heightminus1 = heightsLB[j-1]/OverallHeightOfLayersBelow
                Qminus1 = fillingFactorLayersBelow(0.0, Wef, OverallHeightOfLayersBelow, heightminus1)
                Q = fillingFactorM(Qminus1, Wef, OverallHeightOfLayersBelow)
                QDividedByEff = Q/eff
            else:
                heightminus1 = heightsLB[j-1]/OverallHeightOfLayersBelow
                Qminus1 = fillingFactorLayersBelow(0.0, Wef, OverallHeightOfLayersBelow, heightminus1)
                Q = fillingFactorLayersBelow(Qminus1, Wef, OverallHeightOfLayersBelow, height)
                QDividedByEff = Q/eff
            fillingFactorsLB.append(Q)
            fillingFactorsLBDividedByEff.append(QDividedByEff)
            j = j + 1
        sumfillingFactorsLB = sum(fillingFactorsLB)
        sumfillingFactorsLBSquared = math.pow(sumfillingFactorsLB, 2)
        sumfillingFactorsLBDividedByEff = sum(fillingFactorsLBDividedByEff)
        effectivePermittivityLBCoeff = sumfillingFactorsLBSquared/sumfillingFactorsLBDividedByEff

        k = len(heights_above)
        fillingFactorsLA = []
        fillingFactorsLADividedByEff = []

        # Find filling factors of dielectric layers above the conductor
        l = 0
        while l < k:
            eff = effsLA[l]
            height = heightsLA[l]/OverallHeightOfLayersBelow
            if l == 0:
                vj = ((2*OverallHeightOfLayersBelow)/Pi)*(math.atan((Pi/((Pi/2)*(Wef/OverallHeightOfLayersBelow)-2)*(height-1))))
                V = vj/OverallHeightOfLayersBelow
                Q = fillingFactorMplusone(Wef, OverallHeightOfLayersBelow, height, V)
                QDividedByEff = Q/eff
            else:
                heightminus1 = heightsLA[l-1]
                vjminus1 = (2*OverallHeightOfLayersBelow/Pi)*(math.atan((Pi/((Pi/2)*(Wef/OverallHeightOfLayersBelow)-2)*(heightminus1-1))))
                Vminus1 = vjminus1/OverallHeightOfLayersBelow
                Qminus1 = fillingFactorLayersAbove(0.0, Wef, OverallHeightOfLayersBelow, heightminus1, Vminus1)
                vj = (2*OverallHeightOfLayersBelow/Pi)*(math.atan((Pi/((Pi/2)*(Wef/OverallHeightOfLayersBelow)-2)*(height-1))))
                V = vj/OverallHeightOfLayersBelow
                Q = fillingFactorLayersAbove(Qminus1, Wef, OverallHeightOfLayersBelow, height, V)
                QDividedByEff = Q/eff
            fillingFactorsLA.append(Q)
            fillingFactorsLADividedByEff.append(QDividedByEff)
            l = l + 1

        sumfillingFactorsLA = sum(fillingFactorsLA)
        sumfillingFactorsLB = sum(fillingFactorsLB)
        Q = fillingFactorN(sumfillingFactorsLB, sumfillingFactorsLA)
        QDividedByEff = Q/eff
        fillingFactorsLA.append(Q)
        fillingFactorsLADividedByEff.append(QDividedByEff)

        # Use information found to calculate the charateristic impedance and
        # relative permittivity of structure
        sumfillingFactorsLA = sum(fillingFactorsLA)
        sumfillingFactorsLASquared = math.pow(sumfillingFactorsLA, 2)
        sumfillingFactorsLADividedByEff = sum(fillingFactorsLADividedByEff)
        effectivePermittivityLACoeff = sumfillingFactorsLASquared/sumfillingFactorsLADividedByEff
        effRelativePermittivityForWholeStructure = effectivePermittivityLACoeff + effectivePermittivityLBCoeff
        charateristicImpedance = ((120*Pi)/(math.sqrt(effRelativePermittivityForWholeStructure)))*(OverallHeightOfLayersBelow/Wef)
        effRelativePermittivityForWholeStructure = format(effRelativePermittivityForWholeStructure, '.2f')
        charateristicImpedance = format(charateristicImpedance, '.2f')
    else:
        i = len(heightsLB)
        fillingFactorsLB = []
        fillingFactorsLBDividedByEff = []

        # Find filling factors of dielectric layers below the conductor
        j = 0
        while j < i:
            eff = effsLB[j]
            height = heightsLB[j]/OverallHeightOfLayersBelow
            if j == 0:
                A = (1+height)/(1-height+(W/(4*OverallHeightOfLayersBelow)))
                Q = fillingFactor1WGH(W, OverallHeightOfLayersBelow, height, A)
                QDividedByEff = Q/eff
            elif j == i - 1:
                heightminus1 = heightsLB[j-1]/OverallHeightOfLayersBelow
                Aminus1 = (1+heightminus1)/(1-heightminus1+(W/(4*OverallHeightOfLayersBelow)))
                Qminus1 = fillingFactorLayersBelowWGH(0.0, W, OverallHeightOfLayersBelow, heightminus1, Aminus1)
                Q = fillingFactorMWGH(Qminus1, W, OverallHeightOfLayersBelow)
                QDividedByEff = Q/eff
            else:
                heightminus1 = heightsLB[j-1]/OverallHeightOfLayersBelow
                Aminus1 = (1+heightminus1)/(1-heightminus1+(W/(4*OverallHeightOfLayersBelow)))
                Qminus1 = fillingFactorLayersBelowWGH(0.0, W, OverallHeightOfLayersBelow, heightminus1, Aminus1)
                A = (1+height)/(1-height+(W/(4*OverallHeightOfLayersBelow)))
                Q = fillingFactorLayersBelowWGH(Qminus1, W, OverallHeightOfLayersBelow, height, A)
                QDividedByEff = Q/eff
            fillingFactorsLB.append(Q)
            fillingFactorsLBDividedByEff.append(QDividedByEff)
            j = j + 1

        sumfillingFactorsLB = sum(fillingFactorsLB)
        sumfillingFactorsLBSquared = math.pow(sumfillingFactorsLB, 2)
        sumfillingFactorsLBDividedByEff = sum(fillingFactorsLBDividedByEff)
        effectivePermittivityLBCoeff = sumfillingFactorsLBSquared/sumfillingFactorsLBDividedByEff

        k = len(heights_above)
        fillingFactorsLA = []
        fillingFactorsLADividedByEff = []

        # Find filling factors of dielectric layers above the conductor
        l = 0
        while l < k:
            eff = effsLA[l]
            height = heightsLA[l]/OverallHeightOfLayersBelow
            if l == 0:
                B = (height+1)/(height+(W/(4*OverallHeightOfLayersBelow))-1)
                Q = fillingFactorMplusoneWGH(W, OverallHeightOfLayersBelow, height, B)
                QDividedByEff = Q/eff
            else:
                heightminus1 = heightsLA[l-1]/OverallHeightOfLayersBelow
                Bminus1 = (heightminus1+1)/(heightminus1+(W/(4*OverallHeightOfLayersBelow))-1)
                Qminus1 = fillingFactorLayersAboveWGH(0.0, W, OverallHeightOfLayersBelow, heightminus1, Bminus1)
                B = (height+1)/(height+(W/(4*OverallHeightOfLayersBelow))-1)
                Q = fillingFactorLayersAboveWGH(Qminus1, W, OverallHeightOfLayersBelow, height, B)
                QDividedByEff = Q/eff
            fillingFactorsLA.append(Q)
            fillingFactorsLADividedByEff.append(QDividedByEff)
            l = l + 1

        sumfillingFactorsLA = sum(fillingFactorsLA)
        sumfillingFactorsLB = sum(fillingFactorsLB)
        Q = fillingFactorNWGH(sumfillingFactorsLB, sumfillingFactorsLA)
        QDividedByEff = Q/eff
        fillingFactorsLA.append(Q)
        fillingFactorsLADividedByEff.append(QDividedByEff)

        # Use information found to calculate the charateristic impedance and
        # relative permittivity of structure
        sumfillingFactorsLA = sum(fillingFactorsLA)
        sumfillingFactorsLASquared = math.pow(sumfillingFactorsLA, 2)
        sumfillingFactorsLADividedByEff = sum(fillingFactorsLADividedByEff)
        effectivePermittivityLACoeff = sumfillingFactorsLASquared/sumfillingFactorsLADividedByEff
        effRelativePermittivityForWholeStructure = effectivePermittivityLACoeff + effectivePermittivityLBCoeff
        charateristicImpedance = ((60)/(math.sqrt(effRelativePermittivityForWholeStructure)))*(math.log((8*OverallHeightOfLayersBelow)/(W)))
        effRelativePermittivityForWholeStructure = format(effRelativePermittivityForWholeStructure, '.2f')
        charateristicImpedance = format(charateristicImpedance, '.2f')
    return [effRelativePermittivityForWholeStructure, charateristicImpedance]
