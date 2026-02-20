"""
Tax record model
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.connection import Base


class TaxRecord(Base):
    __tablename__ = "tax_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    financial_year = Column(String(10), nullable=False)
    gross_income = Column(Numeric(15, 2))
    deductions = Column(Numeric(15, 2))
    taxable_income = Column(Numeric(15, 2))
    tax_liability = Column(Numeric(15, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="tax_records")
