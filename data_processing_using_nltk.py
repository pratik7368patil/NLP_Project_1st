from nltk.book import *
import nltk
# Friquency of words
dist = FreqDist(text7)
print(len(dist))

# List of dist words
vocab1 = list(dist.keys())
print(vocab1[:10])
