from tagging.utils import tag_ingredient_parts


class IngredientBuilder(object):

    def __init__(self):
        self.name = ""
        self.quantity = 0.0
        self.measurement = None
        self.descriptor = None
        self.preparation = None
        self.phrase = ""

    @staticmethod
    def convert_to_ingredients(ingredient_texts):
        ingredients = []
        for phrase in ingredient_texts:
            builder = IngredientBuilder()
            builder.convert(phrase)
            ingredients.append(builder.create_ingredient())
        return ingredients

    def create_ingredient(self):
        return Ingredient(self.name, self.quantity, self.measurement, self.descriptor, self.preparation, self.phrase)

    def convert(self, phrase):
        taggings = tag_ingredient_parts(phrase)
        self.quantity = taggings["qty"] if "qty" in taggings else self.quantity
        self.measurement = taggings["unit"] if "unit" in taggings else self.quantity
        self.name = taggings["name"] if "name" in taggings else self.quantity
        self.preparation = taggings["comment"] if "comment" in taggings else self.preparation
        self.phrase = phrase


class Ingredient(object):

    def __init__(self, name, quantity, measurement, descriptor, preparation, phrase):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.descriptor = descriptor
        self.preparation = preparation
        self.phrase = phrase

    def __repr__(self):
        representation =  (str(self.quantity) + ", " if self.quantity else "") + \
               (str(self.measurement) + ", " if self.measurement else "") + \
               (str(self.descriptor) + ", " if self.descriptor else "") + \
               (str(self.preparation) + ", " if self.preparation else "") + \
               self.name
        return representation if representation != "" else self.phrase

    def __str__(self):
        return "Ingredient Name: " + str(self.name)+ "\n"\
               "Quantity       : " + str(self.quantity) + "\n" \
               "Measurement    : " + str(self.measurement) + "\n"\
               "Descriptor     : " + str(self.descriptor) + "\n"\
               "Preparation    : " + str(self.preparation) + "\n"\
               "Phrase         : " + str(self.phrase) + "\n"\

