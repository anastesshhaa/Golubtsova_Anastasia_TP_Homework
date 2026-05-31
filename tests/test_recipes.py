import pytest
from src.recipes import Ingredient
from src.recipes import Recipe
from src.recipes import ShoppingList
from src.recipes import DietaryRecipe

def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"

def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")
    assert str(ingredient) == "Мука: 500.0 г"

def test_ingredient_repr():
    ingredient = Ingredient("Мука", 500, "г")
    assert repr(ingredient) == ("Ingredient('Мука', 500.0, 'г')")

def test_ingredient_equality():
    ingredient1 = Ingredient("Мука", 100, "г")
    ingredient2 = Ingredient("Мука", 500, "г")
    assert ingredient1 == ingredient2

def test_ingredient_negative_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", -5, "г")


def test_recipe_creation():
    ingredients = [Ingredient("Мука", 500, "г"), Ingredient("Вода", 300, "мл")]
    recipe = Recipe("Тесто", ingredients)
    assert recipe.title == "Тесто"
    assert len(recipe.ingredients) == 2

def test_add_new_ingredient():
    recipe = Recipe("Тесто")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"

def test_add_existing_ingredient_adds():
    recipe = Recipe("Тесто")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 700.0

def test_is_valid_ratio():
    assert Recipe.is_valid_ratio(2) is True
    assert Recipe.is_valid_ratio(1.5) is True
    assert Recipe.is_valid_ratio(0) is False
    assert Recipe.is_valid_ratio(-1) is False
    assert Recipe.is_valid_ratio("abc") is False

def test_scale_recipe():
    recipe = Recipe("Тесто", [Ingredient("Мука", 500, "г"), Ingredient("Вода", 300, "мл")])
    scaled_recipe = recipe.scale(2)
    assert scaled_recipe.title == "Тесто"
    assert scaled_recipe.ingredients[0].quantity == 1000.0
    assert scaled_recipe.ingredients[1].quantity == 600.0

def test_scale_original_recipe_is_unchanged():
    recipe = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    scaled_recipe = recipe.scale(2)
    assert recipe.ingredients[0].quantity == 500.0
    assert scaled_recipe.ingredients[0].quantity == 1000.0

def test_scale_with_bad_ratio():
    recipe = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    with pytest.raises(ValueError):
        recipe.scale(0)

def test_recipe_len():
    recipe = Recipe("Тесто", [Ingredient("Мука", 500, "г"), Ingredient("Вода", 300, "мл")])
    assert len(recipe) == 2


def test_add_recipe_to_shopping_list():
    recipe = Recipe("Тесто", [Ingredient("Мука", 500, "г"), Ingredient("Вода", 300, "мл")])
    list = ShoppingList()
    list.add_recipe(recipe, 2)
    result = list.get_list()
    assert len(result) == 2
    assert result[0].name == "Вода"
    assert result[0].quantity == 600.0
    assert result[1].name == "Мука"
    assert result[1].quantity == 1000.0

def test_add_recipe_with_bad_portions():
    recipe = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    list = ShoppingList()
    with pytest.raises(ValueError):
        list.add_recipe(recipe, 0)

def test_get_list_adds_same_ingredients():
    recipe1 = Recipe("Пицца", [Ingredient("Мука", 500, "г"), Ingredient("Сыр", 200, "г")])
    recipe2 = Recipe("Пирог", [Ingredient("Мука", 300, "г"), Ingredient("Клубнички", 4, "шт")])
    list = ShoppingList()
    list.add_recipe(recipe1, 1)
    list.add_recipe(recipe2, 1)
    result = list.get_list()
    flour = None
    for ingredient in result:
        if ingredient.name == "Мука":
            flour = ingredient
    assert flour is not None
    assert flour.quantity == 800.0

def test_remove_recipe():
    recipe1 = Recipe("Какао", [Ingredient("Бобы", 500, "г")])
    recipe2 = Recipe("Кофэ", [Ingredient("Зерно", 2, "шт")])
    list = ShoppingList()
    list.add_recipe(recipe1, 1)
    list.add_recipe(recipe2, 1)
    list.remove_recipe("Какао")
    result = list.get_list()
    assert len(result) == 1
    assert result[0].name == "Зерно"

def test_add_shopping_lists():
    recipe1 = Recipe("Какао", [Ingredient("бобы", 500, "г")])
    recipe2 = Recipe("Кофэ", [Ingredient("Зерно", 2, "шт")])
    list1 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list2 = ShoppingList()
    list2.add_recipe(recipe2, 1)
    result_list = list1 + list2
    result = result_list.get_list()
    assert len(result) == 2


def test_dietary_recipe_creation():
    recipe = DietaryRecipe("Салат", "веган")
    assert recipe.title == "Салат"
    assert recipe.diet_type == "веган"
    assert recipe.ingredients == []

def test_dietary_recipe_scale():
    recipe = DietaryRecipe("Салат", "веган", [Ingredient("Авокадо", 2, "шт")])
    scaled = recipe.scale(2)
    assert isinstance(scaled, DietaryRecipe)
    assert scaled.diet_type == "веган"
    assert scaled.ingredients[0].quantity == 4.0

def test_dietary_recipe_str():
    recipe = DietaryRecipe("Салат", "веган",[Ingredient("Авокадо", 2, "шт")])
    result = str(recipe)
    assert "[веган]" in result
    assert "Салат" in result