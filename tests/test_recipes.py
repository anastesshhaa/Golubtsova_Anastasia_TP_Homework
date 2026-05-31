import pytest
from src.recipes import Ingredient

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