import json

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


class RecipeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Ingredient):
            return {'name': o.name,
                    'quantity': o.quantity,
                    'measurement': o.measurement,
                    'descriptor': o.descriptor,
                    'preparation': o.preparation}
        return o.__dict__