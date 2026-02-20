"""
Robo-Advisory API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.schemas.auth import APIResponse
from backend.services.robo_advisor import RoboAdvisor
from typing import List, Dict

router = APIRouter(prefix="/advisory", tags=["Robo Advisory"])

robo_advisor = RoboAdvisor()


@router.get("/questionnaire", response_model=APIResponse)
async def get_questionnaire():
    """
    Get risk profiling questionnaire
    """
    return APIResponse(
        status="success",
        message="Risk questionnaire retrieved",
        data={"questions": robo_advisor.RISK_QUESTIONNAIRE}
    )


@router.post("/profile", response_model=APIResponse)
async def create_risk_profile(
    answers: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create risk profile from questionnaire answers
    """
    try:
        if len(answers) != len(robo_advisor.RISK_QUESTIONNAIRE):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expected {len(robo_advisor.RISK_QUESTIONNAIRE)} answers"
            )
        
        profile = robo_advisor.calculate_risk_score(answers)
        
        # Save to database
        from backend.models.advisory import RiskProfile
        import json
        
        risk_profile = RiskProfile(
            user_id=current_user.id,
            risk_score=profile["risk_score"],
            risk_category=profile["category"],
            questionnaire_responses=json.dumps(answers)
        )
        
        db.add(risk_profile)
        db.commit()
        db.refresh(risk_profile)
        
        return APIResponse(
            status="success",
            message="Risk profile created",
            data={
                "profile_id": risk_profile.id,
                **profile
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating risk profile: {str(e)}"
        )


@router.post("/recommend", response_model=APIResponse)
async def get_recommendations(
    risk_score: int,
    investment_amount: float = 10000,
    current_user: User = Depends(get_current_user)
):
    """
    Get investment recommendations based on risk score
    """
    try:
        if not 1 <= risk_score <= 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Risk score must be between 1 and 10"
            )
        
        recommendations = robo_advisor.recommend_securities(risk_score, investment_amount)
        
        return APIResponse(
            status="success",
            message="Recommendations generated",
            data=recommendations
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.post("/strategy", response_model=APIResponse)
async def generate_strategy(
    risk_score: int,
    investment_amount: float,
    time_horizon_years: int = 10,
    current_user: User = Depends(get_current_user)
):
    """
    Generate comprehensive investment strategy
    """
    try:
        allocation = robo_advisor.recommend_asset_allocation(risk_score)
        recommendations = robo_advisor.recommend_securities(risk_score, investment_amount)
        
        strategy = {
            "risk_profile": {
                "score": risk_score,
                "category": robo_advisor.calculate_risk_score([risk_score] * 5)["category"]
            },
            "investment_details": {
                "amount": investment_amount,
                "time_horizon_years": time_horizon_years
            },
            "asset_allocation": allocation,
            "recommended_securities": recommendations["securities"],
            "action_plan": [
                "1. Open investment accounts (brokerage, retirement)",
                "2. Set up automatic monthly contributions",
                "3. Purchase recommended securities according to allocation",
                "4. Review and rebalance quarterly",
                "5. Increase contributions as income grows"
            ]
        }
        
        return APIResponse(
            status="success",
            message="Investment strategy generated",
            data=strategy
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating strategy: {str(e)}"
        )


@router.post("/rebalance", response_model=APIResponse)
async def get_rebalancing_advice(
    current_allocation: Dict[str, float],
    target_allocation: Dict[str, float],
    current_user: User = Depends(get_current_user)
):
    """
    Get portfolio rebalancing recommendations
    """
    try:
        rebalancing = robo_advisor.rebalancing_strategy(current_allocation, target_allocation)
        
        return APIResponse(
            status="success",
            message="Rebalancing strategy generated",
            data=rebalancing
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating rebalancing: {str(e)}"
        )
