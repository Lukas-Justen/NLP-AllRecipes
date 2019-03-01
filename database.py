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
        self.tools = self.all_recipes_db.tools
        self.actions = self.all_recipes_db.actions

    def insert_recipe(self, recipe):
        recipe_json = json.dumps(recipe, cls=RecipeEncoder)
        data = json_util.loads(recipe_json)
        self.recipes.insert_one(data)

    def find_recipe(self):
        recipe = self.recipes.find_one()
        return recipe

    def find_actions(self):
    	#return a list of actions

        actions_list = self.actions.find()
        actions_dict = [dict for dict in actions_list]

        #iterate through the actions dict to get the actions
        actions = []
        for dicts in actions_dict:
        	actions.append(dicts['\ufeffActions'])
        
        return actions
        

    def find_tools(self):
        #Return a string list of actions

        tools_list = self.tools.find()
        tools_dict = [dict for dict in tools_list]

        tools = []
        #iterate to get the tools
        for dicts in tools_dict:
        	tools.append(dicts['\ufeffTools'])
        
        return tools
