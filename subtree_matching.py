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

text = "Tableau was recently acquired by Salesforce." 

doc = nlp(text) 
# print dependancy and pos tagging.
#for tok in doc: 
 # print(tok.text,"-->",tok.dep_,"-->",tok.pos_)

# subtree matcher for 
def subtree_matcher(doc):
  subjpass = 0

  for i,tok in enumerate(doc):
    # find dependency tag that contains the text "subjpass"    
    if tok.dep_.find("subjpass") == True:
      subjpass = 1

  x = ''
  y = ''

  # if subjpass == 1 then sentence is passive
  if subjpass == 1:
    for i,tok in enumerate(doc):
      if tok.dep_.find("subjpass") == True:
        y = tok.text

      if tok.dep_.endswith("obj") == True:
        x = tok.text
  
  # if subjpass == 0 then sentence is not passive
  else:
    for i,tok in enumerate(doc):
      if tok.dep_.endswith("subj") == True:
        x = tok.text

      if tok.dep_.endswith("obj") == True:
        y = tok.text

  return x,y

# extract doc using above function
print(subtree_matcher(doc))
print(subtree_matcher(nlp("Salesforce recently acquired Tableau.")))

