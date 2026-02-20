"""
Tax Calculation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.schemas.auth import APIResponse
from backend.services.tax_calculator import TaxCalculator
from typing import Dict, Optional

router = APIRouter(prefix="/tax", tags=["Tax Optimization"])

tax_calculator = TaxCalculator()


@router.post("/calculate", response_model=APIResponse)
async def calculate_tax(
    gross_income: float,
    regime: str = "new",
    deductions: Optional[Dict[str, float]] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Calculate income tax
    
    Regimes: 'new', 'old', 'compare'
    """
    try:
        if regime == "new":
            result = tax_calculator.calculate_tax_new_regime(gross_income)
        elif regime == "old":
            if deductions is None:
                deductions = {}
            result = tax_calculator.calculate_tax_old_regime(gross_income, deductions)
        elif regime == "compare":
            if deductions is None:
                deductions = {}
            result = tax_calculator.compare_regimes(gross_income, deductions)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Regime must be 'new', 'old', or 'compare'"
            )
        
        return APIResponse(
            status="success",
            message="Tax calculated successfully",
            data=result
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating tax: {str(e)}"
        )


@router.get("/suggestions", response_model=APIResponse)
async def get_tax_suggestions(
    gross_income: float,
    current_user: User = Depends(get_current_user)
):
    """
    Get tax planning suggestions
    """
    try:
        suggestions = tax_calculator.tax_planning_suggestions(gross_income)
        
        return APIResponse(
            status="success",
            message="Tax planning suggestions generated",
            data={
                "suggestions": suggestions,
                "gross_income": gross_income
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating suggestions: {str(e)}"
        )


@router.get("/slabs", response_model=APIResponse)
async def get_tax_slabs():
    """
    Get current tax slabs for both regimes
    """
    return APIResponse(
        status="success",
        message="Tax slabs retrieved",
        data={
            "new_regime": [
                {"limit": "Up to ₹3,00,000", "rate": "0%"},
                {"limit": "₹3,00,001 to ₹7,00,000", "rate": "5%"},
                {"limit": "₹7,00,001 to ₹10,00,000", "rate": "10%"},
                {"limit": "₹10,00,001 to ₹12,00,000", "rate": "15%"},
                {"limit": "₹12,00,001 to ₹15,00,000", "rate": "20%"},
                {"limit": "Above ₹15,00,000", "rate": "30%"}
            ],
            "old_regime": [
                {"limit": "Up to ₹2,50,000", "rate": "0%"},
                {"limit": "₹2,50,001 to ₹5,00,000", "rate": "5%"},
                {"limit": "₹5,00,001 to ₹10,00,000", "rate": "20%"},
                {"limit": "Above ₹10,00,000", "rate": "30%"}
            ],
            "standard_deduction": "₹50,000",
            "cess": "4% on tax"
        }
    )
