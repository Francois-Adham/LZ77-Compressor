import cv2
import numpy as np

BestPointer = 0
flag = 0
searchBufferPointer = 0
BestMatchLength = 0
BestMatchJump = 0
lookAheadPointer = 0
tempMatch = 0


def get_match():
    global k, BestPointer, BestMatchLength, tempMatch, lookAheadPointer, searchBufferPointer
    while searchBufferPointer < searchBufferLength:
        if searchBufferList[searchBufferPointer] == lookAheadList[lookAheadPointer]:
            tempMatch += 1
            searchBufferPointer += 1
            lookAheadPointer += 1
        else:
            tempMatch = 0
            searchBufferPointer += 1
            lookAheadPointer = 0
        if BestMatchLength < tempMatch:
            BestMatchLength = tempMatch
            BestPointer = searchBufferPointer - BestMatchLength
    if BestMatchLength < len(lookAheadList):
        if lookAheadList[BestMatchLength] == searchBufferList[BestPointer]:
            BestMatchLength += 1
            tempPointer = BestPointer + 1
            while k < (lookAheadLength-BestMatchLength):
                if lookAheadList[BestMatchLength] == searchBufferList[tempPointer]:
                    BestMatchLength += 1
                    tempPointer += 1
                else:
                   break
                k += 1
    return


# getting info from user
# path = input("Enter Image Path: ")--------------------------------------------------------------
slidingWindow = input("Enter length of sliding window: ")
slidingWindow = int(slidingWindow)
lookAheadLength = input("Enter look-ahead size: ")
lookAheadLength = int(lookAheadLength)
searchBufferLength = slidingWindow - lookAheadLength
i = slidingWindow
# reading the image
# img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)----------------------------------------------------
# flatting the image
# flattened = [val for sublist in img for val in sublist]---------------------------------------------
flattened = ['c', 'a', 'b', 'r', 'a', 'c', 'a', 'd', 'a', 'b', 'r', 'a', 'r', 'r', 'a', 'r', 'r', 'a', 'd', 'f', 'f']
if lookAheadLength > slidingWindow:
    print('Invalid Values')
    exit()

if slidingWindow > 256:
    jumpList = np.array([], dtype=np.uint16)
    wordLengthList = np.array([], dtype=np.uint16)
else:
    jumpList = np.array([], dtype=np.uint8)
    wordLengthList = np.array([], dtype=np.uint8)

codes = np.array([], dtype=np.uint8)
# codes = np.append(codes, 10)
# print(len(codes))
# print(codes)

while i < len(flattened):
    searchBufferList = flattened[flag:flag + searchBufferLength]
    lookAheadList = flattened[flag + searchBufferLength:flag + searchBufferLength + lookAheadLength]
    k = 0
    searchBufferPointer = 0
    BestMatchLength = 0
    BestMatchJump = 0
    lookAheadPointer = 0
    tempMatch = 0
    get_match()
    i += (BestMatchLength+1)
    flag += (BestMatchLength + 1)
    if BestMatchLength > 0:
        jumpList = np.append(jumpList, searchBufferLength-BestPointer)
        wordLengthList = np.append(wordLengthList, BestMatchLength)
    else:
        jumpList = np.append(jumpList, 0)
        wordLengthList = np.append(wordLengthList, 0)
    codes = np.append(codes, lookAheadList[BestMatchLength])

i -= BestMatchLength+1
remainingLength = (len(flattened) % i)
if remainingLength:
    remainingPointer = 0
    while remainingPointer < remainingLength:
        k = 0
        searchBufferPointer = 0
        BestMatchLength = 0
        BestMatchJump = 0
        lookAheadPointer = 0
        tempMatch = 0
        lookAheadList = flattened[len(flattened)-remainingLength+remainingPointer:]
        searchBufferList = flattened[len(flattened)-remainingLength-searchBufferLength+remainingPointer:
                                     len(flattened)-remainingLength+remainingPointer]
        get_match()
        if BestMatchLength > 0:
            jumpList = np.append(jumpList, searchBufferLength - BestPointer)
            wordLengthList = np.append(wordLengthList, BestMatchLength)
        else:
            jumpList = np.append(jumpList, 0)
            wordLengthList = np.append(wordLengthList, 0)
        if BestMatchLength < len(lookAheadList):
            codes = np.append(codes, lookAheadList[BestMatchLength])
        else:
            codes = np.append(codes, '$')
        remainingPointer += 1
print(remainingLength)
print(codes)
