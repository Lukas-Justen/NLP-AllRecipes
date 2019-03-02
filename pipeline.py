from scraper.recipescraper import RecipeScraper
from datastructure.resources import database
from scraper.seleniumscraper import SeleniumScraper

url = "https://www.allrecipes.com/recipes/87/everyday-cooking/vegetarian/?internalSource=hubcard&referringContentType=Search&clickId=cardslot%201&page=2"
category = "Vegetarian"

scraper = SeleniumScraper(url)
scraper.scrape_urls()
urls = scraper.get_urls_to_be_scraped()

print(len(urls))

for u in urls:
    print("Scraping: " + u)
    scraper = RecipeScraper(u, category)
    recipe = scraper.get_recipe()
    database.insert_recipe(recipe)
