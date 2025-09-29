from src.db import Base, engine
from src.data import models

def init():
  Base.metadata.create_all(bind=engine)
  print("Database Initialized")

if __name__ == "__main__":
  init()