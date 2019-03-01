import re

import requests
from bs4 import BeautifulSoup

from database import Database
from direction import DirectionBuilder
from ingredient import IngredientBuilder
from recipe import RecipeBuilder
# from seleniumscraper import SeleniumScraper


class Scraper(object):

    def __init__(self, url, parser="html.parser"):
        r = requests.get(url)
        html = r.text
        self.soup = BeautifulSoup(html, features=parser)
        self.sub_spaces = re.compile(r'\s+')
        self.recipe = None
        self.database = Database()

    def get_recipe(self):
        if not self.recipe:
            builder = RecipeBuilder()
            builder.name = self.get_recipe_name()
            builder.ingredients = self.get_ingredients()
            builder.prep_time = self.get_time("prepTime")
            builder.cook_time = self.get_time("cookTime")
            builder.total_time = self.get_time("totalTime")
            builder.servings_count = self.get_servings_count()
            builder.directions = self.get_directions()
            builder.breadcrumbs = self.get_site_breadcrumbs()
            self.recipe = builder.create_recipe()
        return self.recipe

    def get_ingredients(self):
        ingredient_spans = self.soup.find_all("span", itemprop="recipeIngredient")
        ingredient_texts = [span.text for span in ingredient_spans]
        ingredients = IngredientBuilder.convert_to_ingredients(ingredient_texts)
        return ingredients

    def get_time(self, type):
        time = 0.0
        try:
            scalar_values = [1440.0, 60.0, 1.0]
            prep_time_div = self.soup.find("time", itemprop=type)
            prep_time_span = prep_time_div.find_all("span", class_="prepTime__item--time")
            prep_time_values = [float(span.text) for span in prep_time_span]
            scalar_values = scalar_values[-len(prep_time_span):]
            time = sum([x * y for x, y in zip(scalar_values, prep_time_values)])
        except:
            print("Error: Could not read " + type + " from recipe.")
        return time

    def get_servings_count(self):
        servings_meta = self.soup.find("meta", id="metaRecipeServings")
        servings_count = float(servings_meta["content"])
        return servings_count

    def get_directions(self):
        direction_spans = self.soup.find_all("span", class_="recipe-directions__list--item")
        direction_texts = [span.text for span in direction_spans]
        direction_texts = [d.strip() for d in direction_texts if d != '']
        directions = DirectionBuilder.convert_to_directions(direction_texts,self.database)
        return directions

    def get_recipe_name(self):
        content_span = self.soup.find(id="recipe-main-content")
        recipe_name = content_span.text
        return recipe_name

    def get_site_breadcrumbs(self):
        breadcrumb_spans = self.soup.find_all("span", class_="toggle-similar__title")
        breadcrumbs = [self.sub_spaces.sub(' ', span.text).strip() for span in breadcrumb_spans]

        return breadcrumbs

    










