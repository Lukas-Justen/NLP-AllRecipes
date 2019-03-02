from database import Database
from scraper import Scraper

url = "https://www.allrecipes.com/recipe/220643/ginas-creamy-mushroom-lasagna/?internalSource=streams&referringId=16800&referringContentType=Recipe%20Hub&clickId=st_trending_b"

database = Database()
tools = database.find_tools()
actions = database.find_actions()
scraper = Scraper(url,tools,actions)

recipe = scraper.get_recipe()
print(recipe)
database.insert_recipe(recipe)

# database.find_tools()