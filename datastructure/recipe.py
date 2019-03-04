import json
import random
import re

from datastructure.ingredient import Ingredient


class RecipeBuilder(object):

    def __init__(self):
        self.url = ""
        self.name = ""
        self.ingredients = []
        self.prep_time = 0.0
        self.cook_time = 0.0
        self.total_time = 0.0
        self.servings_count = 1.0
        self.directions = []
        self.breadcrumbs = []
        self.calories = 0.0
        self.fat = 0.0
        self.carbohydrates = 0.0
        self.protein = 0.0
        self.cholesterol = 0.0
        self.sodium = 0.0

    def create_recipe(self):
        return Recipe(self.url,
                      self.name,
                      self.ingredients,
                      self.prep_time,
                      self.cook_time,
                      self.total_time,
                      self.servings_count,
                      self.directions,
                      self.breadcrumbs,
                      self.calories,
                      self.fat,
                      self.carbohydrates,
                      self.protein,
                      self.cholesterol,
                      self.sodium)


class Recipe(object):

    def __init__(self, url,name, ingredients, prep_time, cook_time, total_time, servings_count, directions, breadcrumbs, calories, fat, carbohydrates, protein, cholesterol, sodium):
        self.url = url
        self.name = name
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.total_time = total_time
        self.servings_count = servings_count
        self.directions = directions
        self.breadcrumbs = breadcrumbs
        self.calories = calories
        self.fat = fat
        self.carbohydrates = carbohydrates
        self.protein = protein
        self.cholesterol = cholesterol
        self.sodium = sodium
        self.variable_finder = re.compile(r'%(?P<variable_name>.+)%')

    def __str__(self):
        ingredient_string = ""
        for ingredient in self.ingredients:
            ingredient_string += ingredient.__repr__() + "\n"
        direction_string = ""
        counter = 1
        for direction in self.directions:
            direction_string += str(counter) + ".  " + direction.__repr__() + "\n"
            counter += 1
        return "Recipe Name: " + str(self.name)+ "\n" \
               "Url        : " + str(self.url) + "\n\n" \
               "Breadcrumbs: " + str(self.breadcrumbs) + "\n\n" \
               "Prep-Time  : " + str(self.prep_time) + "\n" \
               "Cook-Time  : " + str(self.cook_time) + "\n"\
               "Total-Time : " + str(self.total_time) + "\n\n"\
               "Servings   : " + str(self.servings_count)+ "\n\n"\
               "Calories   : " + str(self.calories)+ "\n"\
               "Fat        : " + str(self.fat)+ "\n"\
               "Carbs      : " + str(self.carbohydrates)+ "\n"\
               "Protein    : " + str(self.protein)+ "\n"\
               "Cholesterol: " + str(self.cholesterol)+ "\n"\
               "Sodium     : " + str(self.sodium)+ "\n\n"\
               "Ingredients: \n" + ingredient_string + "\n"\
               "Directions : \n" + direction_string

    def convert(self, template_file, variables):
        template = {"REPLACE":[], "ADD": [], "SCALE": []}
        mode = ""
        with open(template_file) as fp:
            lines = fp.readlines()
        for line in lines:
            line = line.replace("\n", "")
            if line.startswith("*"):
                mode = line.replace("*", "")
            else:
                line = self.insert_variables(line,variables)
                parts = line.split(" > ")
                if mode == "REPLACE":
                    from_ingredients = str(parts[0]).strip().split(", ")
                    to_ingredients = str(parts[1]).strip().split(", ")
                    replacement_dict = {"from":from_ingredients, "to": to_ingredients}
                    template[mode].append(replacement_dict)
                elif mode == "ADD":
                    to_add = str(parts[0]).strip().split(", ")
                    number = int(str(parts[1]).strip())
                    where = str(parts[2]).strip()
                    template["ADD"].append({"add": to_add, "number": number, "where": where})
                else:
                    ingredient = str(parts[0]).strip()
                    scale = float(str(parts[1]).strip())
                    template["SCALE"].append({"ingredient":ingredient, "scale":scale})
        self.replace(template["REPLACE"])
        self.add(template["ADD"])
        self.scale(template["SCALE"])

    def insert_variables(self, line, variables):
        matches = self.variable_finder.findall(line)
        for match in matches:
            variable_name = str(match.group("variable_name"))
            line = line.replace("%" + variable_name + "%", variables[variable_name])
        return line

    def replace(self, list_of_replacements):
        for replacement in list_of_replacements:
            from_types = replacement["from"]
            to_types = replacement["to"]
            for type in from_types:
                for ingredient in self.ingredients:
                    if self.simple_match(type,ingredient.name):
                        replace_with = random.choice(to_types)
                        to_types.remove(replace_with)
                        ingredient.phrase = str(ingredient.phrase).replace(ingredient.name, replace_with)
                        self.replace_direction(ingredient.name, replace_with)
                        ingredient.name = replace_with

    def simple_match(self, ingredient_from_list,ingredient_in_recipe):
        return ingredient_from_list in ingredient_in_recipe

    def replace_direction(self, from_name, to_name):
        for direction in self.directions:
            if from_name in direction.ingredients:
                direction.ingredients = [w if w != from_name else to_name for w in direction.ingredients]
                direction.phrase = str(direction.phrase).replace(from_name, to_name)

    def add(self, list_of_additions):
        pass

    def scale(self, list_of_scalings):
        pass




class RecipeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Ingredient):
            return {'name': o.name,
                    'quantity': o.quantity,
                    'measurement': o.measurement,
                    'descriptor': o.descriptor,
                    'preparation': o.preparation}
        return o.__dict__