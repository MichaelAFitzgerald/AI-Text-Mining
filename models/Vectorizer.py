import pandas as pd
import string

# A - tokenizer
from models.Porter_Stemmer import PorterStemmer


def tokenizer(document):
    return document.split()


def punctRemover(sentList):
    removed = []
    for line in sentList:
        removed.append(line.translate(str.maketrans('', '', string.punctuation)))
    return removed


def numRemover(sentList):
    removed = []
    for line in sentList:
        removed.append(line.translate(str.maketrans('', '', string.digits)))
    return removed


def capsRemover(sentList):
    removed = []
    for line in sentList:
        removed.append(line.translate(str.maketrans(string.ascii_uppercase, string.ascii_lowercase)))
    return removed


def stopRemover(sentList):
    stopWords = pd.read_table('data/stop_words.txt', header=None)
    stopWords = stopWords.to_string()
    removed = [word for word in sentList if word not in stopWords]
    return removed


def stemmer(sentList):
    p = PorterStemmer()
    stems = []
    for line in sentList:
        out = p.stem(line, 0, len(line) - 1)
        stems.append(out)
    return stems


def concat(sentList):
     return set(sentList)


def freqFinder(sentList, document, num):
    doc = [[]]
    for sentence in document.split('\n'):
        histogram = []
        for gram in sentList:
            histogram.append(sentence.count(gram))
        doc.append(histogram)
    df = pd.DataFrame(doc[1:], columns=sentList)
    for x in sentList:
        if df[x].sum() < num:
            df.drop(x, axis=1, inplace=True)
    return df
