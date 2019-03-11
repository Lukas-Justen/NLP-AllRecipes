import re

import requests
from bs4 import BeautifulSoup

from datastructure.direction import DirectionBuilder
from datastructure.ingredient import IngredientBuilder
from datastructure.recipe import RecipeBuilder


class RecipeScraper(object):

    def __init__(self, url, category, parser="html.parser"):
        r = requests.get(url)
        html = r.text
        self.url = url
        self.category = category
        self.soup = BeautifulSoup(html, features=parser)
        self.sub_spaces = re.compile(r'\s+')
        self.recipe = None

    def get_recipe(self):
        if not self.recipe:
            builder = RecipeBuilder()
            builder.url = self.url
            builder.name = self.get_recipe_name()
            builder.ingredients = self.get_ingredients()
            builder.prep_time = self.get_time("prepTime")
            builder.cook_time = self.get_time("cookTime")
            builder.total_time = self.get_time("totalTime")
            builder.servings_count = self.get_servings_count()
            builder.directions = self.get_directions(builder.ingredients)
            builder.breadcrumbs = self.get_site_breadcrumbs()
            builder.calories = self.get_nutrition("calories", "cal")
            builder.fat = self.get_nutrition("fatContent", "g")
            builder.carbohydrates = self.get_nutrition("carbohydrateContent", "g")
            builder.protein = self.get_nutrition("proteinContent", "g")
            builder.cholesterol = self.get_nutrition("cholesterolContent", "mg")
            builder.sodium = self.get_nutrition("sodiumContent", "mg")
            builder.cooking_action = self.find_main_action(builder.directions)
            self.recipe = builder.create_recipe()
        return self.recipe

    def get_ingredients(self):
        ingredient_spans = self.soup.find_all("span", itemprop="recipeIngredient")
        ingredient_texts = [span.text for span in ingredient_spans if span.text[-1] != ":"]
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

    def get_directions(self, ingredients):
        direction_spans = self.soup.find_all("span", class_="recipe-directions__list--item")
        direction_texts = [span.text for span in direction_spans]
        direction_texts = [d.strip() for d in direction_texts if d != '']
        directions = DirectionBuilder.convert_to_directions(direction_texts, ingredients)
        return directions

    def get_recipe_name(self):
        content_span = self.soup.find(id="recipe-main-content")
        recipe_name = content_span.text
        return recipe_name

    def get_site_breadcrumbs(self):
        breadcrumb_spans = self.soup.find_all("span", class_="toggle-similar__title")
        breadcrumbs = set([self.sub_spaces.sub(' ', span.text).strip() for span in breadcrumb_spans])
        breadcrumbs.add(self.category)
        return list(breadcrumbs)

    def get_nutrition(self, name, unit):
        value = 0.0
        try:
            html_span = self.soup.find("span", itemprop=name)
            match = re.findall(r'[\d.,]+', html_span.text)
            if match:
                value = float(match[0])
        except:
            print("Error: Could not read " + name + " from recipe.")
        return {"value": value, "unit": unit}

    def find_main_action(self, directions):
        longest_action = ""
        try:
            main_actions = ["broil", "boil", "bake", "grill", "stir", "simmer", "stew", "fry", "roast", "steam"]
            longest_time = 0.0
            time_directions = [d for d in directions if d.time]
            for d in time_directions:
                current_time = float(str(re.match(r'\d+', d.time).group(0)))
                if current_time > longest_time:
                    for a in d.actions:
                        for m in main_actions:
                            if a == m:
                                longest_time = current_time
                                longest_action = a

            if longest_action == "":
                for d in directions:
                    for a in d.actions:
                        for m in main_actions:
                            if a == m:
                                longest_action = a

            if longest_action == "":
                longest_action = "heat"

        except:
            print("Couldn't read main cooking action")

        return longest_action

