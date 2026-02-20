"""
Stock model
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.connection import Base


class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker_symbol = Column(String(20), unique=True, nullable=False, index=True)
    company_name = Column(String(255))
    sector = Column(String(100))
    industry = Column(String(100))
    current_price = Column(Numeric(15, 4))
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    holdings = relationship("PortfolioHolding", back_populates="stock")
