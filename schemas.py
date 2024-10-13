from pydantic import BaseModel


class RecipeCreate(BaseModel):
    """
    Схема Pydantic для создания нового рецепта.

    Атрибуты:
        name (str): Название рецепта. Обязательное поле.
        cooking_time (int): Время приготовления в минутах. Обязательное поле.
        description (str): Описание рецепта. Обязательное поле.
    """
    name: str
    cooking_time: int
    description: str


class IngredientCreate(BaseModel):
    """
    Схема Pydantic для добавления ингредиентов к существующему рецепту.

    Атрибуты:
        name (str): Название ингредиента. Обязательное поле.
        list_of_ingredients (str): Список ингредиентов в текстовом формате. Обязательное поле.
        recipe_id (int): Идентификатор рецепта, к которому добавляется ингредиент. Обязательное поле.
    """
    name: str
    list_of_ingredients: str
    recipe_id: int


class RecipeDelete(BaseModel):
    """
    Схема Pydantic для ответа на запрос об удалении рецепта.

    Атрибуты:
        message (str): Сообщение о результате удаления рецепта. Обязательное поле.
    """
    message: str
