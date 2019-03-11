from datastructure.resources import variables, database
from scraper.recipescraper import RecipeScraper
from scraper.seleniumscraper import SeleniumScraper

from tagging.ingredient_train import *


def scrape_category(category_url, category_name):
    scraper = SeleniumScraper(category_url)
    scraper.scrape_urls()
    urls = scraper.get_urls_to_be_scraped()

    for u in urls:
        # try:
        scraper = RecipeScraper(u, category_name)
        recipe = scraper.get_recipe()
        if not "Desserts" in recipe.breadcrumbs:
            database.insert_recipe(recipe)
        print("Scraped :   " + u)
        # except Exception as e:
        #     # print(e)
        #     print("Unable  :   " + u)


def get_ingredient_type(ingredient, variables):
    for key in variables:
        if ingredient in variables[key]:
            return key
    return "others"


def count_ingredients(recipes):
    counter = {"meats": {}, "seafood": {}, "poultry": {}, "shellfish": {}, "vegetarian": {}, "legumes": {},
               "fruits": {}, "cheeses": {}, "grains": {}, "noodles": {}, "nuts": {}, "vegetables": {}, "spices": {},
               "liquids": {}, "others": {}}

    for recipe in recipes:
        for ingredient in recipe["ingredients"]:
            ingredient_name = str(ingredient["name"]).lower()
            type = get_ingredient_type(ingredient_name, variables)
            if ingredient_name in counter[type]:
                counter[type][ingredient_name] += 1
            else:
                counter[type][ingredient_name] = 1

    for key in counter:
        counter[key] = {k: counter[key][k] for k in sorted(counter[key], key=counter[key].get, reverse=True)}
    return counter

category = "Chinese"
# url = "https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/"
# scrape_category(url, category)
recipes = database.find_recipes(category)
counter = count_ingredients(recipes)