import hashlib
import math

shingleSize = 4

testStr = "a rose is a rose is a rose"
testStr2 = "rose is a rose is a rose a"
testStr3 = "violet is a rose is a violet"

mathstring1 = "Do not worry about your diffulties in Mathematics, I assure you that mine are still greater"
mathstring2 = "Do not worry about your diffulties in Mathematics, I assure you that mine are still greater"

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

print(shing(testStr, shingleSize))

def jaccard(string1, string2):
    return len(shing(string1, shingleSize).intersection(shing(string2, shingleSize)))/len(shing(string1, shingleSize).union(shing(string2,shingleSize)))
       
def hashingFunctions(functionNumber, x):

    encoded = x.encode('utf-8')

    if(functionNumber == 0):
        return int(hashlib.sha256(encoded).hexdigest(), 16)

    if(functionNumber == 1):
        return int(hashlib.sha1(encoded).hexdigest(), 16)

    if(functionNumber == 2):
        return int(hashlib.sha224(encoded).hexdigest(), 16)

    if(functionNumber == 3):
        return int(hashlib.sha384(encoded).hexdigest(), 16)

    if(functionNumber == 4):
        return int(hashlib.sha512(encoded).hexdigest(), 16)

def fiveHash(shingleSet):

    finalArray = [math.inf for x in range(0,5)]

    for x in shingleSet:
        for i in range(0,5):
            if(finalArray[i] > hashingFunctions(i,x)):
                finalArray[i] = hashingFunctions(i,x)

    return finalArray

#print(fiveHash(shing(testStr, 4)))

def shinglesCompare(str1, str2):
    arr1 = fiveHash(shing(str1,shingleSize))
    arr2 = fiveHash(shing(str2,shingleSize))

    positiveMatches = 0

    for (x,y) in zip(arr1, arr2):
        if(x == y):
            positiveMatches += 1

    return positiveMatches

#print (shinglesCompare(testStr, testStr2))
#print (shinglesCompare(testStr, testStr3))

print (shinglesCompare(mathstring3,mathstring4))
print (shinglesCompare(mathstring3,mathstring3))
print (jaccard(mathstring3, mathstring4))










        

        
        
