from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends, HTTPException, Query
from typing import Annotated
import os

db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_username = os.getenv("DB_USERNAME")
db_name = os.getenv("DB_NAME")
db_url = f"postgresql+psycopg://{db_username}:{db_password}@{db_host}/{db_name}"
connect_args = {}

engine = create_engine(db_url, connect_args = connect_args) 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]