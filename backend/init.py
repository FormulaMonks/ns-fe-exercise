import os
import sys
from sqlalchemy import create_engine

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './app')))

from app.db.base import Base
from app.db.session import engine
from app.models.transaction import Transaction
from app.models.category import Category

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    init_db()
