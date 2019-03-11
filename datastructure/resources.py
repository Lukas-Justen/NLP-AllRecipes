from datastructure.database import Database

database = Database()

tools = database.find_tools()
actions = database.find_actions()

variables = database.find_ingredient_types(["meats", "seafood",
     "poultry", "shellfish",
     "vegetarian", "legumes",
     "fruits", "cheeses",
     "grains", "noodles",
     "nuts", "vegetables",
     "spices", "liquids"])
