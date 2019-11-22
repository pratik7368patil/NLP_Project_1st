from nltk.book import *
import nltk
# Friquency of words
dist = FreqDist(text7)
print(len(dist))

# List of dist words
vocab1 = list(dist.keys())
print(vocab1[:10])

# form tokens with nltk
text12 = 'Recall from your high school grammar. that part-of-speech are these. verb classes like nouns, and verbs, and adjectives.'
token = nltk.word_tokenize(text12)
print(token)
print(len(token))

sen = nltk.sent_tokenize(text12)
print(len(sen))
print(sen)
result = nltk.pos_tag(sen[0])
print(result)
print(sen[0])
