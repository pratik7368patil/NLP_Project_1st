import re 
import string 
import nltk 
import spacy 
import pandas as pd 
import numpy as np 
import math 
from tqdm import tqdm 

from spacy.matcher import Matcher 
from spacy.tokens import Span 
from spacy import displacy 

pd.set_option('display.max_colwidth', 200)
# load spaCy model
nlp = spacy.load("en_core_web_sm")
# sample text 
text = "GDP in developing countries such as Vietnam will continue growing at a high rate. Fruits such as apples Cars such as Ferrari Flowers such as rose" 

# create a spaCy object 
doc = nlp(text)

# print token, dependency, POS tag 
for tok in doc: 
  print(tok.text, "-->",tok.dep_,"-->", tok.pos_)

#define the pattern 
pattern = [{'POS':'NOUN'}, 
           {'LOWER': 'such'}, 
           {'LOWER': 'as'}, 
           {'POS': 'PROPN'}] # Proper Noun

# Matcher class object 
matcher = Matcher(nlp.vocab) 
matcher.add("matching_1", None, pattern) 

matches = matcher(doc) 
span = doc[matches[0][1]:matches[0][2]] 

print(span.text) # gives output of such as pattern X such as Y
#modify result for such as pattern 
# Matcher class object
matcher = Matcher(nlp.vocab)

#define the pattern
pattern = [{'DEP':'amod', 'OP':"?"}, # adjectival modifier
           {'POS':'NOUN'},
           {'LOWER': 'such'},
           {'LOWER': 'as'},
           {'POS': 'PROPN'}]

matcher.add("matching_1", None, pattern)
matches = matcher(doc)

span = doc[matches[0][1]:matches[0][2]]
print(span.text) # gives output for X such as Y


# for new pattern
doc = nlp("Here is how you can keep your car and other vehicles or truck clean.") 

# print dependency tags and POS tags
#for tok in doc: 
 # print(tok.text, "-->",tok.dep_, "-->",tok.pos_)

# Matcher class object 
matcher = Matcher(nlp.vocab) 

#define the pattern 
pattern = [{'DEP':'amod', 'OP':"?"}, 
           {'POS':'NOUN'}, 
           {'LOWER': 'and', 'OP':"?"}, 
           {'LOWER': 'or', 'OP':"?"}, 
           {'LOWER': 'other'}, 
           {'POS': 'NOUN'}] 
           
matcher.add("matching_1", None, pattern) 

matches = matcher(doc) 
span = doc[matches[0][1]:matches[0][2]] 
print(span.text) # gives output of and/or pattern X and/or Y

# for pattern X,including Y
doc = nlp("Eight people, including two children, were injured in the explosion") 

#for tok in doc: 
 # print(tok.text, "-->",tok.dep_, "-->",tok.pos_)

# Matcher class object 
matcher = Matcher(nlp.vocab) 

#define the pattern 
pattern = [{'DEP':'nummod','OP':"?"}, # numeric modifier 
           {'DEP':'amod','OP':"?"}, # adjectival modifier 
           {'POS':'NOUN'}, 
           {'IS_PUNCT': True}, 
           {'LOWER': 'including'}, 
           {'DEP':'nummod','OP':"?"}, 
           {'DEP':'amod','OP':"?"}, 
           {'POS':'NOUN'}] 
                               
matcher.add("matching_1", None, pattern) 

matches = matcher(doc) 
span = doc[matches[0][1]:matches[0][2]] 
print(span.text)

# pattern for X,especially Y
doc = nlp("A healthy eating pattern includes fruits, especially whole fruits.") 

#for tok in doc: 
 # print(tok.text, tok.dep_, tok.pos_)

# Matcher class object 
matcher = Matcher(nlp.vocab)

#define the pattern 
pattern = [{'DEP':'nummod','OP':"?"}, 
           {'DEP':'amod','OP':"?"}, 
           {'POS':'NOUN'}, 
           {'IS_PUNCT':True}, 
           {'LOWER': 'especially'}, 
           {'DEP':'nummod','OP':"?"}, 
           {'DEP':'amod','OP':"?"}, 
           {'POS':'NOUN'}] 
           
matcher.add("matching_1", None, pattern) 

matches = matcher(doc) 
span = doc[matches[0][1]:matches[0][2]] 
print(span.text)



