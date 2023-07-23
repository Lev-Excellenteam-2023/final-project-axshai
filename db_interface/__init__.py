import os

from sqlalchemy import create_engine

DB_PATH = "db"
DB_NAME = "database.db"
engine = create_engine(rf"sqlite:///{os.path.join(os.path.join(__file__, '..', '..', DB_PATH, DB_NAME))}", echo=True)
