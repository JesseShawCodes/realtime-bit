from fastapi import FastAPI
from . import routes

from starlette.middleware.wsgi import WSGIMiddleware
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd


app = FastAPI(title="Real-Time Data API")

app.include_router(routes.router)

@app.get("/")
async def read_root():
  return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}
