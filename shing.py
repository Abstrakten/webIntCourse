
testStr = "a rose is a rose is a rose"

def shing(st, l):

    termList = st.split(' ')

    finalList = set()

    for (i,x) in enumerate(termList):
        lst = termList[i:i+l]
        if(len(lst) == l):
            finalList.add(tuple(lst))

    return finalList

print(shing(testStr, 4))
