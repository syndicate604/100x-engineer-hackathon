import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

def get_db():
    """
    Create a database connection and return a session.
    If the database doesn't exist, it will be created.
    """
    # Use a local SQLite database in the project root
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'local.db')
    
    # Create SQLAlchemy engine
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        create_database(engine.url)
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
