import json

import pymongo
from bson import json_util

from recipe import RecipeEncoder


class Database(object):

    def __init__(self):
        connection = "mongodb+srv://AllRecipes:J4XAMWFIqPX3zi4l@cluster0-cpmav.mongodb.net/test?retryWrites=true"
        client = pymongo.MongoClient(connection)
        self.all_recipes_db = client["AllRecipes"]
        self.recipes = self.all_recipes_db.recipes

    def insert_recipe(self, recipe):
        recipe_json = json.dumps(recipe, cls=RecipeEncoder)
        data = json_util.loads(recipe_json)
        self.recipes.insert_one(data)

    def find_recipe(self):
        recipe = self.recipes.find_one()
        return recipe

    def find_actions(self):
        # TODO : Return a string list of actions
        pass

    def find_tools(self):
        # TODO : Return a string list of tools
        pass
