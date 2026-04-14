# # backend/init_db.py

# from backend.models import Base, engine   # assumes models.py defines Base

# Base.metadata.create_all(bind=engine)

# # backend/init_db.py

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # Replace with your actual connection string
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/exercises"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Dependency for FastAPI routes
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# backend/init_db.py

from backend.models import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()