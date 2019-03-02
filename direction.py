import re

import nltk


class DirectionBuilder(object):

    def __init__(self, tools, actions, recipe_ingredients, stopwords):
        self.time = None
        self.temperature = None
        self.tools = []
        self.ingredients = []
        self.actions = []
        self.tools = tools
        self.actions = actions
        self.recipe_ingredients = recipe_ingredients
        self.wordnet_lemmatizer = nltk.stem.WordNetLemmatizer()
        self.stemming = nltk.porter.PorterStemmer()
        self.stopwords = stopwords
        self.phrase = ""

    @staticmethod
    def convert_to_directions(direction_texts, tools, actions, ingredients):
        directions = []
        stopwords = nltk.corpus.stopwords.words('english')
        for phrase in direction_texts:
            for sentence in phrase.split(". "):
                builder = DirectionBuilder(tools, actions, ingredients, stopwords)
                builder.convert(sentence)
                directions.append(builder.create_direction())
        return directions

    def create_direction(self):
        return Direction(self.time, self.temperature, self.tools, self.ingredients, self.actions,self.phrase)

    def convert(self, sentence):
        self.time = re.findall(r'(\d+ to \d+|[\d\s/ ]+) (minutes|hours|minute|hour|seconds|second)', sentence)
        self.temperature = re.findall(r'\d+ degrees F \(\d+ degrees C\)', sentence)
        self.actions = self.parse_actions(sentence)
        self.tools = self.parse_tools(sentence)
        self.ingredients = self.parse_ingredients(sentence, self.recipe_ingredients)
        self.phrase = sentence

    def parse_actions(self, sentence):
        actions = self.actions
        found = []
        for word in sentence.split():
            word = self.wordnet_lemmatizer.lemmatize(word)
            word = self.stemming.stem(word)
            if word in actions:
                found.append(word)
        return found

    def parse_tools(self, sentence):
        tools = self.tools
        found = []
        for word in sentence.split():
            word = self.wordnet_lemmatizer.lemmatize(word)
            word = self.stemming.stem(word)
            if word in tools:
                found.append(word)
        return found

    def parse_ingredients(self, sentence, recipe_ingredients):
        ingredient_names = [r.name for r in recipe_ingredients]

        for r in ingredient_names:
            ingredient_names.remove(r)
            ingredient_names.extend(r.split(' and '))

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
                if len(word) >= 3 and word in name:
                    found.add(name)

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
