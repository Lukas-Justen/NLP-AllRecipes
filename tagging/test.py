from datastructure.resources import variables, database
from scraper.recipescraper import RecipeScraper


def scrape_category(category_url):
    recipes = []
    url = "https://www.allrecipes.com/recipe/220643"
    scraper = RecipeScraper(url, "")
    recipe1 = scraper.get_recipe()

    url = "https://www.allrecipes.com/recipe/222343"
    scraper = RecipeScraper(url, "")
    recipe2 = scraper.get_recipe()

    recipes.append(recipe1)
    recipes.append(recipe2)
    return recipes


def get_ingredient_type(ingredient, variables):
    for key in variables:
        if ingredient in variables[key]:
            return key
    return "others"


def count_ingredients(recipes):
    counter = {"meats": {}, "seafood": {}, "poultry": {}, "shellfish": {}, "vegetarian": {}, "legumes": {},
               "fruits": {}, "cheeses": {}, "grains": {}, "noodles": {}, "nuts": {}, "vegetables": {}, "spices": {},
               "others": {}}

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

recipes = database.find_recipes("Vegetarian")
# recipes = scrape_category("some_url")
counter = count_ingredients(recipes)
counter
