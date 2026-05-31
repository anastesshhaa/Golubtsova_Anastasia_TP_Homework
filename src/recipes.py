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


class ShoppingList:
    def __init__(self):
        self._items = []
    
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for i in scaled_recipe.ingredients:
            self._items.append((i, recipe.title))
    
    def remove_recipe(self, title):
        items = []
        for i in self._items:
            if i[1] != title:
                items.append(i)
        self._items = items
    
    def get_list(self):
        res = {}
        for i, title in self._items:
            key = (i.name, i.unit)
            if key in res:
                res[key] += i.quantity
            else:
                res[key] = i.quantity
        shopping_list = []
        for (name, unit), q in res.items():
            shopping_list.append(Ingredient(name, q, unit))
        shopping_list.sort(key = lambda i: i.name)
        return shopping_list
    
    def __add__(self, other):
            list1 = ShoppingList()
            list1._items = (self._items.copy() + other._items.copy())
            return list1