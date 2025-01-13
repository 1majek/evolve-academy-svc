from pydantic import BaseModel
from typing import Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Chat (BaseModel):
    prompt: str

class ListChat (BaseModel):
    prompt: Optional[List]

class Recipe (SQLModel, table = True):
    id: int | None = Field(default=None, primary_key= True)
    description: str