from sklearn.naive_bayes import GaussianNB
import numpy as np
import nltk.sentiment.vader as vader
import classifier
import happyfuntokenizer

with open("SentimentTrainingData.txt", "r", encoding="utf-8") as f:
    t = happyfuntokenizer.Tokenizer()
    allVectors = []
    allLabels = []
    mapping = {}
    length = 0
    reviewPrefix = "review/text: "
    labelPrefix = "review/score: "
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

    print(allVectors)
    print(allLabels)
