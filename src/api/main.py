from fastapi import FastAPI
from . import routes

app = FastAPI(title="Real-Time Data API")

app.include_router(routes.router)

@app.get("/")
async def read_root():
  return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}
