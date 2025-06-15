from fastapi import FastAPI
from app.views import include_routers
from app.database.init_db import init_db

app = FastAPI()

init_db()

include_routers(app)

@app.get("/", include_in_schema=False)
def home():
  return {"message": "Hello, Emmanuel"}