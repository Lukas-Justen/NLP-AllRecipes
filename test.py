from scraper.recipescraper import RecipeScraper

scraper = RecipeScraper("https://www.allrecipes.com/recipe/220643", "")
recipe = scraper.get_recipe()