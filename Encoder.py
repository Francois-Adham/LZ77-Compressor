import cv2
import numpy as np

# getting info from user
path = input("Enter Image Path: ")
slidingWindow = input("Enter length of sliding window: ")
slidingWindow = int(slidingWindow)
lookAheadLength = input("Enter look-ahead size: ")
lookAheadLength = int(lookAheadLength)
searchBufferLength = slidingWindow - lookAheadLength

# reading the image
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

# flatting the image
flattened = [val for sublist in img for val in sublist]

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

BestPointer = 0
i = slidingWindow
flag = 0
while i < len(flattened):
    k = 0
    searchBufferList = flattened[flag:flag+searchBufferLength]
    lookAheadList = flattened[flag+searchBufferLength:flag+searchBufferLength+lookAheadLength]
    searchBufferPointer = 0
    BestMatchLength = 0
    BestMatchJump = 0
    lookAheadPointer = 0
    tempMatch = 0
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
    i += (BestMatchLength+1)
    flag += (BestMatchLength + 1)
    if BestMatchLength > 0:
        jumpList = np.append(jumpList, searchBufferLength-BestPointer)
        wordLengthList = np.append(wordLengthList, BestMatchLength)
    else:
        jumpList = np.append(jumpList, 0)
        wordLengthList = np.append(wordLengthList, 0)
    codes = np.append(codes, lookAheadList[BestMatchLength])

