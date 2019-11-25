import nltk
from nltk.tag import tnt
from nltk.corpus import indian
from cltk.corpus.swadesh import Swadesh
from cltk.stop.classical_hindi.stops import STOPS_LIST

def hindi_model():
    train_data = indian.tagged_sents('hindi.pos')
    tnt_pos_tagger = tnt.TnT()
    tnt_pos_tagger.train(train_data)
    return tnt_pos_tagger

print(STOPS_LIST[:5])
swadesh = Swadesh('hi')
print(swadesh.words()[:10])
hindi_text = 'सब छात्रों के लिए हिंदी व्याकरण से जुड़ी बहुत महत्वपूर्ण पुस्तक की तैयारी कर रहे है.'
hindi_text_tokenize = nltk.word_tokenize(hindi_text)
print(hindi_text_tokenize[0:10])
model = hindi_model()
print(model.tag(hindi_text_tokenize))

