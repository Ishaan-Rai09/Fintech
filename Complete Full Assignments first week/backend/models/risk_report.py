"""
Risk report model
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.connection import Base


class RiskReport(Base):
    __tablename__ = "risk_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    report_date = Column(Date, nullable=False)
    var_95 = Column(Numeric(15, 2))
    var_99 = Column(Numeric(15, 2))
    expected_shortfall = Column(Numeric(15, 2))
    method = Column(String(50))
    timeframe = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="risk_reports")
