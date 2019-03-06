from datastructure.resources import variables
from scraper.recipescraper import RecipeScraper

url = "https://www.allrecipes.com/recipe/141395"
scraper = RecipeScraper(url, "")
recipe = scraper.get_recipe()
recipe.convert('converts/ToVeg.txt', variables=variables)

print(recipe)
