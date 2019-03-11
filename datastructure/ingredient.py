import re
from copy import deepcopy
from fractions import Fraction

import pymongo

from tagging.ingredient_train import IngredientPredict
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
        phrase = phrase.lower()
        taggings = IngredientPredict().get_taggings(phrase)
        # custom_taggings = tagger.tag_phrase(phrase)
        # descriptor_taggings = tag_ingredient_parts(phrase)
        self.quantity = taggings["qty"] if "qty" in taggings else self.quantity
        self.measurement = self.strip_value(taggings["unit"] if "unit" in taggings else self.quantity)
        self.name = taggings["name"] if "name" in taggings else self.quantity
        self.descriptor = self.strip_value(taggings["comment"] if "comment" in taggings else self.preparation)
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
        representation =  str(self.phrase) + "\t\t\t" + \
               ("Q: " + str(self.quantity) + ", " if self.quantity else "") + \
               ("M: " + str(self.measurement) + ", " if self.measurement else "") + \
               ("D: " + str(self.descriptor) + ", " if self.descriptor else "") + \
               ("P: " + str(self.preparation) + ", " if self.preparation else "") + \
               "Name: " + self.name
        return representation if representation != "" else self.phrase

    def __str__(self):
        return "Ingredient Name: " + str(self.name)+ "\n"\
               "Quantity       : " + str(self.quantity) + "\n" \
               "Measurement    : " + str(self.measurement) + "\n"\
               "Descriptor     : " + str(self.descriptor) + "\n"\
               "Preparation    : " + str(self.preparation) + "\n"\
               "Phrase         : " + str(self.phrase) + "\n"\

class IngredientParser:

    def __init__(self):
        self.qty_finder = re.compile(r'(?P<quantity>^[^a-zA-Z(]+)')
        connection = "mongodb+srv://AllRecipes:J4XAMWFIqPX3zi4l@cluster0-cpmav.mongodb.net/test?retryWrites=true"
        client = pymongo.MongoClient(connection)
        all_recipes_db = client["AllRecipes"]
        self.units = all_recipes_db.units
        self.ingredients = all_recipes_db.ingredients
        self.comments = all_recipes_db.comments
        self.comments_list = self.find_comments()
        self.units_list = self.find_units()
        self.ingredients_list = self.find_ingredients()

    def tag_phrase(self, phrase):
        taggings = {}
        phrase, qty = self.get_quantity(phrase)
        phrase, unit = self.get_unit(phrase)
        phrase, name = self.get_ingredient(phrase)
        phrase, comments = self.get_comments(phrase)

        name_parts = name.split()
        comments = [c for c in comments if not c in name_parts and c not in name]
        new_comments = []
        for comment1 in comments:
            good = True
            for comment2 in comments:
                if comment1 != comment2 and comment1 in comment2:
                    good = False
                    break
            if good:
                new_comments.append(comment1)
        comment = ", ".join(new_comments)

        taggings["qty"] = qty
        taggings["unit"] = unit
        taggings["comment"] = comment
        taggings["name"] = name
        return taggings

    def get_quantity(self, phrase):
        qty = 1.0
        match = self.qty_finder.match(phrase)
        if match:
            str_qty = match.group("quantity")
            phrase = phrase.replace(str_qty, "")
            phrase = phrase.strip()
            str_qty = str_qty.strip()
            str_qty = str_qty.replace(",", ".")
            qty = 0
            if " " in str_qty:
                try:
                    splits = str_qty.split()
                    qty = float(Fraction(splits[0]))
                    str_qty = splits[1]
                except Exception as e:
                    print("Unable to convert fraction!")
            try:
                qty += float(Fraction(str_qty))
            except Exception as e:
                print("Unable to convert fraction!")

            if qty == 0:
                qty = 1.0

        return phrase, qty

    def get_unit(self, phrase):
        for unit in self.units_list:
            if unit in phrase:
                phrase = phrase.replace(unit, "")
                phrase = phrase.strip()
                return phrase, unit
        return phrase, None

    def get_ingredient(self, phrase):
        for ingredient in self.ingredients_list:
            if ingredient in phrase:
                return phrase, str(ingredient).strip()
        return phrase, "Nothing found"

    def get_comments(self, phrase):
        comments = []
        for comment in self.comments_list:
            if comment in phrase:
                comments.append(comment)
        return phrase, comments

    def find_units(self):
        units_list = self.units.find()
        units_dict = [dict for dict in units_list]
        units = []
        for dicts in units_dict:
            if dicts["unit"]:
                units.append(dicts['unit'])
        # units.sort(key=len, reverse=True)
        return units

    def find_ingredients(self):
        ingredients_list = self.ingredients.find()
        ingredients_dict = [dict for dict in ingredients_list]
        ingredients = []
        for dicts in ingredients_dict:
            if dicts["name"]:
                ingredients.append(dicts['name'])
        ingredients.sort(key=len, reverse=True)
        return ingredients

    def find_comments(self):
        commets_list = self.comments.find()
        commets_dict = [dict for dict in commets_list]
        commets = []
        for dicts in commets_dict:
            if dicts["comment"]:
                commets.append(dicts['comment'])
        commets.sort(key=len, reverse=True)
        return commets


tagger = IngredientParser()