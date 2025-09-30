from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from ..db.db import Base

class Price(Base):
  __tablename__ = "prices"

  id = Column(Integer, primary_key=True, index=True)
  asset = Column(String, index=True)
  price = Column(Float)
  timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
