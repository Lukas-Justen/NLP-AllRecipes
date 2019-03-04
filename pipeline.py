from scraper.recipescraper import RecipeScraper
from datastructure.resources import database
from scraper.seleniumscraper import SeleniumScraper

# url = "https://www.allrecipes.com/recipes/87/everyday-cooking/vegetarian/?internalSource=hubcard&referringContentType=Search&clickId=cardslot%201&page=2"
# category = "Vegetarian"
#
# scraper = SeleniumScraper(url)
# scraper.scrape_urls()
# urls = scraper.get_urls_to_be_scraped()
#
# print(len(urls))
#
# for u in urls:
#     print("Scraping: " + u)
#     scraper = RecipeScraper(u, category)
#     recipe = scraper.get_recipe()
#     database.insert_recipe(recipe)

url = "https://www.allrecipes.com/recipe/220643/ginas-creamy-mushroom-lasagna/?internalSource=streams&referringId=16800&referringContentType=Recipe%20Hub&clickId=st_trending_b"
scraper = RecipeScraper(url, "Lasagne")
recipe = scraper.get_recipe()
recipe
recipe.convert('converts/VegToNonVeg.txt',{})
recipe
# non_veg_proteins = database.find_ingredient_types(["meats","poultry","seafood","shellfish"])
# veg_proteins = database.find_ingredient_types(["vegetarian"])
#
# recipe.change(["broth", "boullion"], ["vegetable broth"])
# recipe.change_all(veg_proteins, non_veg_proteins)
# recipe

