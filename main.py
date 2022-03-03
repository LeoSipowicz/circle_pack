import numpy as np
import random
from graphics import *
import math

isLocValidCalls = 0


def fillWithCircles(inputCircle, inputArray, completeArray):
    global circlesUsed
    inputRadius = inputCircle[0]
    inputXPos = inputCircle[1]
    inputYPos = inputCircle[2]

    x = 0
    while x < 360:
        if circlesUsed < circleArray.size:
            newRadius = inputArray[circlesUsed]
            distanceBetween = newRadius + inputRadius
            proposedXPos = (distanceBetween * math.cos(math.radians(x))) + inputXPos
            proposedYPos = (distanceBetween * math.sin(math.radians(x))) + inputYPos

            if circleLocationValid(windowSizeX, windowSizeY, proposedXPos, proposedYPos, newRadius, completeArray,
                                   circlesUsed):
                completeArray[circlesUsed] = [newRadius, proposedXPos, proposedYPos]
                circlesUsed = circlesUsed + 1

        x = x + 10


def circularPack(xDum, yDum, inputArray):
    global circlesUsed
    circlesUsed = 0
    completeArray = np.zeros([inputArray.size, 3])

    # First circle in middle
    radius = inputArray[0]
    xPos = windowSizeX / 2
    yPos = windowSizeX / 2
    completeArray[0] = [radius, xPos, yPos]
    for t in range(inputArray.size):
        if completeArray[t][0] != 0:
            fillWithCircles(completeArray[t], inputArray, completeArray)
    return completeArray


def orderedRandomGuessCirclePack(xDim, yDim, inputArray):
    inputArray = np.sort(inputArray)
    inputArray = inputArray[::-1]
    completeArray = np.zeros([inputArray.size, 3])
    x = 0
    failCounter = 0
    while x < inputArray.size:
        xLocation = random.randint(0, xDim)
        yLocation = random.randint(0, yDim)
        radius = inputArray[x]

        if circleLocationValid(xDim, yDim, xLocation, yLocation, radius, completeArray, x):
            completeArray[x] = [inputArray[x], xLocation, yLocation]
        else:
            x = x - 1
            failCounter = failCounter + 1
            if failCounter == inputArray.size * 50:
                return completeArray
        x = x + 1
    return completeArray


def randomGuessCirclePack(xDim, yDim, inputArray):
    completeArray = np.zeros([inputArray.size, 3])
    x = 0
    failCounter = 0
    while x < inputArray.size:
        xLocation = random.randint(0, xDim)
        yLocation = random.randint(0, yDim)
        radius = inputArray[x]

        if circleLocationValid(xDim, yDim, xLocation, yLocation, radius, completeArray, x):
            completeArray[x] = [inputArray[x], xLocation, yLocation]
        else:
            x = x - 1
            failCounter = failCounter + 1
            if failCounter == inputArray.size * 50:
                return completeArray
        x = x + 1
    return completeArray


def circleLocationValid(xDim, yDim, xLoc, yLoc, radius, completeArray, x):
    global isLocValidCalls
    isLocValidCalls = isLocValidCalls + 1

    for x in range(x):
        distance = math.dist([xLoc, yLoc], [completeArray[x][1], completeArray[x][2]])
        if xLoc + radius > xDim or xLoc - radius < 0 or yLoc + radius > yDim or yLoc - radius < 0:
            return False
        elif distance < radius + completeArray[x][0]:
            return False
    return True


def display(xDim, yDim, array):
    win = GraphWin("display", xDim, yDim)
    for x in array:
        pt = Point(x[1], x[2])
        cir = Circle(pt, x[0])
        cir.draw(win)
    win.getMouse()
    win.close()


def length(array):
    count = 0
    for x in array:
        if x[0] != 0 and x[1] != 0 and x[2] != 0:
            count = count + 1
    return count


if __name__ == '__main__':
    windowSizeX = 500
    windowSizeY = 500
    circleArray = np.empty(600, dtype=int)
    for t in range(circleArray.size):
        circleArray[t] = random.randint(4, 15)

    # finishedArray = randomGuessCirclePack(windowSizeX, windowSizeY, circleArray)
    # finishedArray = orderedRandomGuessCirclePack(windowSizeX, windowSizeY, circleArray)
    finishedArray = circularPack(windowSizeX, windowSizeY, circleArray)

    print("Total circles packed: " + str(length(finishedArray)))
    print("Total position valid checks: " + str(isLocValidCalls))
    display(windowSizeX, windowSizeY, finishedArray)
