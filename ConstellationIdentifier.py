from Tkinter import *
import tkFileDialog
from tkFileDialog import askopenfilename
import math
import PIL
from PIL import Image, ImageTk
from PIL import ImageEnhance
from operator import itemgetter, attrgetter, methodcaller
import cv2
import numpy as np

#Mark all neighbors
def markNeighbors (pixels, sizeX, sizeY, pixelMatrix, x, y, posID, starList):
    #Mark all neighbors
    pixelMatrix = markPosition2(pixels, sizeX, sizeY, pixelMatrix, x, y, posID)
    
    #Set center
    starList.append(findCenter(pixelMatrix, x, y, sizeX, sizeY, posID))
    
    return (pixelMatrix, starList)

#Mark from specified position
def markPosition (pixels, sizeX, sizeY, pixelMatrix, x, y, posID):
    w = x

    print "Mark: {}, {}".format(x, y)
    
    for x in range(x, sizeX): #Go Left -> Right
        print "I: {}, {}".format(x, y)
        if(pixels[x, y] == (0, 0, 0) or (pixelMatrix[x][y] != 0 and pixelMatrix[x][y] != posID)):
            break
        else:
            pixelMatrix[x][y] = posID #Mark actual pivot

            j = y + 1
            for j in range(j, sizeY): #Go up
                if(pixels[x, j] == (0, 0, 0) or (pixelMatrix[x][j] != 0 and pixelMatrix[x][j] != posID)):
                    break
                else:
                    #Go sides
                    k = x
                    while k >= 0: #Left
                        if(pixels[k, j] == (0, 0, 0) or (pixelMatrix[k][j] != 0  and pixelMatrix[k][j] != posID)):
                            break
                        print "A: {}, {}".format(k, j)
                        pixelMatrix[k][j] = posID
                        k = k - 1

                    #p = x + 1
                    #while p < sizeX: #Right
                    #    if(pixels[p, j] == (0, 0, 0) or (pixelMatrix[p][j] != 0 and pixelMatrix[p][j] != posID)):
                    #        break
                    #    print "B: {}, {}".format(p, j)
                    #    pixelMatrix[p][j] = posID
                    #    p = p + 1

    return pixelMatrix

#Mark from specified position
def markPosition2 (pixels, sizeX, sizeY, pixelMatrix, x, y, posID):
    w = x

    #print "Mark: {}, {}".format(x, y)
    
    for y in range(y, sizeY): #Go Left -> Right
        #print "I: {}, {}".format(x, y)
        if(pixels[x, y] == (0, 0, 0) or (pixelMatrix[x][y] != 0 and pixelMatrix[x][y] != posID)):
            break
        else:
            pixelMatrix[x][y] = posID #Mark actual pivot

            i = x + 1
            for i in range(i, sizeX): #Go up
                if(pixels[i, y] == (0, 0, 0) or (pixelMatrix[i][y] != 0 and pixelMatrix[i][y] != posID)):
                    break
                else:
                    #Go sides
                    k = y
                    while k >= 0: #Left
                        if(pixels[i, k] == (0, 0, 0) or (pixelMatrix[i][k] != 0  and pixelMatrix[i][k] != posID)):
                            break
                        #print "A: {}, {}".format(i, k)
                        pixelMatrix[i][k] = posID
                        k = k - 1

                    p = y + 1
                    while p < sizeY: #Right
                        if(pixels[i, p] == (0, 0, 0) or (pixelMatrix[i][p] != 0 and pixelMatrix[i][p] != posID)):
                            break
                        #print "B: {}, {}".format(i, p)
                        pixelMatrix[i][p] = posID
                        p = p + 1

    return pixelMatrix

#Search and return start center data
def findCenter (pixelMatrix, x, y, sizeX, sizeY, posID):
    pHeight = 0
    pWidth = 0
    
    j = y
    for j in range(y, sizeY): #Go Down, Get Height
        if(pixelMatrix[x][j] == posID):
            pHeight = pHeight + 1
        else:
            break

    #Set new Y Coordinate
    y = pHeight / 2 + y
    
    i = x
    while i > 0: #Go Left, Get Pivot
        if(pixelMatrix[i][y] != posID):
            break
        i = i - 1

    for i in range(i + 1, sizeX): #Go Right, Get Width
        if(pixelMatrix[i][y] == posID):
            pWidth = pWidth + 1
        else:
            break

    #Set new X Coordinate
    x = pWidth / 2 + x

    return (x, y, pWidth, pHeight, pWidth * pHeight, posID)

#Search and return start center data
def findCenter2 (pixelMatrix, x, y, sizeX, sizeY, posID):
    pHeight = 0
    pWidth = 0
    
    for j in range(y, sizeY): #Go Down, Get Height
        if(pixelMatrix[x][j] == posID):
            pHeight = pHeight + 1
        else:
            break

    #Set new Y Coordinate
    y = pHeight / 2 + y
    
    i = x
    while i > 0: #Go Left, Get Pivot
        if(pixelMatrix[i][y] != posID):
            break
        i = i - 1

    for i in range(i + 1, sizeX): #Go Right, Get Width
        if(pixelMatrix[i][y] == posID):
            pWidth = pWidth + 1
        else:
            break

    #Set new X Coordinate
    x = pWidth / 2 + x

    return (x, y, pWidth, pHeight, pWidth * pHeight, posID)

#Detect Constellation from patternArray
def detectPattern(patternArray, starList, offset):
    result = list()
    preResult = list()
    pID = 0
    stLen = len(starList)
    if(stLen > 40):
        stLen = 40
    
    patternUsed = list()
    for i in range(len(patternArray)):
        patternUsed.append(0)
    
    for i in range(stLen): #Pivot Star
        for j in range(stLen): #Most near star
            if(j == i):
                continue
            
            distPivot = math.sqrt((starList[i][0] - starList[j][0]) * (starList[i][0] - starList[j][0]) + (starList[i][1] - starList[j][1]) * (starList[i][1] - starList[j][1]))
            #print "distPivot: {} ID0: {} ID1: {}".format(distPivot, i, j)
            preResult.append(i)
            preResult.append(j)

            for k in range(stLen): #Compare all other stars
                if(k == i or k == j):
                    continue
                dist3 = math.sqrt((starList[i][0] - starList[k][0]) * (starList[i][0] - starList[k][0]) + (starList[i][1] - starList[k][1]) * (starList[i][1] - starList[k][1]))
                #print "distance3: {} ID0: {} ID2: {}".format(dist3, i, k)
                for p in range(1, len(patternArray)): #Compare distances
                    if(distPivot * patternArray[p] - offset < dist3 and distPivot * patternArray[p] + offset > dist3 and patternUsed[p] != 1):
                        preResult.append(k) #Found
                        patternUsed[p] = 1
                        break

                if(len(preResult) == len(patternArray) + 1): #All stars found
                    result.append(preResult)
                    break

            preResult = list()    
            for p in range(len(patternArray)):
                patternUsed[p] = 0

    return result

def identifyConstellation(starList, starID0, starID1, starID2, distance0, distance1, distance2, offset):
    constellationFound = False;
    starFound = False
    remainingStars = len(distance0) - 3
    currentStar = 3

    similarity = 0

    maxLen = len(starList)
    if(maxLen > 60):
        maxLen = 60
    
    result = list()
    result.append(starID0)
    result.append(starID1)
    result.append(starID2)

    #Calculate pivot distances
    pivotDist0 = math.sqrt((starList[starID0][0] - starList[starID1][0]) * (starList[starID0][0] - starList[starID1][0]) + (starList[starID0][1] - starList[starID1][1]) * (starList[starID0][1] - starList[starID1][1]))
    pivotDist1 = math.sqrt((starList[starID1][0] - starList[starID2][0]) * (starList[starID1][0] - starList[starID2][0]) + (starList[starID1][1] - starList[starID2][1]) * (starList[starID1][1] - starList[starID2][1]))
    pivotDist2 = math.sqrt((starList[starID2][0] - starList[starID0][0]) * (starList[starID2][0] - starList[starID0][0]) + (starList[starID2][1] - starList[starID0][1]) * (starList[starID2][1] - starList[starID0][1]))

    while(remainingStars > 0):
        #Search 4th star and onwards
        starFound = False
        for i in range(maxLen):
            if(i == starID0 or i == starID1 or i == starID2):
                continue

            #Calculate all distances
            dist0 = math.sqrt((starList[i][0] - starList[starID0][0]) * (starList[i][0] - starList[starID0][0]) + (starList[i][1] - starList[starID0][1]) * (starList[i][1] - starList[starID0][1]))
            dist1 = math.sqrt((starList[i][0] - starList[starID1][0]) * (starList[i][0] - starList[starID1][0]) + (starList[i][1] - starList[starID1][1]) * (starList[i][1] - starList[starID1][1]))
            dist2 = math.sqrt((starList[i][0] - starList[starID2][0]) * (starList[i][0] - starList[starID2][0]) + (starList[i][1] - starList[starID2][1]) * (starList[i][1] - starList[starID2][1]))

            #Compare all distances
            if(pivotDist0 * distance0[currentStar] - offset <= dist0 and pivotDist0 * distance0[currentStar] + offset >= dist0):
                if(pivotDist1 * distance1[currentStar] - offset <= dist1 and pivotDist1 * distance1[currentStar] + offset >= dist1):
                    if(pivotDist2 * distance2[currentStar] - offset <= dist2 and pivotDist2 * distance2[currentStar] + offset >= dist2):
                        currentStar += 1
                        remainingStars -= 1

                        starFound = True
                        result.append(i)
                        
                        break


        #If !starFound -> constellation not found
        if(starFound == False):
            #print "Constellation Not Found"
            #print float(currentStar) / float(len(distance0))
            return (result, False, float(currentStar) / float(len(distance0)))

    #No more remaining stars -> constellation found
    print "Constellation Found"
    return (result, True, 1.0)

def identifyTemplate(name, starList, offset, arrayPattern0, arrayPattern1, arrayPattern2):
    global constellationName
    
    result = list()
    bestResult = list()
    similarity = 0
    bestSimilarity = 0
    constellationFound = False

    constellationName = name

    maxLen = len(starList)
    if(maxLen > 60):
        maxLen = 60

    for i in range(maxLen):
        for j in range(maxLen):
            if(j == i):
                continue
            for k in range(maxLen):
                if(k == i or k == j):
                    continue
                (result, constellationFound, similarity) = identifyConstellation(starList, i, j, k, arrayPattern0, arrayPattern1, arrayPattern2, offset)
                if(constellationFound == True):
                    bestResult = result
                    bestSimilarity = similarity
                    break
                if(similarity > bestSimilarity):
                    bestResult = result
                    bestSimilarity = similarity


            if(constellationFound == True):
                break

        if(constellationFound == True):
            break
    
    print "{} - Sim: {} \nResult: {}".format(name, bestSimilarity, bestResult)
    return (bestSimilarity, bestResult)

def identifyAquarius(starList, offset):
    global arrayLines
    print "Aquarius"
    
    #Aquarius Distances
    arrayPattern0 = [0.0, 1.0, 1.5361, 1.6831, 3.0655, 2.8351, 2.2763, 2.5493, 2.0161, 1.1546, 1.3180, 1.1906, 1.1461, 2.6463, 1.5115] #0 -> 1
    arrayPattern1 = [1.7093, 0.0, 1.0, 1.2758, 4.6587, 4.4291, 3.3481, 3.0867, 2.3471, 3.6707, 0.7093, 2.2990, 1.3634, 3.4123, 0.8905] #1 -> 2
    arrayPattern2 = [1.0, 0.3808, 0.0, 0.1058, 1.5579, 1.5123, 1.1039, 0.8350, 0.6214, 1.7514, 0.1475, 0.9642, 0.5412, 0.9884, 0.1093] #2 -> 0

    #Lines
    arrayLines = [(0, 1), (2, 3), (4, 5), (5, 6), (6, 8), (7, 8), (0, 9), (2, 10), (0, 11), (9, 11), (10, 12), (11, 12), (2, 14), (7, 13), (4, 13), (3, 8)]

    (similarity, result) = identifyTemplate("Aquarius", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyAries(starList, offset):
    global arrayLines
    print "Aries"

    #Aries
    arrayPattern0 = [0.0, 1.0, 0.7461, 1.9784, 2.3230, 2.9363] #0 -> 1
    arrayPattern1 = [3.4136, 0.0, 1.0, 9.8883, 10.0975, 11.9623] #1 -> 2
    arrayPattern2 = [1.0, 0.3927, 0.0, 3.6114, 3.8351, 4.6025] #2 -> 0

    arrayLines = [(0, 2), (1, 2), (0, 4), (3, 4), (4, 5)]

    (similarity, result) = identifyTemplate("Aries", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyCancer(starList, offset):
    global arrayLines
    print "Cancer"

    #Cancer
    arrayPattern0 = [0.0, 1.0, 1.0513, 1.2909, 1.9391] #0 -> 1
    arrayPattern1 = [1.5076, 0.0, 1.0, 1.4373, 2.4050] #1 -> 2
    arrayPattern2 = [1.0, 0.6310, 0.0, 0.2923, 0.9406] #2 -> 0

    arrayLines = [(1, 2), (0, 2), (2, 3), (3, 4)]

    (similarity, result) = identifyTemplate("Cancer", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyCapricornus(starList, offset):
    global arrayLines
    print "Capricornus"

    #Capricornus
    arrayPattern0 = [0.0, 1.0, 1.0844, 0.6417, 0.6958, 1.1083, 0.8138, 0.1393, 1.2046, 0.2053] #0 -> 1
    arrayPattern1 = [4.5434, 0.0, 1.0, 1.8575, 2.5536, 1.7173, 2.3935, 5.0341, 2.0746, 3.7580] #1 -> 2
    arrayPattern2 = [1.0, 0.2030, 0.0, 0.4101, 0.7002, 0.1533, 0.6810, 1.0825, 0.2182, 0.8649] #2 -> 0

    arrayLines = [(1, 2), (0, 3), (3, 5), (1, 6), (0, 7), (4, 6), (2, 8), (5, 8), (4, 9), (0, 9)]

    (similarity, result) = identifyTemplate("Capricornus", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyGemini(starList, offset):
    global arrayLines
    print "Gemini"

    #Gemini
    arrayPattern0 = [0.0, 1.0, 0.2269, 0.2246, 0.2653, 0.6560, 0.9981, 0.7827, 0.4564, 0.6489, 0.3880, 0.2483, 1.0958, 0.9320, 0.9186, 0.5153] #0 -> 1
    arrayPattern1 = [1.0364, 0.0, 1.0, 0.8163, 0.8123, 0.3849, 0.4175, 0.4972, 0.9171, 0.4544, 0.9005, 0.8785, 0.2039, 0.2233, 0.3596, 0.5886] #1 -> 2
    arrayPattern2 = [1.0, 4.2528, 0.0, 0.9621, 1.7276, 2.6247, 4.6430, 2.8571, 2.8249, 3.0849, 0.7906, 0.5202, 4.5026, 4.1724, 4.2522, 1.8133] #2 -> 0

    #Lines
    arrayLines = [(0, 4), (1, 5), (2, 11), (3, 4), (3, 11), (4, 8), (4, 9), (10, 11), (7, 12), (9, 13), (5, 15), (7, 15), (11, 15), (6, 14), (9, 14)]

    (similarity, result) = identifyTemplate("Gemini", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyLeo(starList, offset):
    global arrayLines
    print "Leo"

    #Leo
    arrayPattern0 = [0.0, 1.0, 0.3384, 0.7312, 0.5259, 0.6640, 0.4719, 0.5877, 0.1948] #0 -> 1
    arrayPattern1 = [1.1188, 0.0, 1.0, 0.4666, 1.4006, 0.3863, 1.0809, 1.3582, 1.1195] #1 -> 2
    arrayPattern2 = [1.0, 2.6415, 0.0, 1.5472, 1.0833, 1.6406, 0.4447, 1.0673, 0.5164] #2 -> 0

    arrayLines = [(1, 3), (1, 5), (0, 5), (2, 6), (4, 7), (6, 7), (2, 8), (0, 8), (2, 3)]

    (similarity, result) = identifyTemplate("Leo", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyLibra(starList, offset):
    global arrayLines
    print "Libra"

    #Libra
    arrayPattern0 = [0.0, 1.0, 1.6632, 0.9341, 0.8309, 1.3195] #0 -> 1
    arrayPattern1 = [1.0547, 0.0, 1.0, 1.9169, 1.7569, 1.1730] #1 -> 2
    arrayPattern2 = [1.0, 0.5701, 0.0, 1.3002, 1.1949, 0.4346] #2 -> 0

    arrayLines = [(1, 2), (0, 1), (3, 4), (4, 5), (2, 5)]

    (similarity, result) = identifyTemplate("Libra", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyPisces(starList, offset):
    global arrayLines
    print "Pisces"

    #Pisces
    arrayPattern0 = [0.0, 1.0, 0.3497, 0.9329, 0.2091, 0.6338, 0.4554, 0.8521, 0.8591, 0.1408, 0.7459, 0.9453, 0.1827, 0.5922, 0.7134, 0.3754, 0.3123] #0 -> 1
    arrayPattern1 = [1.1846, 0.0, 1.0, 0.1160, 0.9521, 1.0741, 0.6632, 0.1849, 0.1772, 1.0318, 0.3170, 0.0917, 1.0647, 1.0012, 1.0840, 0.7642, 0.8384] #1 -> 2
    arrayPattern2 = [1.0, 2.4141, 0.0, 2.1636, 0.6264, 0.8375, 0.8913, 2.0741, 1.9863, 0.6933, 1.6513, 2.3222, 0.4785, 0.6976, 1.0580, 0.6953, 0.6077] #2 -> 0

    arrayLines = [(1, 3), (3, 8), (7, 8), (0, 9), (4, 9), (8, 10), (6, 10), (7, 11), (1, 11), (9, 12), (2, 12), (2, 13), (5, 13), (13, 14), (5, 14), (4, 16), (6, 15), (15, 16)]

    (similarity, result) = identifyTemplate("Pisces", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifySaggittarus(starList, offset):
    global arrayLines
    print "Saggittarus"

    #Saggittarus
    arrayPattern0 = [0.0, 1.0, 0.5930, 0.7932, 1.2551, 1.1090, 0.3752, 0.2821, 0.2171] #0 -> 1
    arrayPattern1 = [1.1665, 0.0, 1.0, 0.5132, 0.3031, 0.6174, 1.0320, 1.2595, 0.9663] #1 -> 2
    arrayPattern2 = [1.0, 1.4456, 0.0, 0.7469, 1.8547, 1.1246, 1.4269, 1.4508, 0.6856] #2 -> 0

    arrayLines = [(1, 3), (2, 3), (1, 4), (1, 5), (3, 5), (1, 6), (0, 7), (6, 7), (2, 8), (0, 8), (6, 8), (3, 8)]

    (similarity, result) = identifyTemplate("Saggittarus", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyScorpius(starList, offset):
    global arrayLines
    print "Scorpius"

    #Scorpius
    arrayPattern0 = [0.0, 1.0, 1.2644, 0.9556, 0.5294, 1.1609, 0.5073, 0.1307, 0.4030, 1.1755, 0.7344, 0.4490, 0.4522, 1.1087, 1.2470, 0.1179, 0.4717] #0 -> 1
    arrayPattern1 = [2.9214, 0.0, 1.0, 1.5096, 1.5449, 0.4731, 4.3981, 2.5443, 3.8805, 0.6106, 1.3784, 4.2040, 3.6678, 1.2250, 0.7293, 3.2498, 4.2611] #1 -> 2
    arrayPattern2 = [1.0, 0.2707, 0.0, 0.3819, 0.5883, 0.1881, 1.4000, 0.8967, 1.2195, 0.2951, 0.4652, 1.3291, 1.1362, 0.2188, 0.1606, 1.0820, 1.3719] #2 -> 0

    arrayLines = [(1, 5), (0, 7), (4, 7), (1, 9), (4, 10), (3, 10), (6, 11), (8, 11), (8, 12), (2, 13), (3, 13), (5, 14), (2, 14), (0, 15), (6, 16), (11, 15)]

    (similarity, result) = identifyTemplate("Scorpius", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyTaurus(starList, offset):
    global arrayLines
    print "Taurus"

    #Taurus
    arrayPattern0 = [0.0, 1.0, 1.5310, 1.2026, 0.9693, 1.0955, 2.0145, 0.4713, 1.7884, 1.0918, 2.0674] #0 -> 1
    arrayPattern1 = [1.7815, 0.0, 1.0, 0.4245, 0.3372, 0.1942, 1.9162, 1.6259, 1.4065, 0.3414, 2.0034] #1 -> 2
    arrayPattern2 = [1.0, 0.3666, 0.0, 0.2164, 0.3685, 0.2960, 0.3381, 0.9621, 0.2549, 0.2871, 0.3690] #2 -> 0

    arrayLines = [(2, 3), (0, 4), (1, 5), (3, 5), (2, 6), (1, 7), (2, 8), (3, 9), (4, 9), (6, 10)]

    (similarity, result) = identifyTemplate("Taurus", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

def identifyVirgo(starList, offset):
    global arrayLines
    print "Virgo"

    #Virgo
    arrayPattern0 = [0.0, 1.0, 0.9211, 0.4104, 0.9000, 2.0999, 0.3721, 2.1508, 1.3886, 1.6491, 0.9338, 0.5621, 0.9141, 1.1010] #0 -> 1
    arrayPattern1 = [0.6399, 0.0, 1.0, 0.7149, 1.1803, 0.8826, 0.8483, 1.0525, 0.6830, 0.5994, 1.2355, 0.2963, 0.4750, 1.3371] #1 -> 2
    arrayPattern2 = [1.0, 1.6967, 0.0, 0.5754, 1.5033, 2.2475, 1.1709, 2.0564, 1.3099, 1.8656, 1.0791, 1.2357, 1.0477, 1.4647] #2 -> 0

    arrayLines = [(0, 3), (2, 3), (0, 6), (4, 6), (7, 8), (5, 9), (6, 10), (0, 11), (1, 11), (8, 12), (9, 12), (0, 12), (4, 13), (10, 13)]

    (similarity, result) = identifyTemplate("Virgo", starList, offset, arrayPattern0, arrayPattern1, arrayPattern2)
    return (similarity, result)

#def saveStarPattern(name, starList):
#    f = open('ConstellationPatterns.txt', 'r+')
#
#    f.write(name)
#
#    f.close()

def preProcessImage():
    global newImage
    global processedImg

    #Grayscale RGB
    processedImg = newImage.convert('L').convert('RGB')

    #Do opencv operations
    numpImg = np.asarray(processedImg)

    ##Filter Image
    #blur = cv2.blur(numpImg,(5,5)) #Blur
    #dst = cv2.fastNlMeansDenoisingColored(blur,None,10,10,7,21) #Noise Reduction
    #print "Blur + Noise Reduction Complete"

    #Binary image
    thresh = 141
    numpImg = cv2.threshold(numpImg, thresh, 255, cv2.THRESH_BINARY)[1]

    ##Erosion
    #kernel = np.ones((2,2),np.uint8)
    #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    #numpImg = cv2.erode(numpImg, kernel, iterations = 1)

    #Dilate
    #numpImg = cv2.dilate(numpImg, kernel, iterations = 1)

    #End opencv operations
    processedImg = Image.fromarray(np.uint8(numpImg))

    return

def getStarList():
    global processedImg
    global starList
    global pixels

    pixels = processedImg.load()

    imWidth, imHeight = processedImg.size
    boolPixel = [[0 for x in range(imHeight)] for y in range(imWidth)]
    
    i = 0
    j = 0
    posID = 1
    starList = list()
    for i in range(processedImg.size[0]):
        for j in range(processedImg.size[1]):
            if (pixels[i, j] > (0, 0, 0) and boolPixel[i][j] == 0):
                (boolPixel, starList) = markNeighbors (pixels, processedImg.size[0], processedImg.size[1], boolPixel, i, j, posID, starList)
                posID = posID + 1

    starList = sorted(starList, key=itemgetter(4), reverse=True)
    
    print "Star List Size: {}".format(len(starList))
    
    return

def markShowResult():
    global pixels
    global canv
    global imgOnCanvas
    global imageCons
    global newImage
    global result
    global starList
    global arrayLines
    global similarity

    if(similarity < 0.7):
        print "Constellation Not Found - Best Guess: {} Sim: {}".format(constellationName, similarity)
        return

    #Do opencv operations
    numpImg = np.asarray(newImage)
    
    #Draw Circles
    for i in range(len(result)):
        cv2.circle(numpImg, (starList[result[i]][0], starList[result[i]][1]), starList[result[i]][2], (255, 0, 0, 0), thickness=1, lineType=8, shift=0)

    #Draw Lines
    for i in range(len(arrayLines)):
        if(arrayLines[i][0] < len(result) and arrayLines[i][1] < len(result)):
            cv2.line(numpImg, (starList[result[arrayLines[i][0]]][0], starList[result[arrayLines[i][0]]][1]), (starList[result[arrayLines[i][1]]][0], starList[result[arrayLines[i][1]]][1]), (255, 0, 0, 0), thickness=1, lineType=8, shift=0)

    #End opencv operations
    newImage = Image.fromarray(np.uint8(numpImg))
    
    #for i in range(len(result)):
    #    pixels[starList[result[i]][0], starList[result[i]][1]] = (255, 0, 0)

    ##Mark biggest stars
    #pixels[starList[0][0], starList[0][1]] = (0, 0, 255) #1st
    #pixels[starList[1][0], starList[1][1]] = (0, 255, 0) #2nd
    #pixels[starList[2][0], starList[2][1]] = (0, 0, 0) #3rd
    ##pixels[starList[3][0], starList[3][1]] = (0, 0, 0) #4th

    imageCons = ImageTk.PhotoImage(newImage)

    imWidth, imHeight = newImage.size
    print "Size W:{} H:{}".format(imWidth, imHeight)

    #canv = Canvas(width=1002, height=600)
    #canv.pack(side='top', fill='both', expand='yes')
    imgOnCanvas = 0
    canv.create_image(0, 0, image=imageCons, anchor='nw')

    return

def onClickLoadImage():
    global canv
    global imgOnCanvas
    global imageCons
    global newImage
    
    imageFilename = askopenfilename()
    if(imageFilename == ""):
        return

    print imageFilename
    #Clean Canvas
    canv.delete(imgOnCanvas)

    #Load and setup
    newImage = Image.open(imageFilename);
    imWidth, imHeight = newImage.size
    aspectRatio = float(imWidth) / float(imHeight)
    print "ApR: {}".format(aspectRatio)

    #image1 = image1.convert('L').convert('RGB')

    if(imWidth > 800):
        newImage = newImage.resize((800, int(float(800) / aspectRatio)), Image.ANTIALIAS)
        imWidth = 800
        imHeight = 800 / aspectRatio

    #Convert to photo
    imageCons = ImageTk.PhotoImage(newImage)
        
    imgOnCanvas = canv.create_image(0, 0, image=imageCons, anchor='nw')

def onClickSaveImage():
    global constellationName
    global newImage

    newImage.save(constellationName + '.jpg')

    print "Image saved as: {}".format(constellationName + '.jpg')

    return

def onClickIdentifyAny():
    global result
    global similarity
    global constellationName

    preProcessImage()
    getStarList()

    bestResult = list()
    bestSimilarity = 0.0
    bestName = ""
    (similarity, result) = identifyAquarius(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return
    
    (similarity, result) = identifyAries(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return

    (similarity, result) = identifyCancer(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return
    
    (similarity, result) = identifyCapricornus(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return

    (similarity, result) = identifyGemini(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return
    
    (similarity, result) = identifyLeo(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return

    (similarity, result) = identifyLibra(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return
    
    (similarity, result) = identifyPisces(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return

    (similarity, result) = identifySaggittarus(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return

    (similarity, result) = identifyScorpius(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return
    
    (similarity, result) = identifyTaurus(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return

    (similarity, result) = identifyVirgo(starList, 8)
    if(similarity > bestSimilarity):
        bestResult = result
        bestSimilarity = similarity
        bestName = constellationName

    if(similarity == 1.0):
        markShowResult()
        return

    result = bestResult
    similarity = bestSimilarity
    constellationName = bestName

    markShowResult()

    return

def onClickIdentifyAquarius():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyAquarius(starList, 8)

    markShowResult()

    return

def onClickIdentifyAries():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyAries(starList, 8)

    markShowResult()
    return

def onClickIdentifyCancer():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyCancer(starList, 8)

    markShowResult()

    return

def onClickIdentifyCapricornus():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyCapricornus(starList, 8)

    markShowResult()

    return

def onClickIdentifyGemini():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyGemini(starList, 8)

    markShowResult()

    return

def onClickIdentifyLeo():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyLeo(starList, 8)

    markShowResult()
    
    return

def onClickIdentifyLibra():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyLibra(starList, 8)

    markShowResult()
    
    return

def onClickIdentifyPisces():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyPisces(starList, 8)

    markShowResult()
    
    return

def onClickIdentifySaggittarus():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifySaggittarus(starList, 8)

    markShowResult()

    return

def onClickIdentifyScorpius():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyScorpius(starList, 8)

    markShowResult()

    return

def onClickIdentifyTaurus():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyTaurus(starList, 8)

    markShowResult()

    return

def onClickIdentifyVirgo():
    global result
    global similarity

    preProcessImage()
    getStarList()

    (similarity, result) = identifyVirgo(starList, 8)

    markShowResult()

    return

def onClickShowBinary():
    global canv
    global imgOnCanvas
    global imageCons
    global processedImg

    preProcessImage()

    #Clean Canvas
    canv.delete(imgOnCanvas)
    
    #Convert to photo
    imageCons = ImageTk.PhotoImage(processedImg)
        
    imgOnCanvas = canv.create_image(0, 0, image=imageCons, anchor='nw')

def onClickRemoveNoise():
    global canv
    global imgOnCanvas
    global imageCons
    global newImage
    
    #Do opencv operations
    numpImg = np.asarray(newImage)

    numpImg = cv2.fastNlMeansDenoisingColored(numpImg,None,10,10,7,21)
    
    #End opencv operations
    newImage = Image.fromarray(np.uint8(numpImg))
    imWidth, imHeight = newImage.size
    aspectRatio = imWidth / imHeight

    #Clean Canvas
    canv.delete(imgOnCanvas)

    #image1 = image1.convert('L').convert('RGB')

    if(imWidth > 800):
        newImage = newImage.resize((800, int(float(imHeight) * aspectRatio)), Image.ANTIALIAS)
        imWidth = 800
        imHeight = imHeight * aspectRatio

    #Convert to photo
    imageCons = ImageTk.PhotoImage(newImage)
        
    imgOnCanvas = canv.create_image(0, 0, image=imageCons, anchor='nw')

def onClickIncreaseConstrast():
    global canv
    global imgOnCanvas
    global imageCons
    global newImage

    #Do opencv operations
    numpImg = np.asarray(newImage)

    imghsv = cv2.cvtColor(numpImg, cv2.COLOR_BGR2HSV)
    imghsv[:,:,2] = [[max(pixel - 25, 0) if pixel < 190 else min(pixel + 25, 255) for pixel in row] for row in imghsv[:,:,2]]
    imghsv = cv2.cvtColor(imghsv, cv2.COLOR_HSV2BGR)
    
    #End opencv operations
    newImage = Image.fromarray(np.uint8(imghsv))
    imWidth, imHeight = newImage.size
    aspectRatio = imWidth / imHeight

    #Clean Canvas
    canv.delete(imgOnCanvas)

    #image1 = image1.convert('L').convert('RGB')

    if(imWidth > 800):
        newImage = newImage.resize((800, int(float(imHeight) * aspectRatio)), Image.ANTIALIAS)
        imWidth = 800
        imHeight = imHeight * aspectRatio

    #Convert to photo
    imageCons = ImageTk.PhotoImage(newImage)
        
    imgOnCanvas = canv.create_image(0, 0, image=imageCons, anchor='nw')

def onClickReduceConstrast():
    global canv
    global imgOnCanvas
    global imageCons
    global newImage

    #Do opencv operations
    numpImg = np.asarray(newImage)

    imghsv = cv2.cvtColor(numpImg, cv2.COLOR_BGR2HSV)
    imghsv[:,:,2] = [[max(pixel - 25, 0) if pixel > 190 else min(pixel + 25, 255) for pixel in row] for row in imghsv[:,:,2]]
    
    #End opencv operations
    newImage = Image.fromarray(np.uint8(imghsv))
    imWidth, imHeight = newImage.size
    aspectRatio = imWidth / imHeight

    #Clean Canvas
    canv.delete(imgOnCanvas)

    #image1 = image1.convert('L').convert('RGB')

    if(imWidth > 800):
        newImage = newImage.resize((800, int(float(imHeight) * aspectRatio)), Image.ANTIALIAS)
        imWidth = 800
        imHeight = imHeight * aspectRatio

    #Convert to photo
    imageCons = ImageTk.PhotoImage(newImage)
        
    imgOnCanvas = canv.create_image(0, 0, image=imageCons, anchor='nw')

#####Start Program#####
#sys.setrecursionlimit(10000)

root = Tk()

#image1 = Image.open("Orion-NoMarks.jpg").convert('L')
#image1 = Image.open("Libra-NoMarks.jpg")
#image1 = Image.open("Virgo-5.jpg")
#image1 = Image.open("Test.png")
#image1 = Image.open("Database/Test-4.png")
newImage = Image.open("Database/VirgoPattern.png")
#newImage = Image.open("Leo-4.jpg")

imWidth, imHeight = newImage.size

#enhancer = ImageEnhance.Brightness(image1)
#image1 = enhancer.enhance(0.1)

#enhancer = ImageEnhance.Contrast(image1)
#image1 = enhancer.enhance(14)

preProcessImage()

starList = list()
pixels = newImage.load()
getStarList()

#starList = [item for item in starList if item[4] > 5]
print len(starList)
print starList[0]#, starList[1], starList[2]#, starList[3], starList[4]

##Print distances
#defaDist = 0
#ID0 = 2
#ID1 = 0
#defaDist = math.sqrt((starList[ID0][0] - starList[ID1][0]) * (starList[ID0][0] - starList[ID1][0]) + (starList[ID0][1] - starList[ID1][1]) * (starList[ID0][1] - starList[ID1][1]))
#print "Default: ID0: {} ID1: {}".format(ID0, ID1)
#for i in range(len(starList)):
#    for j in range(len(starList)):
#        if(i == j):
#            continue
#        #if(j == 0 or (i == 0 and j == 1)):
#        print "ID0: {} ID1: {} Dist: {}".format(i, j, math.sqrt((starList[i][0] - starList[j][0]) * (starList[i][0] - starList[j][0]) + (starList[i][1] - starList[j][1]) * (starList[i][1] - starList[j][1])) / defaDist)

#print starList[0], starList[1], starList[2], starList[3]

#for i in range(2):
#    pixels[starList[i][0], starList[i][1]] = (255, 0, 0)

#Mark Test
#for i in range(image2.size[0]):
#    for j in range(image2.size[1]):
#        if (pixels[i, j] > (0, 0, 0) and boolPixel[i][j] != 0):
#            print j
#            pixels[i, j] = (255, 0, 0)

#Show Image pixels
#for i in range(image2.size[0]):
#    for j in range(image2.size[1]):
#        print '%03d' % (pixels[i, j][0]),
#    print

#Show Aux pixels
#for i in range(image2.size[0]):
#    for j in range(image2.size[1]):
#        print boolPixel[i][j],
#    print

##Libra
#arrayPattern0 = [0.0, 1.0, 0.7668, 1.7561, 2.1069] #0 -> 1
#arrayPattern1 = [0.8503, 0.0, 1.0, 0.8996, 1.4961] #1 -> 2
#arrayPattern2 = [1.0, 1.5336, 0.0, 1.8151, 1.9012] #2 -> 0

result = list()
similarity = 0
#
#(similarity, result) = identifyVirgo(starList, 8)
#onClickIdentifyAquarius()

#print "This is a result: {}".format(result)

#First Detect
#arrayPattern = [1.0, 1.3, 1.3]
#arrayPattern = [1.0, 1.1736, 1.0579, 1.7536, 1.6394]
#result = detectPattern(arrayPattern, starList, 60)

#print "Result0 Len: {}".format(len(result))
#print "Result0:",
#for i in range(len(result)):
#    print result[i],
#print

#Second Detect
#arrayPattern = [1.0, 0.3, 0.43]
#arrayPattern = [1.0, 0.7668, 1.7561, 2.1069, 1.2625] #0 -> 1
#result2 = list()
#result2 = detectPattern(arrayPattern, starList, 60)

#print "Result2 Len: {}".format(len(result2))
#print "Result2:",
#for i in range(len(result2)):
#    print result2[i],
#print

#Third Detect
#arrayPattern = [1.0, 0.4, 0.4]
#arrayPattern = [1.0, 0.6494, 1.1822, 1.2364, 0.4453]
#result3 = list()
#result3 = detectPattern(arrayPattern, starList, 60)

#print "Result3 Len: {}".format(len(result3))
#print "Result3:",
#for i in range(len(result3)):
#    print result3[i],
#print

#finalResult = list()
#finalFound = False
#Merge all results
#for i in range(len(result)): #First Result
#    result[i] = sorted(result[i])
#    for j in range(len(result2)):
#        result2[j] = sorted(result2[j])
#        for k in range(len(result3)):
#            result3[k] = sorted(result3[k])
#            if(result[i] == result2[j] and result[i] == result3[k]):
#                finalResult += result[i]
#                finalFound = True
#                break
#
#        if(finalFound):
#            break
#
#    if(finalFound):
#        break

#Check final result
#print "Final Result: {}".format(finalResult)

#for i in range(len(finalResult)):
#    if(i == 0):
#        pixels[starList[finalResult[i]][0], starList[finalResult[i]][1]] = (0, 255, 0)
#    elif(i == 1):
#        pixels[starList[finalResult[i]][0], starList[finalResult[i]][1]] = (0, 0, 255)
#    else:
#        pixels[starList[finalResult[i]][0], starList[finalResult[i]][1]] = (255, 0, 0)


###for i in range(len(result)):
###    pixels[starList[result[i]][0], starList[result[i]][1]] = (255, 0, 0)

##Mark biggest stars
#pixels[starList[0][0], starList[0][1]] = (0, 0, 255) #1st
#pixels[starList[1][0], starList[1][1]] = (0, 255, 0) #2nd
#pixels[starList[2][0], starList[2][1]] = (0, 0, 0) #3rd
##pixels[starList[3][0], starList[3][1]] = (0, 0, 0) #4th

###imageCons = ImageTk.PhotoImage(newImage)

###print "Size W:{} H:{}".format(imWidth, imHeight)

#saveStarPattern('Cancer', starList)

canv = Canvas(width=1002, height=600)
canv.pack(side='top', fill='both', expand='yes')
imgOnCanvas = 0
#cv.create_image(0, 0, image=imageCons, anchor='nw')

constellationName = ""
arrayLines = list()
processedImg = newImage

####################Buttons###############################
buttonLoad = Button(root, text ="Cargar Imagen", command = onClickLoadImage)
buttonLoad.pack()
buttonLoad.place(x = 802, y = 0, width = 200, height = 30)

buttonLoad = Button(root, text ="Guardar Imagen", command = onClickSaveImage)
buttonLoad.pack()
buttonLoad.place(x = 802, y = 30, width = 200, height = 30)

#Label Constellation
labelConstellation = Label(root, text = "------------------------------------\nConstelacion", relief=FLAT)
labelConstellation.pack()
labelConstellation.place(x = 802, y = 60, width = 200, height = 40)

buttonIdentifyIC = Button(root, text ="Identificar\nCualquiera", command = onClickIdentifyAny)
buttonIdentifyIC.pack()
buttonIdentifyIC.place(x = 802, y = 100, width = 100, height = 40)

buttonIdentifyCAQU = Button(root, text ="Acuario", command = onClickIdentifyAquarius)
buttonIdentifyCAQU.pack()
buttonIdentifyCAQU.place(x = 802, y = 140, width = 100, height = 40)

buttonIdentifyCARI = Button(root, text ="Aries", command = onClickIdentifyAries)
buttonIdentifyCARI.pack()
buttonIdentifyCARI.place(x = 802, y = 180, width = 100, height = 40)

buttonIdentifyCCNC = Button(root, text ="Cancer", command = onClickIdentifyCancer)
buttonIdentifyCCNC.pack()
buttonIdentifyCCNC.place(x = 802, y = 220, width = 100, height = 40)

buttonIdentifyCCNC = Button(root, text ="Capricornus", command = onClickIdentifyCapricornus)
buttonIdentifyCCNC.pack()
buttonIdentifyCCNC.place(x = 802, y = 260, width = 100, height = 40)

buttonIdentifyCGEM = Button(root, text ="Gemini", command = onClickIdentifyGemini)
buttonIdentifyCGEM.pack()
buttonIdentifyCGEM.place(x = 802, y = 300, width = 100, height = 40)

buttonIdentifyCLEO = Button(root, text ="Leo", command = onClickIdentifyLeo)
buttonIdentifyCLEO.pack()
buttonIdentifyCLEO.place(x = 802, y = 340, width = 100, height = 40)

buttonIdentifyCMP = Button(root, text ="Mostrar\nPreproceso", command = onClickShowBinary)
buttonIdentifyCMP.pack()
buttonIdentifyCMP.place(x = 902, y = 100, width = 100, height = 40)

buttonIdentifyCLIB = Button(root, text ="Libra", command = onClickIdentifyLibra)
buttonIdentifyCLIB.pack()
buttonIdentifyCLIB.place(x = 902, y = 140, width = 100, height = 40)

buttonIdentifyCPSC = Button(root, text ="Pisces", command = onClickIdentifyPisces)
buttonIdentifyCPSC.pack()
buttonIdentifyCPSC.place(x = 902, y = 180, width = 100, height = 40)

buttonIdentifyCSGR = Button(root, text ="Saggittarus", command = onClickIdentifySaggittarus)
buttonIdentifyCSGR.pack()
buttonIdentifyCSGR.place(x = 902, y = 220, width = 100, height = 40)

buttonIdentifyCSCO = Button(root, text ="Scorpius", command = onClickIdentifyScorpius)
buttonIdentifyCSCO.pack()
buttonIdentifyCSCO.place(x = 902, y = 260, width = 100, height = 40)

buttonIdentifyCTAU = Button(root, text ="Taurus", command = onClickIdentifyTaurus)
buttonIdentifyCTAU.pack()
buttonIdentifyCTAU.place(x = 902, y = 300, width = 100, height = 40)

buttonIdentifyCVIR = Button(root, text ="Virgo", command = onClickIdentifyVirgo)
buttonIdentifyCVIR.pack()
buttonIdentifyCVIR.place(x = 902, y = 340, width = 100, height = 40)

buttonIdentifyCQR = Button(root, text ="Quitar\nRuido", command = onClickRemoveNoise)
buttonIdentifyCQR.pack()
buttonIdentifyCQR.place(x = 802, y = 440, width = 100, height = 40)

buttonIdentifyCSContrast = Button(root, text ="Subir\nContraste", command = onClickIncreaseConstrast)
buttonIdentifyCSContrast.pack()
buttonIdentifyCSContrast.place(x = 902, y = 440, width = 100, height = 40)

#buttonIdentifyCBContrast = Button(root, text ="Bajar\nContraste", command = onClickReduceConstrast)
#buttonIdentifyCBContrast.pack()
#buttonIdentifyCBContrast.place(x = 902, y = 480, width = 100, height = 40)
################End Buttons##################################

root.mainloop()
