import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..models import Pet, db
from ..app.app import create_app

# Some of this might be best in a constants.py file and read here and in app.py
TABLE_NAME = 'pets'
INDEX_COLUMN = 'id'
SOURCE_FILE = "sqlite:///pet_pals/etl/pets.sqlite"
SOURCE_SQL = f"SELECT * FROM {TABLE_NAME};"
TARGET_DATABASE_URL = os.environ.get('DATABASE_URL')


# Read source file (this example happens to be .sqlite, but CSV is fine too)
def read_source():
    source_engine = create_engine(SOURCE_FILE)
    source_data = source_engine.execute(SOURCE_SQL).fetchall()
    return source_data


# Create the table
def write_target(source_data):
    app = create_app()
    with app.app_context():
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
        db.drop_all()
        db.create_all()

        target_engine = create_engine(TARGET_DATABASE_URL)
        session = Session(target_engine)
        for s in source_data:
            new_pet = Pet(**s)
            session.add(new_pet)
        session.commit()


if __name__ == '__main__':
    source_data = read_source()
    write_target(source_data)
