import requests
from bs4 import BeautifulSoup

from ingredient import Ingredient
from recipe import RecipeBuilder


class Scraper(object):

    def __init__(self, url, parser="html.parser"):
        r = requests.get(url)
        html = r.text
        self.soup = BeautifulSoup(html, features=parser)
        self.recipe = None

    def get_recipe(self):
        if not self.recipe:
            builder = RecipeBuilder()
            builder.ingredients = self.get_ingredients()
            builder.prep_time = self.get_time("prepTime")
            builder.cook_time = self.get_time("cookTime")
            builder.total_time = self.get_time("totalTime")
            builder.servings_count = self.get_servings_count()
            builder.recipe_name = self.get_recipe_name()
            builder.instructions =self.get_directions()
            self.recipe = builder.create_recipe()

        return self.recipe

    def get_ingredients(self):
        ingredient_spans = self.soup.find_all("span", itemprop="recipeIngredient")
        ingredient_texts = [span.text for span in ingredient_spans]
        ingredients = Ingredient.convert_to_ingredients(ingredient_texts)
        return ingredients

    def get_time(self, type):
        scalar_values = [1440.0, 60.0, 1.0]
        prep_time_div = self.soup.find("time", itemprop=type)
        prep_time_span = prep_time_div.find_all("span", class_="prepTime__item--time")
        prep_time_values = [float(span.text) for span in prep_time_span]
        scalar_values = scalar_values[-len(prep_time_span):]
        time = sum([x * y for x, y in zip(scalar_values, prep_time_values)])
        return time

    def get_servings_count(self):
        servings_meta = self.soup.find("meta",id="metaRecipeServings")
        servings_count = float(servings_meta["content"])
        return servings_count

    #This method gets all the directions for the recipes
    def get_directions(self):
        #check for span recipe-directions__list--item to get the direction items
        direction_spans = self.soup.find_all("span", class_="recipe-directions__list--item")
        direction_texts = [span.text for span in direction_spans]
        
        return direction_texts

    #This method fetches the name of the recipe
    def get_recipe_name(self):
        #get all the text associated with the main content and extract the inner html
        main_ingrediants = self.soup.find(id="recipe-main-content").text


        return main_ingrediants

        

