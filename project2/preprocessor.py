'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')


class Preprocessor:

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
        Write the code in such a way that it can be re-used for processing
        the user's query.
        """
        #convert document text to all lower cases
        text = text.lower()
        #print(text)
        
        #removing special characters
        text_without_spcl = ''
        for character in text:
             if  character == " ":
                #checking charcter is space and if yes concat
                text_without_spcl = text_without_spcl + character
             else:
                if(character.isalnum()):
                    text_without_spcl = text_without_spcl + character
        #print(text_without_spcl)
                
        text_without_ws = text_without_spcl.strip()
        #print(text_without_ws)
        
        text_without_ws=re.sub(' +', ' ', text_without_spcl)
        
        tokenized_text=text_without_ws.split()
        #print(tokenized_text)
        
        tokens_without_sw = [word for word in tokenized_text if not word in self.stop_words]
        
        #print(tokens_without_sw)
        
        tokens_stemmed=[]
        for tokens in tokens_without_sw:
           tokens_stemmed.append(self.ps.stem(tokens))
        
        #print(tokens_stemmed)
        
        return tokens_stemmed
