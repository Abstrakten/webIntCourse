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
            negatedList = classifier.negateTokenList(tokens)
            mapping = classifier.updateMapping(mapping, negatedList)
            sorted_list = sorted(mapping.items(), key=lambda x: x[1])
            allVectors.append(classifier.tokenListToVector(negatedList, mapping))
            counter += 1

        if counter == 1000:
            print("10k reached")
            x = np.array(allVectors).reshape(-1, 1)
            y = np.array(allLabels).reshape(-1, 1)
            gnb.partial_fit(x, y, [1, 2, 3, 4, 5])
            print("Done partial training")
            allVectors = []
            allLabels = []
            counter = 0


