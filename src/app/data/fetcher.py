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

async def poll_prices(interval: int = 30):
    """Continuously polls for prices and saves them to the database."""
    logger.info(f"Starting price polling every {interval} seconds.")
    db_session = _get_db_session()
    try:
        while True:
            data = await fetch_prices()
            if data:
                logger.debug(f"Fetched data: {data}")
                save_prices(data, db_session)
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        logger.info("Polling task was cancelled.")
    except Exception as e:
        logger.error(f"An unexpected error occurred in the polling loop: {e}")
    finally:
        db_session.close()
        logger.info("Database session closed.")
