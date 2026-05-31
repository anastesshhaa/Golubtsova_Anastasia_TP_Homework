class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.unit = unit
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    
    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        if ingredients == None:
            self.ingredients = []
        else:
            self.ingredients = ingredients

    def add_ingredient(self, ingredient : Ingredient):
        for i in self.ingredients:
            if ingredient == i:
                i.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        try:
            ratio = float(ratio)
            return ratio > 0
        except (TypeError, ValueError):
            return False

    def scale(self, ratio):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")
        ingredients1 = []
        for ingredient in self.ingredients:
            scaled_ingredient = Ingredient(ingredient.name, ingredient.quantity * float(ratio), ingredient.unit)
            ingredients1.append(scaled_ingredient)
        return Recipe(self.title, ingredients1)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = f"{self.title}\n"
        for ingredient in self.ingredients:
            result += str(ingredient) + "\n"
        return result.strip("\n")