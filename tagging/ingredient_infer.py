import re
import pickle
from nltk import pos_tag, word_tokenize
#from nltk.chunk import conlltags2tree, tree2conlltags
from fractions import Fraction

class IngredientPredict:
    def __init__(self):
        self.dict_ = {'qty': set(), 'unit': set(), 'name': []}

        f = open('ingrdient.pickle', 'rb')
        self.classifier = pickle.load(f)
        f.close()

    def convert_decimal(self,text):
        try:
            text_split = text.split()
            if text_split[0].isdigit() and '/' in text_split[1]:
                fraction = round(float(sum(Fraction(s) for s in [text_split[0], text_split[1]])), 2)
                text = text.replace(' '.join([text_split[0], text_split[1]]), str(fraction))
                return text
            else:
                return text
        except:
            return text

    def predict_new(self,text):

        text = text.lower()
        text = re.sub(r'[,.!?()-+|]+', ' ', text)
        text = self.convert_decimal(text)

        chunked = self.classifier.tag(pos_tag(word_tokenize(text)))

        for tag, ner in chunked:
            word, pos = tag
            if 'QUANTITY' in ner:
                self.dict_['qty'].add(word)
            elif 'FAC' in ner:
                self.dict_['unit'].add(word)
            elif 'PRODUCT' in ner:
                self.dict_['name'].append(word)

        return self.dict_