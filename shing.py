
testStr = "a rose is a rose is a rose"

termList = testStr.split(' ')

finalList = []

for (i,x) in enumerate(termList):
    lst = termList[i:i+3]
    if(len(lst) == 3):
        finalList.append(termList[i:i+3])

print(finalList)
