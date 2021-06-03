from django.shortcuts import render, redirect
import sys 
from nltk.tag import tnt
from nltk.corpus import indian
import nltk
from nltk.tree import Tree
from langdetect import detect
import re

# Create your views here.
def index(request):
    return render(request, 'home.html')

# Hindi model
def hindi_model():
    train_data = indian.tagged_sents('hindi.pos')
    tnt_pos_tagger = tnt.TnT()
    tnt_pos_tagger.train(train_data)
    return tnt_pos_tagger

# Extract Hindi keywords
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

# Extract English keywords
def extract_eng(text):
    output = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(text)) if pos[0] == 'N']
    return output
# sample input for hindi language
# text = "इराक के विदेश मंत्री ने अमरीका के उस प्रस्ताव का मजाक उड़ाया है , जिसमें अमरीका ने संयुक्त राष्ट्र के प्रतिबंधों को इराकी नागरिकों के लिए कम हानिकारक बनाने के लिए कहा है ।"

def get_all_url(text):
    return re.findall(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?', text)

def filter_special_char(text):
    chars = {'|','[', ']', '.', ',', '{', '}', '(', ')', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '=', '_', '-', '+', '<', '>', '?', '/'}
    for i in chars:
        text = text.replace(i, ' ');
    return text

def filter_result(text, urls = []):
    for url in urls:
        for item in url:
            text = text.replace(item, '');
    text = filter_special_char(text)
    return text

def filter_dummy_result(result):
    d = set()
    for word in result:
        d.add(word.lower())
    return list(d)

def output(request):
    text = request.POST.get('text')
    if text.strip() == '':
        return render(request, 'error.html')
    
    d_flag = ''
    urls = get_all_url(text)
    text = filter_result(text, urls)

    try:
        d_flag = detect(text)
    except:
        return render(request, 'error.html')

    if d_flag == 'en':
        result = list(set(extract_eng(text)))
        result = filter_dummy_result(result)
        return render(request, 'home.html', {'text': result, 'urls': urls})
    elif d_flag == 'hi':
        model = hindi_model()
        new_tagged = model.tag(nltk.word_tokenize(text))
        result = list(set(get_keywords(new_tagged)))
        return render(request, 'home.html', {'text': result, 'urls': urls})

    return render(request, 'error.html')
