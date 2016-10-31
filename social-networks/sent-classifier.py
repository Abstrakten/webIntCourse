from sklearn.naive_bayes import GaussianNB
import numpy as np
import nltk.sentiment.vader as vader
import classifier
import happyfuntokenizer

gnb = GaussianNB()

with open("SentimentTrainingData.txt", "r", encoding="utf-8") as f:
    t = happyfuntokenizer.Tokenizer()
    allVectors = []
    allLabels = []
    mapping = {}
    length = 0
    reviewPrefix = "review/text: "
    labelPrefix = "review/score: "
    counter = 0
    for line in f:
        if line[:14] == labelPrefix:
            allLabels.append(int(line.replace(labelPrefix, "").split(".")[0]))

        if line[:13] == reviewPrefix:
            text = line.replace(reviewPrefix, "")
            sentences = text.split(". ")
            tokens = [t.tokenize(sentence) for sentence in sentences]
            mapping, length = classifier.updateMapping(mapping, length, tokens)
            negatedList = classifier.negateTokenList(tokens)
            allVectors.append(classifier.tokenListToVectors(tokens, mapping, length))
            counter += 1

        if counter == 10000:
            print("10k reached")
            gnb.partial_fit(allVectors,allLabels,[1,2,3,4,5])
            allVectors = []
            allLabels = []
            counter = 0


