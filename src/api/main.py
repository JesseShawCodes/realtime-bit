from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routes

app = FastAPI(title="Real-Time Data API")

app.include_router(routes.router)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://your-deployed-react-app.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
  return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}
