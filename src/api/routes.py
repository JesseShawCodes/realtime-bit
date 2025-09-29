from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..data import models

router = APIRouter()

@router.get("/health")
def health_check():
  return {"status": "ok"}

@router.get("/data/history")
def history(limit: int = 3, db: Session = Depends(get_db)):
  # df = get_data(limit=limit)
  rows = db.query(models.Price).order_by(models.Price.timestamp.desc()).limit(limit).all()
  return rows

@router.get("/data/latest")
def get_latest(limit: int = 10, db: Session = Depends(get_db)):
  """
  Return the last N rows from database
  """
  rows = db.query(models.Price).order_by(models.Price.timestamp.desc()).limit(limit).all()
  return rows

@router.get("/data/metrics")
def get_metrics(db: Session = Depends(get_db), limit: int = 10):
  """
  Compute simple metrics from the DB
  """
  q = db.query(models.Price).order_by(models.Price.timestamp.desc()).limit(limit).all()
  if not q:
    return {"error": "no data"}
  
  values = [r.price for r in q]
  return {
    "min": min(values),
    "max": max(values),
    "avg": sum(values)/len(values)
  }