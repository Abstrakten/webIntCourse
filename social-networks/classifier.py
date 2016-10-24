import happyfuntokenizer
from sklearn.naive_bayes import GaussianNB
import numpy as np
import nltk.sentiment.vader as vader

gnb = GaussianNB()

reviews = ["i like pizza", "i don't like pizza", "i hate pizza", "i fucking love pizza"]
labels = [1, 0, 0, 1]


t = happyfuntokenizer.Tokenizer()
tokens = [t.tokenize(s) for s in reviews]


def negate(sentence):
    negSentence = sentence
    negateWords = vader.NEGATE
    for i, word in enumerate(sentence):
        if word in negateWords:
            head = sentence[0:i+1]
            tail = [w + "_NEG" for w in sentence[i+1:]]
            negSentence = head + tail
            return negSentence
    return negSentence

def negateTokenList(tokens):
    negated = []
    for sentence in tokens:
        negated.append(negate(sentence))
    return negated



def updateMapping(mapping, length, tokenList):
    tokens = list(set(sum(tokenList, [])))
    flattened = sum([[x, x + "_NEG"] for x in tokens], [])
    for i, word in enumerate(flattened):
        if word not in mapping:
            mapping[word] = i + length
    return (mapping, i + length)



def sentenceToVector(sentence, mapping, length):
    vector = [0 for i in range(0, length)]
    for word in sentence:
        i = mapping[word]
        vector[i] = 1
    return vector

def tokenListToVectors(line, mapping, length):
    vectorList = []
    for sentence in line:
        vectorList.append(sentenceToVector(sentence, mapping, length))
    return vectorList


# gnb.fit(vectorList, labels)

# print(mapping)

# test = negate("i like pizza don't i".split())
# print(gnb.predict(sentenceToVector(test)))
