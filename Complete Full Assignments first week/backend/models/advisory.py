"""
Risk profile and advisory models
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.connection import Base


class RiskProfile(Base):
    __tablename__ = "risk_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    risk_score = Column(Integer, CheckConstraint('risk_score >= 1 AND risk_score <= 10'))
    risk_category = Column(String(50))
    time_horizon = Column(Integer)
    investment_goals = Column(Text)
    questionnaire_responses = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="risk_profiles")
    recommendations = relationship("AdvisoryRecommendation", back_populates="risk_profile", cascade="all, delete-orphan")


class AdvisoryRecommendation(Base):
    __tablename__ = "advisory_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    risk_profile_id = Column(Integer, ForeignKey("risk_profiles.id"))
    asset_allocation = Column(Text)
    recommended_securities = Column(Text)
    rebalancing_strategy = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="advisory_recommendations")
    risk_profile = relationship("RiskProfile", back_populates="recommendations")
