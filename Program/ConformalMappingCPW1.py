import math
from scipy.special import ellipk
import json
from pprint import pprint
from scipy import constants

# constants
relativePermittivityOfFreeSpace = constants.epsilon_0
SpeedOfLight = constants.speed_of_light

def ConfomalMappingCPWCalculate(heights_above, heights_below, effsLA, effsLB, Width_Of_Track, Width_Of_Gap, Width_Of_Ground):
    # Finding xa, xb and xc
    S = Width_Of_Track
    W = Width_Of_Gap
    D = Width_Of_Ground
    xa = S/2
    xb = xa + W
    xc = xb + D
    effsLA = effsLA
    effsLB = effsLB

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
        K = ellipk(k)
        Kder = ellipk(kder)
        C0 = (4*relativePermittivityOfFreeSpace*Kder)/K
        print("---------------")
        print("Calculating C0")
        print("kp1 is:", kp1)
        print("kInsideSqurt is:", kInsideSqurt)
        print("kp2 is:", kp2)
        print("k is:", k)
        print("kder is:", kder)
        print("K is:", K)
        print("Kder is:", Kder)
        print("C0 is:", C0)
        return C0

    # Function to find upper capacitances
    def findCap(height, eff):
        print("--------------")
        print("height is:", height)
        print("math.pi is ", math.pi)
        coeffInSideBracketsa = (math.pi*xa)/(2*height)
        coeffInSideBracketsb = (math.pi*xb)/(2*height)
        coeffInSideBracketsc = (math.pi*xc)/(2*height)

        coeffa = math.sinh(coeffInSideBracketsa)
        coeffasquared = math.pow(coeffa, 2)
        print("coeffInSideBracketsb is: ", coeffInSideBracketsb)
        coeffb = math.sinh(coeffInSideBracketsb)
        print("coeffb is: ", coeffb)
        coeffbsquared = math.pow(coeffb, 2)
        coeffc = math.sinh(coeffInSideBracketsc)
        coeffcsquared = math.pow(coeffc, 2)

        kp1 = coeffc/coeffb
        kInsideSqurt = (coeffbsquared-coeffasquared)/(coeffcsquared-coeffasquared)
        kp2 = math.sqrt(kInsideSqurt)
        k = kp1*kp2
        ksquared = math.pow(k, 2)
        kder = math.sqrt(1-ksquared)
        K = ellipk(k)
        Kder = ellipk(kder)

        Kcoeff = Kder/K

        C = 2*relativePermittivityOfFreeSpace*eff*Kcoeff
        print("---------------")
        print("height is:", height)
        print("coeffa is:", coeffa)
        print("coeffasquared is:", coeffasquared)
        print("coeffb is:", coeffb)
        print("coeffbsquared is:", coeffbsquared)
        print("coeffc is:", coeffc)
        print("coeffcsquared is:", coeffcsquared)
        print("Calculating C")
        print("kp1 is:", kp1)
        print("kInsideSqurt is:", kInsideSqurt)
        print("kp2 is:", kp2)
        print("k is:", k)
        print("kder is:", kder)
        print("K is:", K)
        print("Kder is:", Kder)
        print("C is:", C)
        print("Kcoeff is:", Kcoeff)
        print("relativePermittivityOfFreeSpace is:", relativePermittivityOfFreeSpace)
        print("eff is:", eff)
        return C

    ####### Finding C0
    C0 = findC0(xa, xb, xc)
    print("---------------")
    print("C0 is: ", C0)

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

    # Calculate heights of layers above from ground plate
    heightsLA = []
    heights_above_length = len(heights_above)
    for j in range(0, heights_above_length):
        if j == 0:
            height = heights_above[j]
            heightsLA.append(height)
        else:
            height = heightsLA[j-1] + heights_above[j]
            heightsLA.append(height)

    print("effsLA is: ", effsLA)


    CapacitancesAbove = []
    k = 0
    while k < heights_above_length:
        if k == heights_above_length - 1:
            eff = effsLA[k] - 1
            print("eff is: ", eff)
            height = heightsLA[k]
            C = findCap(height, eff)
            CapacitancesAbove.append(C)
        else:
            eff = effsLA[k] - effsLA[k+1]
            print("eff is: ", eff)
            print("effsLA[k] is: ", effsLA[k])
            print("effsLA[k+1] is: ", effsLA[k+1])
            height = heightsLA[k]
            C = findCap(height, eff)
            CapacitancesAbove.append(C)
        k = k + 1

    OverallCapValueAbove = sum(CapacitancesAbove)
    print("---------------")
    print("CapacitancesAbove is:", CapacitancesAbove)
    print("OverallCapValueAbove is:", OverallCapValueAbove)
    # Finding Lower layer capacitances
    print("effsLB is:", effsLB)

    CapacitancesBelow = []
    l = 0
    while l < heights_below_length:
        if l == heights_below_length - 1:
            eff = effsLB[l] - 1
            height = heightsLB[l]
            C = findCap(height, eff)
            CapacitancesBelow.append(C)
        else:
            eff = effsLB[l] - effsLB[l+1]
            height = heightsLB[l]
            C = findCap(height, eff)
            CapacitancesBelow.append(C)
        l = l + 1

    OverallCapValueBelow = sum(CapacitancesBelow)
    print("---------------")
    print("OverallCapValueBelow is: ", OverallCapValueBelow)
    print("CapacitancesBelow is: ", CapacitancesBelow)
    OverallLineCap = OverallCapValueBelow + OverallCapValueAbove + C0
    effRelativePermittivityForWholeStructure = OverallLineCap/C0
    effSquareRoot = math.sqrt(effRelativePermittivityForWholeStructure)
    PhaseVelocity = SpeedOfLight/effSquareRoot
    charateristicImpedance = 1/(OverallLineCap*PhaseVelocity)

    return [effRelativePermittivityForWholeStructure, charateristicImpedance]

def ConfomalMappingCPWCalculateGroundLayerIncluded(heights_above, heights_below, effsLA, effsLB, Width_Of_Track, Width_Of_Gap, Width_Of_Ground):
    # Finding xa, xb and xc
    S = Width_Of_Track
    W = Width_Of_Gap
    D = Width_Of_Ground
    xa = S/2
    xb = xa + W
    xc = xb + D
    effsLA = effsLA
    effsLB = effsLB

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
        K = ellipk(k)
        Kder = ellipk(kder)
        C0 = (4*relativePermittivityOfFreeSpace*Kder)/K
        print("---------------")
        print("Calculating C0")
        print("kp1 is:", kp1)
        print("kInsideSqurt is:", kInsideSqurt)
        print("kp2 is:", kp2)
        print("k is:", k)
        print("kder is:", kder)
        print("K is:", K)
        print("Kder is:", Kder)
        print("C0 is:", C0)
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
        K = ellipk(k)
        Kder = ellipk(kder)

        Kcoeff = Kder/K

        C = 2*relativePermittivityOfFreeSpace*eff*Kcoeff
        print("---------------")
        print("height is:", height)
        print("coeffa is:", coeffa)
        print("coeffasquared is:", coeffasquared)
        print("coeffb is:", coeffb)
        print("coeffbsquared is:", coeffbsquared)
        print("coeffc is:", coeffc)
        print("coeffcsquared is:", coeffcsquared)
        print("Calculating C")
        print("kp1 is:", kp1)
        print("kInsideSqurt is:", kInsideSqurt)
        print("kp2 is:", kp2)
        print("k is:", k)
        print("kder is:", kder)
        print("K is:", K)
        print("Kder is:", Kder)
        print("C is:", C)
        print("Kcoeff is:", Kcoeff)
        print("relativePermittivityOfFreeSpace is:", relativePermittivityOfFreeSpace)
        print("eff is:", eff)
        return C

    ####### Finding C0
    C0 = findC0(xa, xb, xc)
    print("---------------")
    print("C0 is: ", C0)

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

    # Calculate heights of layers above from ground plate
    heightsLA = []
    heights_above_length = len(heights_above)
    for j in range(0, heights_above_length):
        if j == 0:
            height = heights_above[j]
            heightsLA.append(height)
        else:
            height = heightsLA[j-1] + heights_above[j]
            heightsLA.append(height)

    print("effsLA is: ", effsLA)


    CapacitancesAbove = []
    k = 0
    while k < heights_above_length:
        if k == heights_above_length - 1:
            eff = effsLA[k] - 1
            print("eff is: ", eff)
            height = heightsLA[k]
            C = findCap(height, eff)
            CapacitancesAbove.append(C)
        else:
            eff = effsLA[k] - effsLA[k+1]
            print("eff is: ", eff)
            print("effsLA[k] is: ", effsLA[k])
            print("effsLA[k+1] is: ", effsLA[k+1])
            height = heightsLA[k]
            C = findCap(height, eff)
            CapacitancesAbove.append(C)
        k = k + 1

    OverallCapValueAbove = sum(CapacitancesAbove)
    print("---------------")
    print("CapacitancesAbove is:", CapacitancesAbove)
    print("OverallCapValueAbove is:", OverallCapValueAbove)
    # Finding Lower layer capacitances
    print("effsLB is:", effsLB)

    CapacitancesBelow = []
    l = 0
    while l < heights_below_length:
        if l == heights_below_length - 1:
            eff = effsLB[l] - 1
            height = heightsLB[l]
            C = findCap(height, eff)
            CapacitancesBelow.append(C)
        else:
            eff = effsLB[l] - effsLB[l+1]
            height = heightsLB[l]
            C = findCap(height, eff)
            CapacitancesBelow.append(C)
        l = l + 1

    heightsDiveffs = []
    a = 0
    while a < heights_below_length:
        height = heights_below[a]
        eff = effsLB[a]
        heightDiveff = height/eff
        heightsDiveffs.append(heightDiveff)

    sumofheightsDiveffs = sum(heightsDiveffs)
    CapacitancesDueToGround = (relativePermittivityOfFreeSpace*W)/(sumofheightsDiveffs)

    OverallCapValueBelow = sum(CapacitancesBelow)
    print("---------------")
    print("OverallCapValueBelow is: ", OverallCapValueBelow)
    print("CapacitancesBelow is: ", CapacitancesBelow)
    OverallLineCap = OverallCapValueBelow + OverallCapValueAbove + C0 + CapacitancesDueToGround
    effRelativePermittivityForWholeStructure = OverallLineCap/C0
    effSquareRoot = math.sqrt(effRelativePermittivityForWholeStructure)
    PhaseVelocity = SpeedOfLight/effSquareRoot
    charateristicImpedance = 1/(OverallLineCap*PhaseVelocity)

    return [effRelativePermittivityForWholeStructure, charateristicImpedance]
