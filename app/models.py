from .database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Annotated

str_256 = Annotated[str, 256, mapped_column(nullable=False)]
intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Recipe(Base):
    """
    Модель SQLAlchemy для таблицы `recipes`, представляющей рецепт.

    Атрибуты:
        id (int): Уникальный идентификатор рецепта, первичный ключ, автоинкремент.
        name (str): Название рецепта, обязательное поле, максимальная длина 256 символов.
        views (int): Количество просмотров рецепта, по умолчанию 0.
        cooking_time (int): Время приготовления в минутах, обязательное поле.
        description (str): Описание рецепта, обязательное поле, максимальная длина 256 символов.
        ingredients (List[Ingredient]): Список ингредиентов, связанных с рецептом. Отношение `один ко многим`.
    """
    __tablename__ = 'recipes'

    id: Mapped[intpk]
    name: Mapped[str_256]
    views: Mapped[int] = mapped_column(default=0)
    cooking_time: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str_256]

    ingredients: Mapped['Ingredient'] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        """
        Метод для строкового представления объекта.
        """
        return f"<Recipe(name={self.name}, views={self.views}, cooking_time={self.cooking_time})>"

    def to_json(self):
        """
        Метод для сериализации объекта в формат JSON.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Ingredient(Base):
    """
    Модель SQLAlchemy для таблицы `ingredients`, представляющей ингредиенты рецепта.

    Атрибуты:
        id (int): Уникальный идентификатор ингредиента, первичный ключ, автоинкремент.
        name (str): Название ингредиента, обязательное поле, максимальная длина 256 символов.
        cooking_time (int): Время приготовления, аналогичное времени рецепта.
        description (str): Описание ингредиента, обязательное поле, максимальная длина 256 символов.
        list_of_ingredients (str): Список ингредиентов, необходимых для приготовления.
        recipe_id (int): Внешний ключ, ссылающийся на `id` рецепта в таблице `recipes`, обязательное поле.
        recipe (Recipe): Объект рецепта, к которому относится ингредиент. Отношение `многие к одному`.
    """
    __tablename__ = 'ingredients'

    id: Mapped[intpk]
    name: Mapped[str_256]
    cooking_time: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str_256]
    list_of_ingredients: Mapped[str_256]
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)

    recipe: Mapped['Recipe'] = relationship(
        back_populates="ingredients"
    )

    def __repr__(self):
        """
        Метод для строкового представления объекта.
        """
        return f"<Ingredient(name={self.name}, recipe_id={self.recipe_id})>"

    def to_json(self):
        """
        Метод для сериализации объекта в формат JSON.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
