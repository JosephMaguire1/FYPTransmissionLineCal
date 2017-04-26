import math
from scipy.special import ellipk
import json
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

    # Custom Sinh funcion
    def customSinh(x):
        if x > 10:
            return 0
        else:
            return 1/math.sinh(x)

    # Function to find C0
    def findC0(xa, xb, xc):
        xasquared = xa**2
        xbsquared = xb**2
        xcsquared = xc**2

        kp1 = xc/xb
        kInsideSqurt = (xbsquared-xasquared)/(xcsquared-xasquared)
        kp2 = math.sqrt(kInsideSqurt)
        k = kp1*kp2
        ksquared = k**2
        kder = math.sqrt(1-ksquared)
        kdersquared = kder**2

        K = ellipk(ksquared)
        Kder = ellipk(kdersquared)

        C0 = (4*relativePermittivityOfFreeSpace*Kder)/K
        return C0

    # Function to find line capacitances when dielctric layer present
    def findCap(height, eff):
        coeffInSideBracketsa = (math.pi*xa)/(2*height)
        coeffInSideBracketsb = (math.pi*xb)/(2*height)
        coeffInSideBracketsc = (math.pi*xc)/(2*height)

        coeffa = math.sinh(coeffInSideBracketsa)
        coeffasquared = coeffa**2

        coeffb = math.sinh(coeffInSideBracketsb)
        coeffbsquared = coeffb**2

        coeffc = customSinh(coeffInSideBracketsc)
        coeffcsquared = coeffc**2

        kp1 = 1.0/coeffb
        kInsideSqurt = (coeffbsquared-coeffasquared)/(1-coeffasquared*coeffcsquared)
        kp2 = math.sqrt(kInsideSqurt)
        k = kp1*kp2
        ksquared = k**2
        kder = math.sqrt(1-ksquared)
        kdersquared = kder**2

        K = ellipk(ksquared)
        Kder = ellipk(kdersquared)

        Kcoeff = Kder/K

        C = 2*relativePermittivityOfFreeSpace*eff*Kcoeff
        return C

    # Finding C0
    C0 = findC0(xa, xb, xc)

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

    # Find capacitances due to dielectric layers above conductor
    CapacitancesAbove = []
    k = 0
    while k < heights_above_length:
        if k == heights_above_length - 1:
            eff = effsLA[k] - 1
            height = heightsLA[k]
            C = findCap(height, eff)
            CapacitancesAbove.append(C)
        else:
            eff = effsLA[k] - effsLA[k+1]
            height = heightsLA[k]
            C = findCap(height, eff)
            CapacitancesAbove.append(C)
        k = k + 1
    OverallCapValueAbove = sum(CapacitancesAbove)

    # Find capacitances due to dielectric layers below conductor
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

    # Find relativer permittive and charateristic impedance of transmission line from
    # capacitances values already obtained
    OverallLineCap = OverallCapValueBelow + OverallCapValueAbove + C0
    effRelativePermittivityForWholeStructure = OverallLineCap/C0
    effSquareRoot = math.sqrt(effRelativePermittivityForWholeStructure)
    PhaseVelocity = SpeedOfLight/effSquareRoot
    charateristicImpedance = 1/(OverallLineCap*PhaseVelocity)
    effRelativePermittivityForWholeStructure = format(effRelativePermittivityForWholeStructure, '.2f')
    charateristicImpedance = format(charateristicImpedance, '.2f')

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
    def customSinh(x):
        if x > 10:
            return 0
        else:
            return 1/math.sinh(x)

    # Function to find C0
    def findC0(xa, xb, xc):
        xasquared = xa**2
        xbsquared = xb**2
        xcsquared = xc**2
        kp1 = xc/xb
        kInsideSqurt = (xbsquared-xasquared)/(xcsquared-xasquared)
        kp2 = math.sqrt(kInsideSqurt)
        k = kp1*kp2
        ksquared = k**2
        kder = math.sqrt(1-ksquared)
        kdersquared = kder**2
        K = ellipk(ksquared)
        Kder = ellipk(kdersquared)
        C0 = (4*relativePermittivityOfFreeSpace*Kder)/K
        return C0

    # Function to find line capacitances when dielctric layer present
    def findCap(height, eff):
        coeffInSideBracketsa = (math.pi*xa)/(2*height)
        coeffInSideBracketsb = (math.pi*xb)/(2*height)
        coeffInSideBracketsc = (math.pi*xc)/(2*height)

        coeffa = math.sinh(coeffInSideBracketsa)
        coeffasquared = coeffa**2
        coeffb = math.sinh(coeffInSideBracketsb)
        coeffbsquared = coeffb**2
        coeffc = customSinh(coeffInSideBracketsc)
        coeffcsquared = coeffc**2

        kp1 = 1.0/coeffb
        kInsideSqurt = (coeffbsquared-coeffasquared)/(1-coeffasquared*coeffcsquared)
        kp2 = math.sqrt(kInsideSqurt)
        k = kp1*kp2
        ksquared = k**2
        kder = math.sqrt(1-ksquared)
        kdersquared = kder**2

        K = ellipk(ksquared)
        Kder = ellipk(kdersquared)

        Kcoeff = Kder/K

        C = 2*relativePermittivityOfFreeSpace*eff*Kcoeff
        return C

    # Finding C0
    C0 = findC0(xa, xb, xc)

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

    # Find capacitances due to dielectric layers above conductor
    CapacitancesAbove = []
    k = 0
    while k < heights_above_length:
        if k == heights_above_length - 1:
            eff = effsLA[k] - 1
            height = heightsLA[k]
            C = findCap(height, eff)
            CapacitancesAbove.append(C)
        else:
            eff = effsLA[k] - effsLA[k+1]
            height = heightsLA[k]
            C = findCap(height, eff)
            CapacitancesAbove.append(C)
        k = k + 1

    OverallCapValueAbove = sum(CapacitancesAbove)

    # Find capacitances due to dielectric layers below conductor
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

    # Calculations due to the ground layered at the bottom of CPW structure
    heightsDiveffs = []
    x = 0
    while x < heights_below_length:
        height = heights_below[x]
        eff = effsLB[x]
        heightDiveff = height/eff
        heightsDiveffs.append(heightDiveff)
        x = x + 1
    sumofheightsDiveffs = sum(heightsDiveffs)
    CapacitancesDueToGround = (relativePermittivityOfFreeSpace*W)/(sumofheightsDiveffs)

    # Find relativer permittive and charateristic impedance of transmission line from
    # capacitances values already obtained
    OverallCapValueBelow = sum(CapacitancesBelow)
    OverallLineCap = OverallCapValueBelow + OverallCapValueAbove + C0 + CapacitancesDueToGround
    effRelativePermittivityForWholeStructure = OverallLineCap/C0
    effSquareRoot = math.sqrt(effRelativePermittivityForWholeStructure)
    PhaseVelocity = SpeedOfLight/effSquareRoot
    charateristicImpedance = 1/(OverallLineCap*PhaseVelocity)
    effRelativePermittivityForWholeStructure = format(effRelativePermittivityForWholeStructure, '.2f')
    charateristicImpedance = format(charateristicImpedance, '.2f')

    return [effRelativePermittivityForWholeStructure, charateristicImpedance]
