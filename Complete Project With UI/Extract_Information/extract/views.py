# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
import sys 
from nltk.tag import tnt
from nltk.corpus import indian
import nltk
from nltk.tree import Tree
from langdetect import detect
from bs4 import BeautifulSoup
import requests
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

# Extract Urls
def get_all_url(text):
    return re.findall(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?', text)

# Format urls in same fashion to render
def format_urls(urls):
    res = []
    for url in urls:
        res.append(get_all_url(url)[0])
    return res;

# filtering out unnecessary characters
def filter_special_char(text):
    chars = {'|','[', ']', '.', ',', '{', '}', '(', ')', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '=', '_', '-', '+', '<', '>', '?', '/'}
    for i in chars:
        text = text.replace(i, ' ');
    return text

# Filtering result
def filter_result(text, urls = []):
    for url in urls:
        for item in url:
            text = text.replace(item, '');
    text = filter_special_char(text)
    return text

# Removing duplicates from result
def filter_dummy_result(result):
    d = set()
    for word in result:
        if len(word) > 1:
            d.add(word.lower())
    return list(d)

# Extracting dates
def filter_dates(text):
    regex = r'(?:\d{1,2}[-/th|st|nd|rd\s.])?(?:(?:Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|August|Sep|September|Oct|October|Nov|November|Dec|December)[\s,.]*)?(?:(?:\d{1,2})[-/th|st|nd|rd\s,.]*)?(?:\d{2,4})'
    dates = re.findall(regex, text)
    res = []
    for date in dates:
        if ' '  in date:
            res.append(date)
    return res

# Making request to URL given by user to get HTML content
def getHTMLdocument(url):
    response = requests.get(url)
    return response.text

def output(request):
    text = request.POST.get('text')
    link = request.POST.get('link')

    try:
        if text.strip() == '' and link.strip() == '':
            return render(request, 'error.html')
    except:
        return render(request, 'error.html')
    
    d_flag = ''
    urls = get_all_url(text)
    text = filter_result(text, urls)
    dates = filter_dates(text)
    soup = ''
    article = ''
    if link.strip() != '':
        doc = getHTMLdocument(link)
        soup = BeautifulSoup(doc, 'html.parser')
        for para in soup.find_all('p'):
            article += para.get_text();
        try:
            d_flag = detect(article)
        except:
            return render(request, 'error.html')
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            urls.append(link.get('href'))
        urls = format_urls(urls)

    try:
        if text.strip() != '':
            d_flag = detect(text)
    except:
        return render(request, 'error.html')

    if d_flag == 'en': # Extracting for English Language
        if text.strip() != '':
            result = list(set(extract_eng(text)))
        if article.strip() != '':
            result = list(set(extract_eng(article)))
        result = filter_dummy_result(result)
        return render(request, 'home.html', {'text': result, 'urls': urls, 'dates': dates})
    elif d_flag == 'hi': # Extracting for Hindi Language
        model = hindi_model()
        new_tagged = []
        if text.strip() != '':
            new_tagged = model.tag(nltk.word_tokenize(text))
        if article.strip() != '':
            new_tagged = model.tag(nltk.word_tokenize(article))
        result = list(set(get_keywords(new_tagged)))
        return render(request, 'home.html', {'text': result, 'urls': urls, 'dates': dates})

    return render(request, 'error.html')
