from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import statistics

# from src.db import SessionLocal
#from src.data.models import Price
from ..db.db import SessionLocal
from ..models.models import Price

# Simple in-memory history for demo purposes
_price_history: Dict[str, List[float]] = {
  "bitcoin": [],
  "ethereum": []
}

def normalize(raw_data: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
  """
  Convert raw API data into a normalized list with timestamps
  """
  if not raw_data:
    return []
  
  timestamp = datetime.now(timezone.utc).isoformat()
  normalized = [
    {"asset": asset, "price": values["usd"], "timestamp": timestamp}
    for asset, values in raw_data.items()
  ]
  return normalized

def update_history(normalized: List[Dict[str, Any]]) -> None:
  """
  Store the latest price into the in-memory history.
  """
  for entry in normalized:
    asset = entry["asset"]
    price = entry["price"]
    _price_history.setdefault(asset, []).append(price)

    if len(_price_history[asset]) > 100:
      _price_history[asset].pop(0)

def compute_metrics() -> Dict[str, Dict[str, float]]:
  """
  Compute simple metrics (min, max, moving average) for each asset.
  """
  metrics = {}
  for asset, prices in _price_history.items():
    if not prices:
      continue
    metrics[asset] = {
      "min": min(prices),
      "max": max(prices),
      "moving_avg": round(statistics.mean(prices), 2)
    }
  return metrics

def save_to_db(normalized):
  """
  Save normalized data to postgresql
  """
  session = SessionLocal()
  try:
    for entry in normalized:
      record = Price(
        asset=entry["asset"],
        price=entry["price"],
        timestamp=entry["timestamp"]
      )
      session.add(record)
    session.commit()
  except Exception as e:
    session.rollback()
    raise
  finally:
    session.close()
  
if __name__ == "__main__":
  from fetcher import fetch_prices
  import asyncio

  async def demo():
    raw = await fetch_prices()
    normalized = normalize(raw)
    update_history(normalized)
    metrics = compute_metrics()

    print("Normalized:", normalized)
    print("Metrics", metrics)

  asyncio.run(demo())