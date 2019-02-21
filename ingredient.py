class Ingredient(object):

    def __init__(self, name, quantity=1, measurement=None, descriptor=None, preparation=None):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.descriptor = descriptor
        self.preparation = preparation

    @staticmethod
    def convert(ingredient_texts):
        return [Ingredient.create_ingredient(text) for text in ingredient_texts]

    @staticmethod
    def create_ingredient(text):
        # TODO: Add functionality for conversion to ingredient. Initialize attributes of class Ingredient.
        return Ingredient("olive oil")
