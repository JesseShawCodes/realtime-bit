import aiohttp
import asyncio
import logging
from typing import Any, Dict, Optional

from app.models.models import Price
from app.db.db import get_db

logger = logging.getLogger("uvicorn.error") # Use the Uvicorn logger for integration

API_URL = "https://api.coingecko.com/api/v3/simple/price"
PARAMS = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}

async def fetch_prices() -> Optional[Dict[str, Any]]:
  """
  Fetch crypto prices asynchronously
  Returns None on Error
  """
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(API_URL, params=PARAMS) as response:
        if response.status != 200:
          logger.error(f"API error: {response.status}")
          return None
        data = await response.json()
        return data
  except Exception as e:
    logger.exception(f"Exception during fetch: {e}")
    return None


def _get_db_session():
  return next(get_db())

def save_prices(data: dict, db_session):
  logger.info(f"Saving data to DB: {data}")
  for asset, values in data.items():
    price = Price(asset=asset, price=values['usd'])
    db_session.add(price)
  db_session.commit()

async def poll_prices(interval: int = 30): # Increased interval for safety/rate limits
  logger.info(f"Starting price polling with interval: {interval} seconds")
  while True:
    try:
      data = await fetch_prices()
      if data:
        logger.debug(f"Fetched Data: {data}")
        db_session = _get_db_session()
        # Ensure your database connection setup is correct and handles pooling/cleanup
        try:
          save_prices(data, db_session)
        finally:
          db_session.close()
    except asyncio.CancelledError:
        logger.info("Polling task cancelled.")
        break
    except Exception as e:
        logger.error(f"Error in poll_prices loop: {e}")
        
    await asyncio.sleep(interval)

# Remove the `if __name__ == "__main__":` block.