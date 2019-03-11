import nltk
import re
import string
import pickle
import pandas as pd
from pathlib import Path
from fractions import Fraction
from nltk.stem.snowball import SnowballStemmer
from collections import Iterable
from nltk.tag import ClassifierBasedTagger
from nltk.chunk import ChunkParserI
from nltk.chunk import conlltags2tree
from nltk import pos_tag, word_tokenize


def convert_decimal(text):
  try:
    text_split = text.split()
    if text_split[0].isdigit() and '/' in text_split[1]:
       fraction = round(float(sum(Fraction(s) for s in [text_split[0],text_split[1]])),2)
       text = text.replace(' '.join([text_split[0],text_split[1]]), str(fraction))
       return text
    elif '/' in text_split[0]:
        value = float(Fraction(text_split[0]))
        text = text.replace(text_split[0], str(value))
        return text
    else:
       return text
  except:
       return text


def pos_category(text):
    pos_categories = []

    pos_tag = text.lower()
    pos_tag = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(pos_tag))

    for each_cat in pos_tag:
        pos_ = []
        for each_sub in each_cat:
            pos_.append(each_sub[1])
        pos_categories.append(' '.join(pos_))

    return pos_categories[0]


def tagging(series):
    result = []
    text_split = series['input'].split()
    tagger_split = series['pos_tagger'].split()

    for i in range(len(text_split)):

        if text_split[i] in str(series['qty']):
            value = 'qty'
        elif str(series['unit']) in text_split[i]:
            value = 'unit'
        elif text_split[i] in str(series['name']):
            value = 'name'
        else:
            value = 'O'

        val = ((text_split[i], tagger_split[i]), value)
        result.append(val)

    return result


def features(tokens, index, history):
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    `history` = the previous predicted IOB tags
    """

    # init the stemmer
    stemmer = SnowballStemmer('english')

    # Pad the sequence with placeholders
    tokens = [('[START2]', '[START2]'), ('[START1]', '[START1]')] + list(tokens) + [('[END1]', '[END1]'),
                                                                                    ('[END2]', '[END2]')]
    history = ['[START2]', '[START1]'] + list(history)

    # shift the index with 2, to accommodate the padding
    index += 2

    word, pos = tokens[index]
    prevword, prevpos = tokens[index - 1]
    prevprevword, prevprevpos = tokens[index - 2]
    nextword, nextpos = tokens[index + 1]
    nextnextword, nextnextpos = tokens[index + 2]
    previob = history[index - 1]
    contains_dash = '-' in word
    contains_dot = '.' in word
    allascii = all([True for c in word if c in string.ascii_lowercase])

    allcaps = word == word.capitalize()
    capitalized = word[0] in string.ascii_uppercase

    prevallcaps = prevword == prevword.capitalize()
    prevcapitalized = prevword[0] in string.ascii_uppercase

    nextallcaps = prevword == prevword.capitalize()
    nextcapitalized = prevword[0] in string.ascii_uppercase

    return {
        'word': word,
        'lemma': stemmer.stem(word),
        'pos': pos,
        'all-ascii': allascii,

        'next-word': nextword,
        'next-lemma': stemmer.stem(nextword),
        'next-pos': nextpos,

        'next-next-word': nextnextword,
        'nextnextpos': nextnextpos,

        'prev-word': prevword,
        'prev-lemma': stemmer.stem(prevword),
        'prev-pos': prevpos,

        'prev-prev-word': prevprevword,
        'prev-prev-pos': prevprevpos,

        'prev-iob': previob,

        'contains-dash': contains_dash,
        'contains-dot': contains_dot,

        'all-caps': allcaps,
        'capitalized': capitalized,

        'prev-all-caps': prevallcaps,
        'prev-capitalized': prevcapitalized,

        'next-all-caps': nextallcaps,
        'next-capitalized': nextcapitalized,
    }


def to_conll_iob(annotated_sentence):
    """
    `annotated_sentence` = list of triplets [(w1, t1, iob1), ...]
    Transform a pseudo-IOB notation: O, PERSON, PERSON, O, O, LOCATION, O
    to proper IOB notation: O, B-PERSON, I-PERSON, O, O, B-LOCATION, O
    """
    proper_iob_tokens = []
    for idx, annotated_token in enumerate(annotated_sentence):
        pos, ner = annotated_token
        tag, word = pos
        if ner != 'O':

            if ner == 'name':
                ner = 'PRODUCT'
            elif ner == 'qty':
                ner = 'QUANTITY'
            else:
                ner = 'FAC'

            if idx == 0:
                ner = "B-" + ner
            elif annotated_sentence[idx - 1][1] == ner:
                ner = "I-" + ner
            else:
                ner = "B-" + ner
        proper_iob_tokens.append(((tag, word), ner))
    return proper_iob_tokens


class NamedEntityChunker(ChunkParserI):
    def __init__(self, train_sents, **kwargs):
        assert isinstance(train_sents, Iterable)

        self.feature_detector = features
        self.tagger = ClassifierBasedTagger(train=train_sents, feature_detector=features, **kwargs)

    def parse(self, tagged_sent):
        chunks = self.tagger.tag(tagged_sent)

        # Transform the result from [((w1, t1), iob1), ...]
        # to the preferred list of triplets format [(w1, t1, iob1), ...]
        iob_triplets = [(w, t, c) for ((w, t), c) in chunks]

        # Transform the list of triplets to nltk.Tree format
        return conlltags2tree(iob_triplets)


my_file  =Path("./tagging/ingredient.pickle")
if not my_file.exists():
    data = pd.read_csv(
        'https://raw.githubusercontent.com/nytimes/ingredient-phrase-tagger/master/nyt-ingredients-snapshot-2015.csv')
    data = data[['input', 'name', 'qty', 'unit']]
    data = data.loc[data.input.notna()]
    data.reset_index(inplace=True, drop=True)

    data['input'] = data.input.str.lower()
    data['name'] = data.name.str.lower()
    data['unit'] = data.unit.str.lower()

    data['input'] = data.input.apply(lambda x: re.sub(r'[,.!?()-+|]+', ' ', x))
    data['input'] = data.input.apply(lambda x: re.sub(r' +', ' ', x))
    data['input'] = data.input.apply(lambda x: convert_decimal(x))

    data['pos_tagger'] = data.input.apply(lambda x: pos_category(x))

    data['tagger'] = data.apply(tagging, axis=1)
    data['tagger'] = data.tagger.apply(lambda x: to_conll_iob(x))


    training_samples = list(data.tagger)
    chunker = NamedEntityChunker(training_samples)


    f = open('./tagging/ingredient.pickle', 'wb')
    pickle.dump(chunker.tagger, f)
    f.close()





class IngredientPredict:

    def __init__(self):
        self.dict_ = {'qty': [], 'unit': [], 'name': [], "comment": []}

        f = open('./tagging/ingredient.pickle', 'rb')
        self.classifier = pickle.load(f)
        f.close()

    def convert_decimal(self, text):
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

    def predict_new(self, text):
        text = text.lower()
        text = re.sub(r'[,.!?()-+|]+', ' ', text)
        text = re.sub(r' +', ' ', text)
        text = convert_decimal(text)

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

        if len(dict["comment"]) > 0:
           comment = " ".join(dict["comment"])
        else:
           comment = None

        if len(dict["qty"]) > 0:
           taggings["qty"] = float(Fraction(dict["qty"][0]))
        else:
           taggings["qty"] = 1

        if len(dict["unit"]) > 0:
           taggings["unit"] = str(dict["unit"][0])
        else:
           taggings["unit"] = None

        taggings["name"] = name
        taggings["comment"] = comment
        return taggings