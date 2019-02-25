class IngredientBuilder(object):

    def __init__(self):
        self.name = ""
        self.quantity = 1.0
        self.measurement = None
        self.descriptor = None
        self.preparation = None
        self.phrase = ""

    @staticmethod
    def convert_to_ingredients(ingredient_texts):
        ingredients = []
        for text in ingredient_texts:
            builder = IngredientBuilder()
            builder.convert(text)
            ingredients.append(builder.create_ingredient())
        return ingredients

    def create_ingredient(self):
        return Ingredient(self.name, self.quantity, self.measurement, self.descriptor, self.preparation, self.phrase)

    def convert(self, text):
        # TODO: Add functionality for conversion to ingredient. Initialize attributes for class Ingredient.
        self.name = "olive oil" # Remove this one


class Ingredient(object):

    def __init__(self, name, quantity, measurement, descriptor, preparation, phrase):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.descriptor = descriptor
        self.preparation = preparation
        self.phrase = phrase

    def __repr__(self):
        return (str(self.quantity) + " " if self.quantity else "") + \
               (str(self.measurement) + " " if self.measurement else "") + \
               (str(self.descriptor) + " " if self.descriptor else "") + \
               (str(self.preparation) + " " if self.preparation else "") + \
               self.name

    def __str__(self):
        return "Ingredient Name: " + str(self.name)+ "\n"\
               "Quantity       : " + str(self.quantity) + "\n" \
               "Measurement    : " + str(self.measurement) + "\n"\
               "Descriptor     : " + str(self.descriptor) + "\n"\
               "Preparation    : " + str(self.preparation)

