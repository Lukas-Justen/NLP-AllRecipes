from database import Database

from scraper import Scraper
from seleniumscraper import SeleniumScraper

url = "https://www.allrecipes.com/recipes/15937/world-cuisine/middle-eastern/persian/"

scraper = SeleniumScraper(url)
scraper.scrape_urls()
urls = scraper.get_urls_to_be_scraped()

database = Database()
tools = database.find_tools()
actions = database.find_actions()
recipes = []

for u in urls:
    scraper = Scraper(u,tools,actions)
    recipes.append(scraper.get_recipe())

print(len(recipes))
print(recipes)