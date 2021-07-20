import os

import pandas as pd
from sqlalchemy import create_engine

# Some of this might be best in a constants.py file and read here and in app.py
TABLE_NAME = 'pets'
INDEX_COLUMN = 'id'
SOURCE_FILE = "sqlite:///etl/pets.sqlite"
SOURCE_SQL = f"SELECT * FROM {TABLE_NAME};"
# (https://help.heroku.com/ZKNTJQSK/
# why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres)
TARGET_DATABASE_URL = (
    os.environ.get('DATABASE_URL')
    .replace('postgres://', 'postgresql://', 1)
    )


# Read source file (this example happens to be .sqlite, but CSV is fine too)
def read_source():
    source_engine = create_engine(SOURCE_FILE)
    source_conn = source_engine.connect()
    source_df = pd.read_sql(TABLE_NAME, source_conn, index_col=INDEX_COLUMN)
    return source_df


# Create the table
def write_target(source_df):
    target_engine = create_engine(TARGET_DATABASE_URL)
    target_conn = target_engine.connect()
    source_df.to_sql(TABLE_NAME, target_conn, if_exists='replace')

    # sqlalchemy will not detect table without PK. This seems to be the best
    # solution (https://stackoverflow.com/q/50469391)
    target_engine.execute(
        f'ALTER TABLE {TABLE_NAME} ADD PRIMARY KEY ({INDEX_COLUMN});')


if __name__ == '__main__':
    source_data = read_source()
    write_target(source_data)
