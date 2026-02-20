"""
Scraped data model
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from backend.database.connection import Base


class ScrapedData(Base):
    __tablename__ = "scraped_data"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    data_type = Column(String(100))
    ticker_symbol = Column(String(20), index=True)
    data_content = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)
