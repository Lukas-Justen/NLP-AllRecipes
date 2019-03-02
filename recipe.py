import json

from ingredient import Ingredient


class RecipeBuilder(object):

    def __init__(self):
        self.name = ""
        self.ingredients = []
        self.prep_time = 0.0
        self.cook_time = 0.0
        self.total_time = 0.0
        self.servings_count = 1.0
        self.directions = []
        self.breadcrumbs = []

    def create_recipe(self):
        return Recipe(self.name,
                      self.ingredients,
                      self.prep_time,
                      self.cook_time,
                      self.total_time,
                      self.servings_count,
                      self.directions,
                      self.breadcrumbs)


class Recipe(object):

    def __init__(self, name, ingredients, prep_time, cook_time, total_time, servings_count, directions, breadcrumbs):
        self.name = name
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.total_time = total_time
        self.servings_count = servings_count
        self.directions = directions
        self.breadcrumbs = breadcrumbs

    def __str__(self):
        ingredient_string = ""
        for ingredient in self.ingredients:
            ingredient_string += ingredient.__repr__() + "\n"
        direction_string = ""
        counter = 1
        for direction in self.directions:
            direction_string += str(counter) + ".  " + direction.__repr__() + "\n"
            counter += 1
        return "Recipe Name: " + str(self.name)+ "\n\n"\
               "Breadcrumbs: " + str(self.breadcrumbs) + "\n" \
               "Prep-Time  : " + str(self.prep_time) + "\n" \
               "Cook-Time  : " + str(self.cook_time) + "\n"\
               "Total-Time : " + str(self.total_time) + "\n\n"\
               "Servings   : " + str(self.servings_count)+ "\n\n"\
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