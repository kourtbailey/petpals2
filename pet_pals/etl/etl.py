import os
from sqlalchemy import create_engine

from ..models import Pet, db
from ..app.app import create_app

# Some of this might be best in a constants.py file and read here and in app.py
TABLE_NAME = 'pets'
INDEX_COLUMN = 'id'
SOURCE_FILE = "sqlite:///pet_pals/etl/pets.sqlite"
SOURCE_SQL = f"SELECT * FROM {TABLE_NAME};"
# (https://help.heroku.com/ZKNTJQSK/
# why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres)
TARGET_DATABASE_URL = (
    os.environ.get('DATABASE_URL')
    .replace('postgres://', 'postgresql://', 1)
    )
print(TARGET_DATABASE_URL)

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

        for source_pet in source_data:
            source_pet_data = {**source_pet}  # mapping-unpacking operator
            # Remove the id: if we do not remove it, then something about the
            # autoincrement / sqeuence is broken, and adding new pets in the
            # app will fail.  This way SQLAlchemy will always automatically set
            # the id, both here and in the app.
            source_pet_data.pop('id')
            new_pet = Pet(**source_pet_data)
            db.session.add(new_pet)

        db.session.commit()


if __name__ == '__main__':
    source_data = read_source()
    write_target(source_data)
