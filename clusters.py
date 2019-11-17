import math
import random

import pandas as pd

alpha = 0.01
cycles = 2000


def getSquaredSum(matrix, matrixHeight, matrixLength):
    totalNet = 0
    for i in range(matrixHeight):
        sentenceNet = 0
        for j in range(matrixLength):
            sentenceNet = sentenceNet + matrix.iat[i, j]
        totalNet = totalNet + sentenceNet ** 2
    return math.sqrt(totalNet)


def normalizeToUnity(matrix, sSum, matrixHeight, matrixLength):
    for x in range(matrixHeight):
        for y in range(matrixLength):
            matrix.iloc[x, y] = matrix.iloc[x, y] / sSum
    return matrix


def normalizeSum(matrix, matrixHeight):
    localMax = float(matrix.max())
    localMin = float(matrix.min())
    normalMatrix = pd.DataFrame(columns=['Normal Sum'])
    normalList = []
    for i in range(matrixHeight):
        value = matrix.iat[i, 0]
        normValue = regNormalize(value, localMax, localMin)
        normalList.append(normValue)
        normalMatrix = normalMatrix.append({'Normal Sum': normalList[i]}, ignore_index=True)
    return normalMatrix


def regNormalize(val, mMax, mMin):
    return float((val - mMin) / (mMax - mMin))


def alterWeight(value, pattern):
    return value + alpha * pattern


def getNumInputs(tdm):
    return len(tdm.columns)


def getNumPatterns(tdm):
    return len(tdm.index)


def createWeightMatrix(matrix, matrixHeight, matrixLength):
    weightMatrix = matrix.copy()
    for i in range(matrixHeight):
        for j in range(matrixLength):
            weightMatrix.iloc[i, j] = random.uniform(0.0, 1.0)
    return weightMatrix


def singleRowNormalize(matrix, index, sSum):
    for cols in matrix.columns:
        matrix[cols].iloc[index] = matrix[cols].iloc[index] / sSum
    return matrix


def WTA(tdm):
    print('WTA')
    # Step 0 - Preprocessing
    matrixLength = getNumInputs(tdm)
    matrixHeight = getNumPatterns(tdm)

    # Step 1 - Normalizing the TDM
    tdmSum = getSquaredSum(tdm, matrixHeight, matrixLength)
    newTDM = normalizeToUnity(tdm, tdmSum, matrixHeight, matrixLength)
    nTDMSum = newTDM.sum().sum()

    # Step 2 - Creating a weight matrix and normalizing
    weightMatrix = createWeightMatrix(tdm, matrixHeight, matrixLength)
    weightSum = getSquaredSum(weightMatrix, matrixHeight, matrixLength)
    weights = normalizeToUnity(weightMatrix, weightSum, matrixHeight, matrixLength)

    # Step 6 - Iterate through all of the following steps a number of times equal to the
    # predefined cycles variable
    for cycle in range(cycles):
        # Step 3 - Creating a net matrix corresponding to each
        netMatrix = pd.DataFrame(columns={'Net'})
        net = 0.0
        netList = []
        largestNet = 0.0
        largestNetIndex = 0
        for i in range(matrixHeight):
            for j in range(matrixLength):
                # net = net + (newTDM.iloc[i, j] * weights.iloc[i, j])
                net = math.sqrt(2-2*(weights.iloc[i, j] * tdm.iloc[i, j]))
            # The values of net are not correctly being added to the netMatrix
            netList.append(net.__str__())
            netMatrix = netMatrix.append({'Net': netList[i]}, ignore_index=True)
            largestNet = netMatrix.max(axis=1).max()
            largestNetIndex = netMatrix.max(axis=1).idxmax()

        # Step 4 - Update the values of the weights whose row corresponds to the largest net
        for col in range(matrixLength):
            value = weights.iat[largestNetIndex, col]
            pattern = tdm.iat[largestNetIndex, col]
            weights.iloc[largestNetIndex, col] = alterWeight(value, pattern)

        # Step 5
        weightSum = getSquaredSum(weights, matrixHeight, matrixLength)
        weights = singleRowNormalize(weights, largestNetIndex, weightSum)
        print("Cycle: {0} Index: {1} Net {2}".format(cycle, largestNetIndex, largestNet))

    vectorSums, normalVectors = sumMatrix(weights, matrixHeight, matrixLength)
    return weights, vectorSums, normalVectors


def sumMatrix(matrix, matrixHeight, matrixLength):
    # Step 7
    # After that is all said and done, we must create a new dataframe that has the sum of each weight vector to return
    # a single column dataframe
    vectorSums = pd.DataFrame(columns=['Sum'])
    tempFrame = []
    for i in range(matrixHeight):
        wSum = 0
        for j in range(matrixLength):
            wSum = wSum + matrix.iat[i, j]
        tempFrame.append(wSum)
        vectorSums = vectorSums.append({'Sum': tempFrame[i]}, ignore_index=True)
    normalVectors = normalizeSum(vectorSums, matrixHeight)
    return vectorSums, normalVectors
