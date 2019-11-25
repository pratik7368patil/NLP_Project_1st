import nltk
from cltk.corpus.swadesh import Swadesh
from cltk.stop.classical_hindi.stops import STOPS_LIST
from cltk.tokenize.sentence import TokenizeSentence
import os

print(STOPS_LIST[:5])
swadesh = Swadesh('hi')
print(swadesh.words()[:10])

tokenizer = TokenizeSentence('hindi')
hindi_text = 'सब छात्रों के लिए हिंदी व्याकरण से जुड़ी बहुत महत्वपूर्ण पुस्तक की तैयारी कर रहे है.'
hindi_text_tokenize = tokenizer.tokenize(hindi_text)
print(hindi_text_tokenize[0:10])
print(hindi_text.split(' '))
