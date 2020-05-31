from django.shortcuts import render, redirect
import sys 
from nltk.tag import tnt
from nltk.corpus import indian
import nltk
from nltk.tree import Tree
from langdetect import detect

# Create your views here.
def index(request):
    return render(request, 'home.html')

def output(request):
    text = request.POST.get('text')
    
    ######################### functions for information extraction in hindi ##########
    def hindi_model():
        train_data = indian.tagged_sents('hindi.pos')
        tnt_pos_tagger = tnt.TnT()
        tnt_pos_tagger.train(train_data)
        return tnt_pos_tagger


    def get_keywords(pos):
        grammar = r"""NP:{<NN.*>}"""
        chunkParser = nltk.RegexpParser(grammar)
        chunked = chunkParser.parse(pos)
        continuous_chunk = set()
        current_chunk = []
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.add(named_entity)
                    current_chunk = []
                else:
                    continue
        return (continuous_chunk)

    ######################## end for hindi #################

    ########### Funcitons for English #################

    def extract_eng(text):
        output = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(text)) if pos[0] == 'N']
        return output
    
    # sample input for hindi language
    # text = "इराक के विदेश मंत्री ने अमरीका के उस प्रस्ताव का मजाक उड़ाया है , जिसमें अमरीका ने संयुक्त राष्ट्र के प्रतिबंधों को इराकी नागरिकों के लिए कम हानिकारक बनाने के लिए कहा है ।"
    ########### end for english ################
    d_flag = detect(text)
    if d_flag == 'en':
        result = extract_eng(text)
        return render(request, 'home.html', {'text': result})
    elif d_flag == 'hi':
        model = hindi_model()
        new_tagged = model.tag(nltk.word_tokenize(text))
        result = list(get_keywords(new_tagged))
        return render(request, 'home.html', {'text': result})
    
    result = "Can not detect your Language, please try to extract Hindi or English."
    return render(request, 'home.html', {'text': result})