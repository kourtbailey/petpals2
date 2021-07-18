import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import db
from models import Pet

# Some of this might be best in a constants.py file and read here and in app.py
TABLE_NAME = 'pets'
INDEX_COLUMN = 'id'
SOURCE_FILE = "sqlite:///pet_pals/pets.sqlite"
SOURCE_SQL = f"SELECT * FROM {TABLE_NAME};"
TARGET_DATABASE_URL = os.environ.get('DATABASE_URL')

# Read source file (this example happens to be .sqlite, but CSV is fine too)
source_engine = create_engine(SOURCE_FILE)
source_data = source_engine.execute(SOURCE_SQL).fetchall()

# Create the table
db.drop_all()
db.create_all()

target_engine = create_engine(TARGET_DATABASE_URL)
session = Session(target_engine)
for s in source_data:
    new_pet = Pet(**s)
    session.add(new_pet)
session.commit()
