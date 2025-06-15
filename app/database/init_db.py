from app.database.postgre import engine, Base
from app.models.user_model import UserModel

def init_db():
  print("Initializing database...")
  Base.metadata.create_all(bind=engine)
  print("Database Created Successfully!")