from fastapi import FastAPI, Depends, HTTPException, Query
from utils import generate_content
from sqlmodel import select
from classes import Chat, ListChat, Recipe
from dbUtils import create_db_and_tables, SessionDep
from typing import Annotated

app = FastAPI()

@app.on_event("startup")
def on_startup():
   create_db_and_tables()

@app.get("/")
async def root():
    return {"Message", "Hello World!"}

@app.post("/prompt")
async def prompt(req: Chat):
   response = generate_content(req.prompt)
   return response.text

@app.post("/recipe")
async def recipe(req: ListChat, session: SessionDep):
   ins_prompt: str = """
   Eres un cocinero de varias estrellas Michelín.
   Te voy a dar un listado de ingredientes y debes generer una receta
   de alguna estrella Michelín que contenta esos ingredientes.

   Los ingredientes son los siguientes:

   %s

   Aquí te paso un ejmplo de receta:
   Paso de la receta:
   Tiempo: 3 minutos
   Paso 1: Ingredientes listos
   Paso 2: Pon un hilito de aove en una sartén y echa los huevos un poco batidos.
   Paso 3: En cuanto cuaje el huevo, pon una ramita de orégano y sírvelo.
   Ingredientes: Huevo y atún.

   Devuelve la receta en formato Markdown
   """ % (req.prompt)
   response = generate_content(ins_prompt)
   recipe = Recipe()
   recipe.description = response.text

   # Save to database
   session.add(recipe)
   session.commit()
   session.refresh(recipe)
   print(recipe.description)

@app.get("/recipes")
async def get_recipies(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Recipe]:
   recipes = session.exec(select(Recipe).offset(offset).limit(limit)).all()
   return recipes
   