from scraper.recipescraper import RecipeScraper
from datastructure.resources import database
from scraper.seleniumscraper import SeleniumScraper

url = "https://www.allrecipes.com/recipe/220643/ginas-creamy-mushroom-lasagna/?internalSource=streams&referringId=16800&referringContentType=Recipe%20Hub&clickId=st_trending_b"
scraper = RecipeScraper(url, "Lasagne")
recipe = scraper.get_recipe()
recipe.convert('converts/VegToNonVeg.txt',{})


print(recipe)

