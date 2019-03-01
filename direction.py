import re

import nltk


class DirectionBuilder(object):

    def __init__(self, tools, actions, recipe_ingredients):
        self.time = None
        self.temperature = None
        self.tools = []
        self.ingredients = []
        self.actions = []
        self.tools = tools
        self.actions = actions
        self.recipe_ingredients = recipe_ingredients
        self.wordnet_lemmatizer = nltk.stem.WordNetLemmatizer()

    @staticmethod
    def convert_to_directions(direction_texts, tools, actions, ingredients):
        directions = []
        for phrase in direction_texts:
            for sentence in phrase.split(". "):
                builder = DirectionBuilder(tools, actions, ingredients)
                builder.convert(sentence)
                directions.append(builder.create_direction())
        return directions

    def create_direction(self):
        return Direction(self.time, self.temperature, self.tools, self.ingredients, self.actions)

    def convert(self, sentence):
        self.time = re.findall(r'(\d+ to \d+|[\d\s/ ]+) (minutes|hours|minute|hour|seconds|second)', sentence)
        self.temperature = re.findall(r'\d+ degrees F \(\d+ degrees C\)', sentence)
        self.actions = self.parse_actions(sentence)
        self.tools = self.parse_tools(sentence)
        self.ingredients = self.parse_ingredients(sentence, self.recipe_ingredients)

    def parse_actions(self, sentence):
        actions = self.actions
        found = []
        for word in sentence.split():
            word = self.wordnet_lemmatizer.lemmatize(word)
            if word in actions:
                found.append(word)
        return found

    def parse_tools(self, sentence):
        tools = self.tools
        found = []
        for word in sentence.split():
            word = self.wordnet_lemmatizer.lemmatize(word)
            if word in tools:
                found.append(word)
        return found

    def parse_ingredients(self, sentence, recipe_ingredients):
        ingredient_names = [r.name for r in recipe_ingredients]
        found = []
        for name in ingredient_names:
            if name in sentence:
                found.append(name)
        return found


class Direction(object):

    def __init__(self, time, temperature, tools, ingredients, actions):
        self.time = time
        self.temperature = temperature
        self.tools = tools
        self.ingredients = ingredients
        self.actions = actions

    # def __repr__(self):
    #     representation =  (str(self.quantity) + ", " if self.quantity else "") + \
    #            (str(self.measurement) + ", " if self.measurement else "") + \
    #            (str(self.descriptor) + ", " if self.descriptor else "") + \
    #            (str(self.preparation) + ", " if self.preparation else "") + \
    #            self.name
    #     return representation if representation != "" else self.phrase
    #
    # def __str__(self):
    #     return "Ingredient Name: " + str(self.name)+ "\n"\
    #            "Quantity       : " + str(self.quantity) + "\n" \
    #            "Measurement    : " + str(self.measurement) + "\n"\
    #            "Descriptor     : " + str(self.descriptor) + "\n"\
    #            "Preparation    : " + str(self.preparation) + "\n"\
    #            "Phrase         : " + str(self.phrase) + "\n"
