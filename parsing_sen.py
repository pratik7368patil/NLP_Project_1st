import nltk

#parsing sentense using nltk
text = nltk.word_tokenize("Alice loves Bob")
print(text)
grammer = nltk.CFG.fromstring("""
S -> NP VP
VP -> V NP
NP -> 'Alice' | 'Bob'
V -> 'loves'
""")
parser = nltk.ChartParser(grammer)
trees = parser.parse_all(text)
for tree in trees:
    print(tree)

#ambiguity in parsing

text2 = nltk.word_tokenize("I saw the man with a telescope")
grammer1 = nltk.data.load('grammer.cfg')
parser = nltk.ChartParser(grammer1)
trees = parser.parse_all(text2)
for tree in trees:
    print(tree)

#pos tagging and parsing complexity
#uncommon usages of words
text3 = nltk.word_tokenize("The old man the boat")
res = nltk.pos_tag(text3)
print(res)

#well formed sentences may still be meaningless!

text4 = nltk.word_tokenize("Colorless green ideas sleep furiously")
res1 = nltk.pos_tag(text4)
print(res1)
