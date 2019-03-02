from database import Database

from scraper import Scraper
from seleniumscraper import SeleniumScraper
# from seleniumscraper import SeleniumScraper
url = "https://www.allrecipes.com/recipe/220643/ginas-creamy-mushroom-lasagna/?internalSource=streams&referringId=16800&referringContentType=Recipe%20Hub&clickId=st_trending_b"

url_sel = "https://www.allrecipes.com/recipes/15937/world-cuisine/middle-eastern/persian/"

# scraper = Scraper(url_sel)
# database = Database()
# tools = database.find_tools()
# actions = database.find_actions()
# scraper = Scraper(url,tools,actions)

scraper = SeleniumScraper(url_sel)

# recipe = scraper.get_recipe()
# database.insert_recipe(recipe)
# database.find_tools()

scraper.scrape_urls()
