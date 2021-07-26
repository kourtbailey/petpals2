import os

import pandas as pd
from sqlalchemy import create_engine

# Use one or the other:
SOURCE_PATH = 'etl/pets.csv'
# SOURCE_PATH = 'sqlite:///etl/pets.sqlite'

TABLE_NAME = 'pets'
INDEX_COLUMN = 'id'
SOURCE_SQL = f"SELECT * FROM {TABLE_NAME};"

# (https://help.heroku.com/ZKNTJQSK/
# why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres)
TARGET_DATABASE_URL = (
    os.environ.get('DATABASE_URL')
    .replace('postgres://', 'postgresql://', 1)
    )


# Read source data
def read_source(source_path):
    if source_path.startswith('sqlite'):
        source_engine = create_engine(source_path)
        source_conn = source_engine.connect()
        source_df = pd.read_sql(
            TABLE_NAME, source_conn, index_col=INDEX_COLUMN)

    elif source_path.lower().endswith('csv'):
        source_df = pd.read_csv(source_path)

    else:
        raise TypeError("Unsupported file format")

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
    source_data = read_source(SOURCE_PATH)
    write_target(source_data)
