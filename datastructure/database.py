import json

import pymongo
from bson import json_util

from datastructure.recipe import RecipeEncoder


class Database(object):

    def __init__(self):
        connection = "mongodb+srv://AllRecipes:J4XAMWFIqPX3zi4l@cluster0-cpmav.mongodb.net/test?retryWrites=true"
        client = pymongo.MongoClient(connection)
        self.all_recipes_db = client["AllRecipes"]
        self.recipes = self.all_recipes_db.recipes
        self.tools = self.all_recipes_db.tools
        self.actions = self.all_recipes_db.actions
        self.ingredient_types = {
            "meats" : self.all_recipes_db.meats,
            "seafood": self.all_recipes_db.seafood,
            "poultry": self.all_recipes_db.poultry,
            "shellfish": self.all_recipes_db.shellfish,
            "vegetarian": self.all_recipes_db.vegetarian
        }

    def insert_recipe(self, recipe):
        recipe_json = json.dumps(recipe, cls=RecipeEncoder)
        data = json_util.loads(recipe_json)
        self.recipes.insert_one(data)

    def find_recipe(self):
        recipe = self.recipes.find_one()
        return recipe

    def find_actions(self):
        actions_list = self.actions.find()
        actions_dict = [dict for dict in actions_list]
        actions = []
        for dicts in actions_dict:
            actions.append(dicts['\ufeffActions'])
        return actions

    def find_tools(self):
        tools_list = self.tools.find()
        tools_dict = [dict for dict in tools_list]
        tools = []
        for dicts in tools_dict:
            tools.append(dicts['\ufeffTools'])
        return tools

    def find_ingredient_types(self, types):
        dict_list = []
        for type in types:
            dict_list.extend([item for item in self.ingredient_types[type].find()])
        items = []
        for dict in dict_list:
            items.append(dict['name'])
        return items
