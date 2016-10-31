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
        negated += negate(sentence)
    return list(set(negated))



def updateMapping(mapping, tokens):
    length = len(mapping)
    i = 0
    for word in tokens:
        if word not in mapping:
            mapping[word] = i + length
            i += 1
    return mapping

def tokenListToVector(tokenList, mapping):
    vector = [0 for i in range(0, len(mapping))]
    for word in tokenList:
        i = mapping[word]
        vector[i] = 1
    return np.array(vector)


# gnb.fit(vectorList, labels)

# print(mapping)

# test = negate("i like pizza don't i".split())
# print(gnb.predict(sentenceToVector(test)))
