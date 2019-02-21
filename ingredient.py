class IngredientBuilder(object):

    def __init__(self):
        self.name = ""
        self.quantity = 1.0
        self.measurement = None
        self.descriptor = None
        self.preparation = None

    def create_ingredient(self):
        return Ingredient(self.name, self.quantity, self.measurement, self.descriptor, self.preparation)

    def convert(self, text):
        # TODO: Add functionality for conversion to ingredient. Initialize attributes for class Ingredient.
        self.name = "olive oil"


class Ingredient(object):

    def __init__(self, name, quantity, measurement, descriptor, preparation):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.descriptor = descriptor
        self.preparation = preparation

    @staticmethod
    def convert_to_ingredients(ingredient_texts):
        ingredients = []
        for text in ingredient_texts:
            builder = IngredientBuilder()
            builder.convert(text)
            ingredients.append(builder.create_ingredient())
        return ingredients
