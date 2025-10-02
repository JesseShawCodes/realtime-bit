from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.api.endpoints import routes
from app.data.fetcher import poll_prices
import logging
logger = logging.getLogger("uvicorn.error") # Use the Uvicorn logger for integration


app = FastAPI(title="Real-Time Data API")

# Global variable to hold the background task
background_task: Optional[asyncio.Task] = None

# --- Startup Event Handlers ---

@app.on_event("startup")
async def start_polling() -> None:
    """Starts the continuous background task (poll_prices)."""
    global background_task
    # Create the task without blocking the startup process
    background_task = asyncio.create_task(poll_prices(interval=30))
    logger.info("Background price polling task started.")

@app.on_event("shutdown")
async def stop_polling() -> None:
    """Stops the continuous background task when the server shuts down."""
    if background_task:
        background_task.cancel()
        logger.info("Background price polling task stopped.")

# --- Middleware and Router Setup ---

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
async def read_root() -> Dict[str, str]:
  return {"message": "Hello, FastAPI!"}
