from datastructure.resources import variables
from scraper.recipescraper import RecipeScraper
from tagging.ingredient_train import *


print("WELCOME TO THE RECIPE CONVERTER")
print("===============================\n")

print("Please enter a url to a recipe from www.allrecipes.com!")
print("Url:", end=" ")
url = str(input())

print("\n\nWhat kind of conversion do you want to apply to the recipe?")
print("1:   To Vegetarian")
print("2:   To Non-Vegetarian")
print("3:   To Healthy")
print("4:   To Unhealthy")
print("5:   To Indian")
print("6:   To German")
print("7:   To Chinese")
conv = {1: "converts/ToVeg.txt",
        2: "converts/ToNonveg.txt",
        3: "converts/ToHealthy.txt",
        4: "converts/ToUnhealthy.txt",
        5: "converts/ToIndian.txt",
        6: "converts/ToGerman.txt",
        7: "converts/ToChinese.txt"}
print("Conversion:" , end=" ")
conversion = int(input())



print("\n\nTHE CURRENT RECIPE:")

scraper = RecipeScraper(url, "")
recipe = scraper.get_recipe()

print(recipe)



print("\n\n\n\nTHE NEW RECIPE:")
replacements, additions, scalings = recipe.convert(conv[conversion], variables=variables)

print(recipe)



if len(replacements) > 0:
    print("\n\nREPLACEMENTS MADE:")
    for r in replacements:
        print(r)
else:
    print("NO REPLACEMENTS MADE")

if len(additions) > 0:
    print("\nADDITIONS MADE:")
    for a in additions:
        print(a)
else:
    print("\nNO ADDITIONS MADE")

if len(scalings) > 0:
    print("\nSCALINGS MADE:")
    for s in scalings:
        print(s)
else:
    print("\nNO SCALINGS MADE")