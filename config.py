import os
from sqlalchemy import create_engine

DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://postgres:1234@localhost:5432/videogames"
)

engine = create_engine(DB_URL)
