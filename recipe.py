class RecipeBuilder(object):

    def __init__(self):
        self.ingredients = None
        self.prep_time = 0
        self.cook_time = 0
        self.total_time = 0

    def create_recipe(self):
        return Recipe(self.ingredients, self.prep_time, self.cook_time, self.total_time)


class Recipe(object):

    def __init__(self, ingredients, prep_time, cook_time, total_time):
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.total_time = total_time
