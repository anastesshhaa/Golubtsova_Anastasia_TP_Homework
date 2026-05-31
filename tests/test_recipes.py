import pytest
from src.recipes import Ingredient
from src.recipes import Recipe

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