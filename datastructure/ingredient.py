import re
from copy import deepcopy

from tagging.utils import tag_ingredient_parts


class IngredientBuilder(object):

    def __init__(self):
        self.name = ""
        self.quantity = 0.0
        self.measurement = None
        self.descriptor = None
        self.preparation = None
        self.phrase = ""

    @staticmethod
    def convert_to_ingredients(ingredient_texts):
        ingredients = []
        for phrase in ingredient_texts:
            builder = IngredientBuilder()
            builder.convert(phrase)
            ingredient = builder.create_ingredient()
            splitted_ingredient_names = str(ingredient.name).split(" and ")
            for split in splitted_ingredient_names:
                new_ingredient = deepcopy(ingredient)
                new_ingredient.name = split
                ingredients.append(new_ingredient)
        return ingredients

    def create_ingredient(self):
        return Ingredient(self.name, self.quantity, self.measurement, self.descriptor, self.preparation, self.phrase)

    def convert(self, phrase):
        phrase = re.sub(r'\(.*\)', " ", phrase)
        taggings = tag_ingredient_parts(phrase)
        self.quantity = str(taggings["qty"] if "qty" in taggings else self.quantity).lower()
        self.measurement = str(self.strip_value(taggings["unit"] if "unit" in taggings else self.quantity)).lower()
        self.name = str(taggings["name"] if "name" in taggings else self.quantity).lower()
        self.preparation = str(self.strip_value(taggings["comment"] if "comment" in taggings else self.preparation)).lower()
        self.phrase = str(phrase).lower()

    def strip_value(self, value):
        if value != None:
            value = re.sub(r'[.,\s\d]+', " ", str(value))
            value = str(value).strip()
            value = value if value != "" else None
        return value


class Ingredient(object):

    def __init__(self, name, quantity, measurement, descriptor, preparation, phrase):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.descriptor = descriptor
        self.preparation = preparation
        self.phrase = phrase

    def __repr__(self):
        representation =  (str(self.quantity) + ", " if self.quantity else "") + \
               (str(self.measurement) + ", " if self.measurement else "") + \
               (str(self.descriptor) + ", " if self.descriptor else "") + \
               (str(self.preparation) + ", " if self.preparation else "") + \
               self.name
        return representation if representation != "" else self.phrase

    def __str__(self):
        return "Ingredient Name: " + str(self.name)+ "\n"\
               "Quantity       : " + str(self.quantity) + "\n" \
               "Measurement    : " + str(self.measurement) + "\n"\
               "Descriptor     : " + str(self.descriptor) + "\n"\
               "Preparation    : " + str(self.preparation) + "\n"\
               "Phrase         : " + str(self.phrase) + "\n"\

