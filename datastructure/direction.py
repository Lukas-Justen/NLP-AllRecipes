import re

import nltk

from datastructure.resources import actions, tools


class DirectionBuilder(object):

    def __init__(self, recipe_ingredients, stopwords):
        self.time = None
        self.temperature = None
        self.tools = []
        self.ingredients = []
        self.actions = []
        self.recipe_ingredients = [r.name for r in recipe_ingredients]
        self.wordnet_lemmatizer = nltk.stem.WordNetLemmatizer()
        self.stemming = nltk.porter.PorterStemmer()
        self.stopwords = stopwords
        self.phrase = ""

    @staticmethod
    def convert_to_directions(direction_texts, ingredients):
        directions = []
        stopwords = nltk.corpus.stopwords.words('english')
        for phrase in direction_texts:
            for sentence in phrase.split(". "):
                builder = DirectionBuilder(ingredients, stopwords)
                builder.convert(sentence)
                directions.append(builder.create_direction())
        return directions

    def create_direction(self):
        return Direction(self.time, self.temperature, self.tools, self.ingredients, self.actions,self.phrase)

    def convert(self, sentence):
        sentence = sentence.lower()
        time_match = re.findall(r'(?:\d+ to \d+|\d[\d\s/., ]*) (?:minutes|hours|minute|hour|seconds|second)', sentence)
        temp_match = re.findall(r'\d+ degrees f \(\d+ degrees c\)', sentence)
        self.phrase = sentence
        self.time = str(time_match[0] if time_match else "").lower()
        self.temperature = str(temp_match[0] if temp_match else "").lower()
        self.actions = self.parse_actions(sentence)
        self.tools = self.parse_tools(sentence)
        self.ingredients = self.parse_ingredients(sentence, self.recipe_ingredients)

    def parse_actions(self, sentence):
        found = set()
        sentence = sentence.lower()
        words = [w for w in sentence.split() if w not in self.stopwords and len(w) > 1]
        for word in words:
            for action in actions:
                if str(word).startswith(action):
                    found.add(action)
                    break
        return list(found)

    def parse_tools(self, sentence):
        found = set()
        sentence = sentence.lower()
        words = [w for w in sentence.split() if w not in self.stopwords and len(w) > 1]
        for word in words:
            for tool in tools:
                if str(tool).startswith(word) and abs(len(tool) - len(word)) <= 4:
                    found.add(tool)
                    break
        return list(found)

    def parse_ingredients(self, sentence, ingredient_names):
        new_sentence = sentence
        second_match = []
        found = set()
        for name in ingredient_names:
            if name in sentence:
                found.add(name)

        sentence = re.sub(r'[^\w\d\s]+', ' ', sentence)
        words = sentence.split()
        words = [w for w in words if w not in self.stopwords]

        found_names = []
        for f in found:
            found_names.extend(f.split())

        words = [w for w in words if w not in found_names]
        for word in words:
            for name in ingredient_names:
                if len(word) > 3 and word in name:
                    if word in second_match:
                        new_sentence = new_sentence.replace(word, "")
                    else:
                        second_match.append(word)
                        new_sentence = new_sentence.replace(word, name)
                    found.add(name)

        new_sentence = new_sentence.replace("  ", " ")
        self.phrase = new_sentence
        return list(found)


class Direction(object):

    def __init__(self, time, temperature, tools, ingredients, actions,phrase):
        self.time = time
        self.temperature = temperature
        self.tools = tools
        self.ingredients = ingredients
        self.actions = actions
        self.phrase = phrase

    def __repr__(self):
        representation =  (str(self.time) + ", " if self.time else "") + \
               (str(self.temperature) + ", " if self.temperature else "") + \
               (str(self.tools) + ", " if self.tools else "") + \
               (str(self.actions) + ", " if self.actions else "") + \
               (str(self.ingredients) + ", " if self.ingredients else "") + \
               self.phrase
        return representation if representation != "" else self.phrase

    def __str__(self):
        return "Time       : " + str(self.time)+ "\n"\
               "Temperature: " + str(self.temperature) + "\n" \
               "Tools      : " + str(self.tools) + "\n"\
               "Actions    : " + str(self.actions) + "\n"\
               "Ingredients: " + str(self.ingredients) + "\n"\
               "Phrase     : " + str(self.phrase) + "\n"
