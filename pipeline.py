from database import Database
from scraper import Scraper

url = "https://www.allrecipes.com/recipe/220643/ginas-creamy-mushroom-lasagna/?internalSource=streams&referringId=16800&referringContentType=Recipe%20Hub&clickId=st_trending_b"

scraper = Scraper(url)
database = Database()

recipe = scraper.get_recipe()
database.insert_recipe(recipe)

print(recipe)
