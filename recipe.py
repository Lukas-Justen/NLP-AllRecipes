class RecipeBuilder(object):

    def __init__(self):
        self.ingredients = None
        self.prep_time = 0.0
        self.cook_time = 0.0
        self.total_time = 0.0
        self.servings_count = 1.0

    def create_recipe(self):
        return Recipe(self.ingredients, self.prep_time, self.cook_time, self.total_time, self.servings_count)


class Recipe(object):

    def __init__(self, ingredients, prep_time, cook_time, total_time, servings_count):
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.total_time = total_time
        self.servings_count = servings_count

    def __str__(self):
        return "Preparataion Time: " + str(self.prep_time) + "\n" \
               "Cooking Time: " + str(self.cook_time) + "\n"\
               "Total Time: " + str(self.total_time) + "\n"\
               "Servings Count: " + str(self.servings_count)