import aiohttp
import asyncio
import logging
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def poll_prices(interval: int = 10):
  while True:
    data = await fetch_prices()
    if data:
      logger.info(f"Fetched Data: {data}")
    await asyncio.sleep(interval)

if __name__ == "__main__":
  # result = asyncio.run(fetch_prices())
  # print(result)
  asyncio.run(poll_prices())
