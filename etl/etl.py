import os
import pandas as pd
from sqlalchemy import create_engine

# Some of this might be best in a constants.py file and read here and in app.py
TABLE_NAME = 'pets'
INDEX_COLUMN = 'id'
SOURCE_FILE = "sqlite:///etl/pets.sqlite"
SOURCE_SQL = f"SELECT * FROM {TABLE_NAME}"
TARGET_DATABASE_URL = os.environ.get('DATABASE_URL')

# Read source file (this example happens to be .sqlite, but CSV is fine too)
source_engine = create_engine(SOURCE_FILE)
pets_df = pd.read_sql(SOURCE_SQL, source_engine, index_col=INDEX_COLUMN)

# Write to PostgreSQL
target_engine = create_engine(TARGET_DATABASE_URL)
pets_df.to_sql(
    TABLE_NAME, target_engine, if_exists='replace', index_label=INDEX_COLUMN)
