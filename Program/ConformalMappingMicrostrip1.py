import math
from scipy.special import ellipe
import json
from pprint import pprint
from scipy import constants

# constants
relativePermittivityOfFreeSpace = constants.epsilon_0
SpeedOfLight = constants.speed_of_light
Pi = constants.pi

# function for finding filling factors for Layers below
def fillingFactor1(Wef, OverallHeightOfLayersBelow, height):
    print("---------------------------")
    print("OverallHeightOfLayersBelow is: ", OverallHeightOfLayersBelow)
    print("Wef is: ", Wef)
    print("height is: ", height)
    print("height/2 is: ", height/2)
    print("Pi/4 is: ", Pi/4)
    print("OverallHeightOfLayersBelow/Wef is: ", OverallHeightOfLayersBelow/Wef)
    print("(2*Wef)/(OverallHeightOfLayersBelow) is: ", (2*Wef)/(OverallHeightOfLayersBelow))
    print("(math.sin((Pi/2)*(height)))/(height) is: ", (math.sin((Pi/2)*(height)))/(height))
    print("math.log(((2*Wef)/(OverallHeightOfLayersBelow))*((math.sin((Pi/2)*(height)))/(height))+math.cos((Pi/2)*(height))) is:", (math.log(((2*Wef)/(OverallHeightOfLayersBelow))*((math.sin((Pi/2)*(height)))/(height))+math.cos((Pi/2)*(height)))))
    Q = (height/2)*(1+(Pi/4)-(OverallHeightOfLayersBelow/Wef)*(math.log(((2*Wef)/(OverallHeightOfLayersBelow))*((math.sin((Pi/2)*(height)))/(height))+math.cos((Pi/2)*(height)))))
    return Q

def fillingFactorM(Qminus1, Wef, OverallHeightOfLayersBelow):
    print("--------------")
    print("fillingFactorM")
    print("Qminus1 is:", Qminus1)
    print("Wef is:", Wef)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    Q = 1 - ((OverallHeightOfLayersBelow/(2*Wef))*(math.log(((Pi)*(Wef/OverallHeightOfLayersBelow))-1))) - Qminus1
    return Q

def fillingFactorLayersBelow(Qminus1, Wef, OverallHeightOfLayersBelow, height):
    print("--------------")
    print("fillingFactorLayersBelow")
    print("Qminus1 is:", Qminus1)
    print("Wef is:", Wef)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    print("height is:", height)
    Q = (height/2)*(1+(Pi/4)-(OverallHeightOfLayersBelow/Wef)*(math.log(((2*Wef)/(OverallHeightOfLayersBelow))*((math.sin((Pi/2)*(height)))/(height))+math.cos((Pi/2)*(height)))))-Qminus1
    return Q

# function for finding filling factors for Layers above
def fillingFactorMplusone(Wef, OverallHeightOfLayersBelow, height, V):
    print("--------------")
    print("fillingFactorMplusone")
    print("V is:", V)
    print("Wef is:", Wef)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    print("height is:", height)
    Q = (OverallHeightOfLayersBelow/(2*Wef))*(math.log((Pi)*(Wef/OverallHeightOfLayersBelow)-1)-(1+V)*(math.log(((2*Wef)/OverallHeightOfLayersBelow)*((math.cos((Pi/2)*(V)))/(2*height-1+V))+math.sin((Pi/2)*(V)))))
    return Q

def fillingFactorN(sumfillingFactorsLB, sumfillingFactorsLA):
    print("--------------")
    print("fillingFactorN")
    print("sumfillingFactorsLB is:", sumfillingFactorsLB)
    print("sumfillingFactorsLA is:", sumfillingFactorsLA)
    Q = 1 - sumfillingFactorsLB - sumfillingFactorsLA
    return Q

def fillingFactorLayersAbove(Qminus1, Wef, OverallHeightOfLayersBelow, height, V):
    print("--------------")
    print("fillingFactorLayersAbove")
    print("Qminus1 is:", Qminus1)
    print("Wef is:", Wef)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    print("height is:", height)
    print("V is:", V)
    Q = (OverallHeightOfLayersBelow/(2*Wef))*(math.log(Pi*(Wef/OverallHeightOfLayersBelow)-1)-(1+V)*(math.log(((2*Wef)/OverallHeightOfLayersBelow)*((math.cos((Pi/2)*(V)))/(2*height-1+V))+math.sin((Pi/2)*(V))))) - Qminus1
    return Q

# function for finding filling factors for Layers below
def fillingFactor1WGH(W, OverallHeightOfLayersBelow, height, A):
    print("--------------")
    print("fillingFactor1WGH")
    print("W is:", W)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    print("height is:", height)
    print("A is:", A)
    print("math.log(A) is:", math.log(A))
    print("2*(math.log((8*OverallHeightOfLayersBelow)/W)) is:", 2*(math.log((8*OverallHeightOfLayersBelow)/W)))
    print("(W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)) is:", (W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)))
    print("math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A))) is:", math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A))))
    print("1+(Pi/4)-(1/2)*(math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)))) is:", 1+(Pi/4)-(1/2)*(math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)))))
    Q = ((math.log(A))/(2*(math.log((8*OverallHeightOfLayersBelow)/W))))*(1+(Pi/4)-(1/2)*(math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)))))
    return Q

def fillingFactorMWGH(Qminus1, W, OverallHeightOfLayersBelow):
    print("--------------")
    print("fillingFactorMWGH")
    print("W is:", W)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    print("Qminus1 is:", Qminus1)
    Q = (1/2) + (0.9/((Pi)*(math.log((8*OverallHeightOfLayersBelow)/(W))))) - Qminus1
    return Q

def fillingFactorLayersBelowWGH(Qminus1, W, OverallHeightOfLayersBelow, height, A):
    print("--------------")
    print("fillingFactorLayersBelowWGH")
    print("W is:", W)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    print("Qminus1 is:", Qminus1)
    print("height is:", height)
    print("A is:", A)
    Q = ((math.log(A))/(2*(math.log((8*OverallHeightOfLayersBelow)/W))))*(1+(Pi/4)-(1/2)*(math.acos((W/(8*height*OverallHeightOfLayersBelow))*(math.sqrt(A)))))-Qminus1
    return Q

# function for finding filling factors for Layers above
def fillingFactorMplusoneWGH(W, OverallHeightOfLayersBelow, height, B):
    print("--------------")
    print("fillingFactorMplusoneWGH")
    print("W is:", W)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    print("height is:", height)
    print("B is:", B)
    Q = 0.5 - (0.9+((Pi/4)*(math.log(B))*(math.acos((1-((1-((W)/(8*OverallHeightOfLayersBelow)))/(height)))*(math.sqrt(B))))))/((Pi)*(math.log((8*OverallHeightOfLayersBelow)/W)))
    return Q

def fillingFactorNWGH(sumfillingFactorsLB, sumfillingFactorsLA):
    print("--------------")
    print("fillingFactorNWGH")
    print("sumfillingFactorsLB is:", sumfillingFactorsLB)
    print("sumfillingFactorsLA is:", sumfillingFactorsLA)
    Q = 1 - sumfillingFactorsLB - sumfillingFactorsLA
    return Q

def fillingFactorLayersAboveWGH(Qminus1, W, OverallHeightOfLayersBelow, height, B):
    print("--------------")
    print("fillingFactorLayersAboveWGH")
    print("W is:", W)
    print("OverallHeightOfLayersBelow is:", OverallHeightOfLayersBelow)
    print("Qminus1 is:", Qminus1)
    print("height is:", height)
    print("B is:", B)
    Q = 0.5 - (0.9+((Pi/4)*(math.log(B))*(math.acos((1-((1-((W)/(8*OverallHeightOfLayersBelow)))/(height)))*(math.sqrt(B))))))/((Pi)*(math.log((8*OverallHeightOfLayersBelow)/W))) - Qminus1
    return Q


def ConfomalMappingMicrostripCalculate(heights_above, heights_below, effsLA, effsLB, Width_Of_Track):
    print("Using This Method")
    W = Width_Of_Track
    print("W is:", W)

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

    OverallHeightOfLayersBelow = heightsLB[heights_below_length-1]
    print("OverallHeightOfLayersBelow is: ", OverallHeightOfLayersBelow)

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
    print("heightsLA is:", heightsLA)

    a = math.log(17.08*((W/(2*OverallHeightOfLayersBelow))+0.92))
    Wef = W + (2*OverallHeightOfLayersBelow/Pi)*(a)
    print("Wef is", Wef)

    if W/OverallHeightOfLayersBelow > 1:
        i = len(heights_below)
        fillingFactorsLB = []
        fillingFactorsLBDividedByEff = []

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
                print("---------------")
                print("Layers Below elif j == i - 1")
                print("heightminus1 is: ", heightminus1)
                print("Qminus1 is: ", Qminus1)
                Q = fillingFactorM(Qminus1, Wef, OverallHeightOfLayersBelow)
                QDividedByEff = Q/eff
            else:
                heightminus1 = heightsLB[j-1]/OverallHeightOfLayersBelow
                Qminus1 = fillingFactorLayersBelow(0.0, Wef, OverallHeightOfLayersBelow, heightminus1)
                print("---------------")
                print("Layers Below else")
                print("heightminus1 is: ", heightminus1)
                print("Qminus1 is: ", Qminus1)
                Q = fillingFactorLayersBelow(Qminus1, Wef, OverallHeightOfLayersBelow, height)
                QDividedByEff = Q/eff
            fillingFactorsLB.append(Q)
            fillingFactorsLBDividedByEff.append(QDividedByEff)
            print("------------------")
            print("Heights Below")
            print("j is: ", j)
            print("Q is: ", Q)
            print("QDividedByEff is: ", QDividedByEff)
            j = j + 1
        sumfillingFactorsLB = sum(fillingFactorsLB)
        sumfillingFactorsLBSquared = math.pow(sumfillingFactorsLB, 2)
        sumfillingFactorsLBDividedByEff = sum(fillingFactorsLBDividedByEff)
        effectivePermittivityLBCoeff = sumfillingFactorsLBSquared/sumfillingFactorsLBDividedByEff

        # layers above
        k = len(heights_above)
        fillingFactorsLA = []
        fillingFactorsLADividedByEff = []

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
                print("---------------")
                print("Layers Above else")
                print("heightminus1 is: ", heightminus1)
                print("vjminus1 is: ", vjminus1)
                print("Vminuse1 is ", Vminus1)
                print("Qminus1 is: ", Qminus1)
                vj = (2*OverallHeightOfLayersBelow/Pi)*(math.atan((Pi/((Pi/2)*(Wef/OverallHeightOfLayersBelow)-2)*(height-1))))
                V = vj/OverallHeightOfLayersBelow
                Q = fillingFactorLayersAbove(Qminus1, Wef, OverallHeightOfLayersBelow, height, V)
                QDividedByEff = Q/eff
            print("------------------")
            print("Heights Above")
            print("l is: ", l)
            print("Q is: ", Q)
            print("QDividedByEff is: ", QDividedByEff)
            fillingFactorsLA.append(Q)
            fillingFactorsLADividedByEff.append(QDividedByEff)
            l = l + 1

        print("----------------")
        print("N layer is air")

        sumfillingFactorsLA = sum(fillingFactorsLA)
        sumfillingFactorsLB = sum(fillingFactorsLB)
        Q = fillingFactorN(sumfillingFactorsLB, sumfillingFactorsLA)
        QDividedByEff = Q/eff
        print("Q is:", Q)
        print("QDividedByEff is:", QDividedByEff)
        fillingFactorsLA.append(Q)
        fillingFactorsLADividedByEff.append(QDividedByEff)

        print("-------------------")
        print("Calculations for Eff and Charateristic Impedance")
        sumfillingFactorsLA = sum(fillingFactorsLA)
        print("sumfillingFactorsLA is: ", sumfillingFactorsLA)
        print("fillingFactorsLA is: ", fillingFactorsLA)
        sumfillingFactorsLASquared = math.pow(sumfillingFactorsLA, 2)
        print("sumfillingFactorsLASquared is: ", sumfillingFactorsLASquared)
        sumfillingFactorsLADividedByEff = sum(fillingFactorsLADividedByEff)
        print("fillingFactorsLADividedByEff is: ", fillingFactorsLADividedByEff)
        print("sumfillingFactorsLADividedByEff is: ", sumfillingFactorsLADividedByEff)
        effectivePermittivityLACoeff = sumfillingFactorsLASquared/sumfillingFactorsLADividedByEff
        print("effectivePermittivityLACoeff is: ", effectivePermittivityLACoeff)
        effRelativePermittivityForWholeStructure = effectivePermittivityLACoeff + effectivePermittivityLBCoeff
        charateristicImpedance = ((120*Pi)/(math.sqrt(effRelativePermittivityForWholeStructure)))*(OverallHeightOfLayersBelow/Wef)
        print("effRelativePermittivityForWholeStructure is: ", effRelativePermittivityForWholeStructure)
        print("charateristicImpedance is: ", charateristicImpedance)
    else:
        i = len(heights_below)
        fillingFactorsLB = []
        fillingFactorsLBDividedByEff = []

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
            print("------------------")
            print("Heights Below")
            print("j is: ", j)
            print("Q is: ", Q)
            print("QDividedByEff is: ", QDividedByEff)
            fillingFactorsLB.append(Q)
            fillingFactorsLBDividedByEff.append(QDividedByEff)
            j = j + 1

        sumfillingFactorsLB = sum(fillingFactorsLB)
        sumfillingFactorsLBSquared = math.pow(sumfillingFactorsLB, 2)
        sumfillingFactorsLBDividedByEff = sum(fillingFactorsLBDividedByEff)
        effectivePermittivityLBCoeff = sumfillingFactorsLBSquared/sumfillingFactorsLBDividedByEff

        # layers above
        k = len(heights_above)
        fillingFactorsLA = []
        fillingFactorsLADividedByEff = []

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
            print("------------------")
            print("Heights Above")
            print("l is: ", l)
            print("Q is: ", Q)
            print("QDividedByEff is: ", QDividedByEff)
            fillingFactorsLA.append(Q)
            fillingFactorsLADividedByEff.append(QDividedByEff)
            l = l + 1

        print("----------------")
        print("N layer is air")
        sumfillingFactorsLA = sum(fillingFactorsLA)
        sumfillingFactorsLB = sum(fillingFactorsLB)
        Q = fillingFactorNWGH(sumfillingFactorsLB, sumfillingFactorsLA)
        QDividedByEff = Q/eff
        print("Q is:", Q)
        print("QDividedByEff is:", QDividedByEff)
        fillingFactorsLA.append(Q)
        fillingFactorsLADividedByEff.append(QDividedByEff)

        print("-------------------")
        print("Calculations for Eff and Charateristic Impedance")
        sumfillingFactorsLA = sum(fillingFactorsLA)
        print("sumfillingFactorsLA is: ", sumfillingFactorsLA)
        print("fillingFactorsLA is: ", fillingFactorsLA)
        sumfillingFactorsLASquared = math.pow(sumfillingFactorsLA, 2)
        print("sumfillingFactorsLASquared is: ", sumfillingFactorsLASquared)
        sumfillingFactorsLADividedByEff = sum(fillingFactorsLADividedByEff)
        print("fillingFactorsLADividedByEff is: ", fillingFactorsLADividedByEff)
        print("sumfillingFactorsLADividedByEff is: ", sumfillingFactorsLADividedByEff)
        effectivePermittivityLACoeff = sumfillingFactorsLASquared/sumfillingFactorsLADividedByEff
        print("effectivePermittivityLACoeff is: ", effectivePermittivityLACoeff)
        effRelativePermittivityForWholeStructure = effectivePermittivityLACoeff + effectivePermittivityLBCoeff
        charateristicImpedance = ((60)/(math.sqrt(effRelativePermittivityForWholeStructure)))*(math.log((8*OverallHeightOfLayersBelow)/(W)))
        print("effRelativePermittivityForWholeStructure is: ", effRelativePermittivityForWholeStructure)
        print("charateristicImpedance is: ", charateristicImpedance)
    return [effRelativePermittivityForWholeStructure, charateristicImpedance]
