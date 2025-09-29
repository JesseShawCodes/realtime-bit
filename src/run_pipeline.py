import asyncio
from src.data.fetcher import fetch_prices
from src.data.processor import normalize, update_history, compute_metrics, save_to_db

async def main():
  raw = await fetch_prices()
  normalized = normalize(raw)

  if normalized:
    update_history(normalized)
    save_to_db(normalized)
  
  metrics = compute_metrics()
  print("Metrics", metrics)

if __name__ == "__main__":
  asyncio.run(main())