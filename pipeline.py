from database import Database

from scraper import Scraper
from seleniumscraper import SeleniumScraper
# from seleniumscraper import SeleniumScraper
url = "https://www.allrecipes.com/recipe/220643/ginas-creamy-mushroom-lasagna/?internalSource=streams&referringId=16800&referringContentType=Recipe%20Hub&clickId=st_trending_b"
url_sel = "https://www.allrecipes.com/recipes/15937/world-cuisine/middle-eastern/persian/"
# sraper = Scraper(url_sel)
database = Database()

sraper = SeleniumScraper(url_sel)

# recipe = scraper.get_recipe()
# database.insert_recipe(recipe)

# database.find_tools()

sraper.scrape_urls()