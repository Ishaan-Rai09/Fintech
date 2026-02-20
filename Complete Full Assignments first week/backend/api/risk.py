"""
Risk Management API endpoints
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.schemas.auth import APIResponse
from backend.services.var_calculator import VaRCalculator
from backend.services.data_service import DataService
from typing import List
import pandas as pd

router = APIRouter(prefix="/risk", tags=["Risk Management"])

var_calculator = VaRCalculator()
data_service = DataService()


@router.post("/var", response_model=APIResponse)
async def calculate_var(
    file: UploadFile = File(...),
    returns_column: str = "returns",
    confidence_level: float = 0.95,
    portfolio_value: float = 100000,
    current_user: User = Depends(get_current_user)
):
    """
    Calculate Value at Risk using all methods
    """
    try:
        content = await file.read()
        df = data_service.load_csv(content)
        
        if returns_column not in df.columns:
            # Calculate returns from prices if 'Close' column exists
            if 'Close' in df.columns:
                returns = df['Close'].pct_change().dropna()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Column '{returns_column}' not found and no 'Close' column to calculate returns"
                )
        else:
            returns = df[returns_column].dropna()
        
        var_results = var_calculator.calculate_all_methods(returns, confidence_level, portfolio_value)
        
        # Add expected shortfall
        es = var_calculator.expected_shortfall(returns, confidence_level)
        var_results["expected_shortfall"] = {
            "es_pct": float(es * 100),
            "es_dollar": float(es * portfolio_value),
            "description": "Average loss beyond VaR threshold"
        }
        
        return APIResponse(
            status="success",
            message="VaR calculated successfully",
            data=var_results
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating VaR: {str(e)}"
        )


@router.post("/dual-stock-var", response_model=APIResponse)
async def dual_stock_var(
    ticker1: str,
    ticker2: str,
    weight1: float,
    weight2: float,
    confidence_level: float = 0.95,
    portfolio_value: float = 100000,
    period: str = "1y",
    current_user: User = Depends(get_current_user)
):
    """
    Calculate VaR for a two-stock portfolio (Capstone feature)
    """
    try:
        if abs(weight1 + weight2 - 1.0) > 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Weights must sum to 1.0"
            )
        
        result = var_calculator.dual_stock_var(
            ticker1, ticker2, [weight1, weight2],
            confidence_level, period, portfolio_value
        )
        
        return APIResponse(
            status="success",
            message="Dual stock VaR calculated",
            data=result
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating dual stock VaR: {str(e)}"
        )


@router.post("/monte-carlo", response_model=APIResponse)
async def monte_carlo_simulation(
    file: UploadFile = File(...),
    returns_column: str = "returns",
    confidence_level: float = 0.95,
    num_simulations: int = 10000,
    current_user: User = Depends(get_current_user)
):
    """
    Run Monte Carlo simulation for VaR
    """
    try:
        content = await file.read()
        df = data_service.load_csv(content)
        
        if returns_column not in df.columns:
            if 'Close' in df.columns:
                returns = df['Close'].pct_change().dropna()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Column '{returns_column}' not found"
                )
        else:
            returns = df[returns_column].dropna()
        
        result = var_calculator.monte_carlo_var(returns, confidence_level, num_simulations)
        
        return APIResponse(
            status="success",
            message=f"Monte Carlo simulation completed ({num_simulations} runs)",
            data=result
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running Monte Carlo simulation: {str(e)}"
        )


@router.get("/report", response_model=APIResponse)
async def generate_risk_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate comprehensive risk report for user's portfolios
    """
    # This would pull data from user's portfolios in the database
    return APIResponse(
        status="success",
        message="Risk report generated",
        data={
            "summary": "Comprehensive risk analysis",
            "portfolios": []
        }
    )
