from datastructure.resources import variables
from scraper.recipescraper import RecipeScraper

url = "https://www.allrecipes.com/recipe/220643/ginas-creamy-mushroom-lasagna/?internalSource=streams&referringId=16800&referringContentType=Recipe%20Hub&clickId=st_trending_b"
scraper = RecipeScraper(url, "")
recipe = scraper.get_recipe()
recipe.convert('converts/ToChinese.txt', variables=variables)

print(recipe)
