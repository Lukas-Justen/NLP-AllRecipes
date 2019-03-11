import json
import random
import re

from tabulate import tabulate

from datastructure.ingredient import Ingredient, IngredientBuilder


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
        self.cooking_action = ""

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
                      self.sodium,
                      self.cooking_action)


class Recipe(object):

    def __init__(self, url,name, ingredients, prep_time, cook_time, total_time, servings_count, directions, breadcrumbs, calories, fat, carbohydrates, protein, cholesterol, sodium, cooking_action):
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
        self.cook_action = cooking_action

    def __str__(self):
        table_ingredients = []
        for ingredient in self.ingredients:
            table_ingredients.append([ingredient.quantity, ingredient.measurement, ingredient.descriptor, ingredient.name, ingredient.phrase])
        table_directions = []
        table_timetemp =[]
        table_phrases = []
        counter = 1
        for direction in self.directions:
            table_directions.append([counter, direction.tools,direction.actions, direction.ingredients])
            table_timetemp.append([counter,direction.time,direction.temperature])
            table_phrases.append([counter, direction.phrase])
            counter += 1
        return "Recipe Name: " + str(self.name)+ "\n" \
               "Main Action: " + str(self.cook_action) + "\n" \
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
               "\n\n" + tabulate(table_ingredients, headers=['Quantity', 'Measurement', "Descriptor", "Name", "Phrase"]) + "\n"\
               "\n\n" + tabulate(table_directions, headers=["Step", "Tools", "Actions", "Ingredients"]) + "\n"\
               "\n\n" + tabulate(table_timetemp, headers=["Step", "Time", "Temperature"]) + "\n"\
               "\n\n" + tabulate(table_phrases, headers=["Step", "Phrase"])

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
                    from_ingredients = [i for i in from_ingredients if i not in to_ingredients]
                    replacement_dict = {"from":from_ingredients, "to": to_ingredients}
                    template[mode].append(replacement_dict)
                elif mode == "ADD":
                    to_add = str(parts[0]).strip().split(", ")
                    where = str(parts[1]).strip().split(", ")
                    quantity = float(str(parts[2]).strip())
                    measurement = str(parts[3]).strip()
                    template["ADD"].append({"add": to_add, "where": where, "quantity": quantity,"measurement": measurement})
                else:
                    ingredient = str(parts[0]).strip().split(", ")
                    scale = float(str(parts[1]).strip())
                    template["SCALE"].append({"ingredient":ingredient, "scale":scale})
        replacements_made = self.replace(template["REPLACE"])
        additions_made = self.add(template["ADD"])
        scalings_made = self.scale(template["SCALE"])
        return (replacements_made, additions_made, scalings_made)

    def insert_variables(self, line, variables):
        matches = re.findall(r'%(?P<variable_name>\w+)%',line)
        for match in matches:
            line = line.replace("%" + match + "%", variables[match])
        return line

    def replace(self, list_of_replacements):
        replacements_made = []
        replaced = []
        for replacement in list_of_replacements:
            from_types = replacement["from"]
            to_types = replacement["to"]
            for type in from_types:
                for index, ingredient in enumerate(self.ingredients):
                    if index not in replaced and self.simple_match(type,ingredient.name):
                        replaced.append(index)
                        replace_with = random.choice(to_types)
                        if len(to_types) > 1:
                            to_types.remove(replace_with)

                        if ingredient.descriptor:
                           list_descriptor = ingredient.descriptor.split()
                           for word in list_descriptor:
                               ingredient.phrase = str(ingredient.phrase).replace(' '.join(word),'')

                        ingredient.phrase = str(ingredient.phrase).replace(ingredient.name, replace_with)

                        self.replace_direction(ingredient.name, replace_with)
                        replacements_made.append(ingredient.name + " > " + replace_with)
                        ingredient.name = replace_with
        return replacements_made


    def simple_match(self, ingredient_from_list,ingredient_in_recipe):
        return ingredient_from_list in ingredient_in_recipe

    def replace_direction(self, from_name, to_name):
        for direction in self.directions:
            if from_name in direction.ingredients:
                direction.ingredients = [w if w != from_name else to_name for w in direction.ingredients]
                direction.phrase = str(direction.phrase).replace(from_name, to_name)

    def add(self, list_of_additions):
        additions_made = []
        for addition in list_of_additions:
            added = False
            for direction in self.directions:
                possible_actions = addition["where"]
                for action in possible_actions:
                    if not added and action in direction.actions:
                        to_add = random.choice(addition["add"])
                        builder = IngredientBuilder()
                        builder.name = to_add
                        builder.quantity = addition["quantity"] * self.servings_count
                        builder.measurement = addition["measurement"]
                        builder.phrase = str(builder.quantity) + " " + str(builder.measurement) + " " + builder.name
                        self.ingredients.append(builder.create_ingredient())
                        if direction.ingredients:
                            direction.ingredients.append(to_add)
                            old_ingredient = direction.ingredients[0]
                            direction.phrase = str(direction.phrase).replace(old_ingredient, old_ingredient + ", " + to_add)
                        additions_made.append(str(builder.quantity) + "  " + str(builder.measurement) +"  " +to_add)
                        added = True
        return additions_made

    def scale(self, list_of_scalings):
        scalings_made = []
        for ingredient in self.ingredients:
            scaled = False
            for scaling in list_of_scalings:
                for match in scaling["ingredient"]:
                    if not scaled and self.simple_match(match, ingredient.name):
                        try:
                            ingredient.quantity *= scaling["scale"]
                            scalings_made.append(str(ingredient.name) + " by factor " + str(scaling["scale"]))
                            scaled = True
                        except:
                            print("Couldn't scale "  + ingredient.name)
        return scalings_made




class RecipeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Ingredient):
            return {'name': o.name,
                    'quantity': o.quantity,
                    'measurement': o.measurement,
                    'descriptor': o.descriptor,
                    'preparation': o.preparation}
        return o.__dict__