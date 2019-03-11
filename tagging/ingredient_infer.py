import re
import pickle
from nltk import pos_tag, word_tokenize
from fractions import Fraction

class IngredientPredict:

    def __init__(self):
        self.dict_ = {'qty': [], 'unit': [], 'name': [], "comment": []}

        f = open('./tagging/ingredient.pickle', 'rb')
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
                self.dict_['qty'].append(word)
            elif 'FAC' in ner:
                self.dict_['unit'].append(word)
            elif 'PRODUCT' in ner:
                self.dict_['name'].append(word)
            else:
                self.dict_["comment"].append(word)

        return self.dict_

    def get_taggings(self, phrase):
        dict = self.predict_new(phrase)
        taggings = {}
        name = " ".join(dict["name"])
        comment = " ".join(dict["comment"])
        taggings["qty"] = float(dict["qty"][0])
        taggings["unit"] = str(dict["unit"][0])
        taggings["name"] = name
        taggings["comment"] = comment
        return taggings