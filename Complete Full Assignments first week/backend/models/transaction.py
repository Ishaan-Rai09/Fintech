"""
Transaction model
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.connection import Base


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    transaction_date = Column(Date, nullable=False, index=True)
    description = Column(Text)
    amount = Column(Numeric(15, 2), nullable=False)
    category = Column(String(100))
    transaction_type = Column(String(50))
    is_suspicious = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
