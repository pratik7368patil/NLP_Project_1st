from PyQt5 import QtCore, QtGui, QtWidgets 
import sys 
from nltk.tag import tnt
from nltk.corpus import indian
import nltk
from nltk.tree import Tree
import sys 


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

# text = "इराक के विदेश मंत्री ने अमरीका के उस प्रस्ताव का मजाक उड़ाया है , जिसमें अमरीका ने संयुक्त राष्ट्र के प्रतिबंधों को इराकी नागरिकों के लिए कम हानिकारक बनाने के लिए कहा है ।"
# text = "भारत के प्रधानमंत्री नरेंद्र मोदी हैं"
# ps_tg = nltk.pos_tag(nltk.word_tokenize(text))
# print(ps_tg)
#text =  input()
#model = hindi_model()
#new_tagged = (model.tag(nltk.word_tokenize(text)))
#print("KEYWORDS----------")
#print(get_keywords(new_tagged))
##sys.stdout.flush()

###################### UI CODE################

class Ui_MainWindow(QtWidgets.QWidget): 
    def setupUi(self, MainWindow): 
        MainWindow.resize(800, 800) 
        self.centralwidget = QtWidgets.QWidget(MainWindow) 
  
        self.pushButton = QtWidgets.QPushButton(self.centralwidget) 
        self.pushButton.setGeometry(QtCore.QRect(300, 400, 100, 50))
        
        # For displaying confirmation message along with user's info.  
        self.label = QtWidgets.QLabel(self.centralwidget)     
        self.label.setGeometry(QtCore.QRect(100, 40, 500, 111)) 
  
        # Keeping the text of label empty initially.        
        self.label.setText("")      
  
        MainWindow.setCentralWidget(self.centralwidget) 
        self.retranslateUi(MainWindow) 
        QtCore.QMetaObject.connectSlotsByName(MainWindow) 
  
    def retranslateUi(self, MainWindow): 
        _translate = QtCore.QCoreApplication.translate 
        MainWindow.setWindowTitle(_translate("MainWindow", "Hindi Keyword Extraction")) 
        self.pushButton.setText(_translate("MainWindow", "Proceed")) 
        self.pushButton.clicked.connect(self.takeinputs) 
          
    def takeinputs(self): 
        name, done1 = QtWidgets.QInputDialog.getText( 
             self, 'Input Dialog', 'Enter your Data:')  
        text = str(name)
        model = hindi_model()
        new_tagged = (model.tag(nltk.word_tokenize(text)))
        result = get_keywords(new_tagged)
  
        if done1: 
             # Showing confirmation message along 
             # with information provided by user.  
             self.label.setText('Keywords Are: \n'
                                 + str(result))    
   
             # Hide the pushbutton after inputs provided by the use. 
             self.pushButton.hide()       
                


if __name__ == "__main__":  
    app = QtWidgets.QApplication(sys.argv)  
    MainWindow = QtWidgets.QMainWindow()  
    ui = Ui_MainWindow()  
    ui.setupUi(MainWindow)  
    MainWindow.show()
  
    sys.exit(app.exec_())  