from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException

from app import models, schemas
from app.database import engine, get_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    Выполняется при старте приложения.
    Создает все таблицы в базе данных, если они еще не существуют.
    """
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    """
    Выполняется при завершении работы приложения.
    Закрывает соединение с базой данных.
    """
    await engine.dispose()


@app.get("/recipes", summary="Получить список всех рецептов")
async def recipes(db: AsyncSession = Depends(get_db)):
    """
    Возвращает список всех рецептов, отсортированных по количеству просмотров (по убыванию)
    и времени приготовления (по возрастанию).

    :param db: Асинхронная сессия базы данных.
    :return: Список рецептов.
    """
    query = select(models.Recipe).order_by(models.Recipe.views.desc(), models.Recipe.cooking_time.asc())
    res = await db.execute(query)
    return res.scalars().all()


@app.get("/recipes/{recipe_id}")
async def recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    """
    Возвращает рецепт по его ID.

    :param recipe_id: Идентификатор рецепта.
    :param db: Асинхронная сессия базы данных.
    :raises HTTPException: Если рецепт не найден, возвращает ошибку 404.
    :return: Рецепт.
    """
    result = await db.execute(select(models.Recipe).filter_by(id=recipe_id))
    recipe = result.scalars().first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.post("/recipes", response_model=schemas.RecipeCreate, summary="Создать новый рецепт")
async def create_recipe(recipe: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)):
    """
    Создает новый рецепт и сохраняет его в базе данных.

    :param recipe: Данные для создания нового рецепта (name, cooking_time, description).
    :param db: Асинхронная сессия базы данных.
    :return: Созданный рецепт.
    """
    db_recipe = models.Recipe(name=recipe.name, cooking_time=recipe.cooking_time, description=recipe.description)
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe


@app.post("/ingredients", response_model=schemas.IngredientCreate, summary="Добавить ингредиенты к рецепту по ID")
async def create_ingredient(ingredient: schemas.IngredientCreate, db: AsyncSession = Depends(get_db)):
    """
    Добавляет ингредиенты к рецепту по его ID.

    :param ingredient: Данные ингредиентов и ID рецепта, к которому они добавляются.
    :param db: Асинхронная сессия базы данных.
    :raises HTTPException: Если рецепт не найден, возвращает ошибку 404.
    :return: Созданный ингредиент.
    """
    result = await db.execute(select(models.Recipe).filter_by(id=ingredient.recipe_id))
    recipe = result.scalars().first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_ingredient = models.Ingredient(
        name=ingredient.name,
        cooking_time=recipe.cooking_time,
        description=recipe.description,
        list_of_ingredients=ingredient.list_of_ingredients,
        recipe_id=ingredient.recipe_id
    )

    db.add(db_ingredient)
    await db.commit()
    await db.refresh(db_ingredient)
    return db_ingredient


@app.delete("/delete_recipe{recipe_id}", response_model=schemas.RecipeDelete, summary="Удалить рецепт по ID")
async def delete_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удаляет рецепт по его ID.

    :param recipe_id: Идентификатор рецепта, который нужно удалить.
    :param db: Асинхронная сессия базы данных.
    :raises HTTPException: Если рецепт не найден, возвращает ошибку 404.
    :return: Сообщение об успешном удалении.
    """
    db_recipe = await db.execute(select(models.Recipe).filter_by(id=recipe_id))
    recipe = db_recipe.scalars().first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    await db.execute(delete(models.Recipe).where(models.Recipe.id == recipe_id))
    await db.commit()

    return {"message": f"Recipe with id {recipe_id} was successfully deleted."}
