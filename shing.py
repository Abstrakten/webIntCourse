import hashlib
import math
import random

shingleSize = 4
hashFuncNum = 84
bigPrime = 4294967311
maxShingleID = 2**32-1
superShingleNum = 6
superShingleSize = 14
superShingleThreshold = 2


randomListA = [random.randint(0, maxShingleID) for x in range(0, hashFuncNum)]
randomListB = [random.randint(0, maxShingleID) for x in range(0, hashFuncNum)]

testStr = "a rose is a rose is a rose"
testStr2 = "rose is a rose is a rose a"
testStr3 = "violet is a rose is a violet"

mathstring1 = "Do not worry about your diffulties in Mathematics, I assure you that mine are still greater"
mathstring2 = "Dont worry about your diffulties in Mathematics, I assure you that mine are still greater"

mathstring3 = "Do not worry about your diffulties in Mathematics"
mathstring4 = "Di not worry about your diffulties in Mathematics"

def shing(st, l):

    termList = st.split(' ')

    finalList = set()

    for (i,x) in enumerate(termList):
        lst = termList[i:i+l]
        if(len(lst) == l):
            finalList.add(" ".join(lst))

    return finalList

#print(shing(testStr, shingleSize))

def jaccard(string1, string2):
    return len(shing(string1, shingleSize).intersection(shing(string2, shingleSize)))/len(shing(string1, shingleSize).union(shing(string2,shingleSize)))

def shinglesToIntegers(shingleSet):

    arr = []

    for x in shingleSet:
        arr.append(int(hashlib.sha1(x.encode('utf-8')).hexdigest(), 16))

    return arr

def minHashVal(shingleSet):

    shingleIntSet = shinglesToIntegers(shingleSet)
    resultList = [math.inf for x in range(0, hashFuncNum)]

    for i in range(0, hashFuncNum):
        a = randomListA[i]
        b = randomListB[i]

        for x in shingleIntSet:
            minVal = (a*x+b) % bigPrime
            if(resultList[i] > minVal):
                resultList[i] = minVal

    return resultList

#print(minHashVal(shing(mathstring3, shingleSize)))
#print(len(minHashVal(shing(mathstring3, shingleSize))))

def shinglesCompare(arr1, arr2):

    positiveMatches = 0

    for (x,y) in zip(arr1, arr2):
        #print(str(x))
        #print(str(y))
        #print()
        if(x == y):
            positiveMatches += 1

    return positiveMatches

def makeSuperShingle(minShingleSet):

    finalArr = []

    for i in range(0,superShingleNum):
        currentMinArr = minShingleSet[i*superShingleSize:(i+1)*superShingleSize]
        stringArr = [str(x) for x in currentMinArr] 
        superShingleString = "".join(stringArr)
        finalArr.append(int(hashlib.sha1(superShingleString.encode('utf-8')).hexdigest(), 16))

    return finalArr


def compareSuperShingle(superShingleSet1, superShingleSet2):

    positiveMatches = 0
    for (x,y) in zip(superShingleSet1,superShingleSet2):
        if(x == y):
            positiveMatches += 1

    return positiveMatches


def checkNearDuplicate(string1, string2):
    minShingleSet1 = minHashVal(shing(string1, shingleSize))
    minShingleSet2 = minHashVal(shing(string2, shingleSize))

    superShingleSet1 = makeSuperShingle(minShingleSet1)
    superShingleSet2 = makeSuperShingle(minShingleSet2)

    if(superShingleThreshold > compareSuperShingle(superShingleSet1,superShingleSet2)):
        return compareSuperShingle(superShingleSet1,superShingleSet2)

    return (shinglesCompare(minShingleSet1,minShingleSet2)/hashFuncNum)*100












#print (makeSuperShingle(minHashVal(shing(mathstring1,shingleSize))))

print (checkNearDuplicate(mathstring1,mathstring2))

#print (shinglesCompare(testStr, testStr2))
#print (shinglesCompare(testStr, testStr3))

#print (shinglesToIntegers(shing(mathstring1,4)))
#print (shinglesToIntegers(shing(mathstring2,4)))
print (jaccard(mathstring1, mathstring2))
