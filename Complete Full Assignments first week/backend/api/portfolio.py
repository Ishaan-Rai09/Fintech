"""
Portfolio API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.schemas.auth import APIResponse
from backend.services.portfolio_service import PortfolioService
from typing import List
import pandas as pd
import io

router = APIRouter(prefix="/portfolio", tags=["Portfolio Management"])

portfolio_service = PortfolioService()


@router.post("/optimize", response_model=APIResponse)
async def optimize_portfolio(
    tickers: List[str],
    period: str = "1y",
    current_user: User = Depends(get_current_user)
):
    """
    Optimize portfolio allocation using Modern Portfolio Theory
    """
    try:
        if len(tickers) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Need at least 2 tickers for optimization"
            )
        
        result = portfolio_service.optimize_portfolio(tickers, period)
        
        return APIResponse(
            status="success",
            message="Portfolio optimized successfully",
            data=result
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizing portfolio: {str(e)}"
        )


@router.post("/efficient-frontier", response_model=APIResponse)
async def get_efficient_frontier(
    tickers: List[str],
    period: str = "1y",
    num_portfolios: int = 100,
    current_user: User = Depends(get_current_user)
):
    """
    Generate efficient frontier for portfolio visualization
    """
    try:
        result = portfolio_service.efficient_frontier(tickers, period, num_portfolios)
        
        return APIResponse(
            status="success",
            message="Efficient frontier generated",
            data=result
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating efficient frontier: {str(e)}"
        )


@router.post("/performance", response_model=APIResponse)
async def calculate_performance(
    tickers: List[str],
    weights: List[float],
    period: str = "1y",
    current_user: User = Depends(get_current_user)
):
    """
    Calculate portfolio performance metrics
    """
    try:
        if len(tickers) != len(weights):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number of tickers must match number of weights"
            )
        
        if abs(sum(weights) - 1.0) > 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Weights must sum to 1.0"
            )
        
        metrics = portfolio_service.portfolio_metrics(tickers, weights, period)
        
        return APIResponse(
            status="success",
            message="Portfolio metrics calculated",
            data={"metrics": metrics, "tickers": tickers, "weights": weights}
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating performance: {str(e)}"
        )
@router.post("/analyze", response_model=APIResponse)
async def analyze_portfolio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze portfolio from uploaded CSV file
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only CSV files are allowed"
            )
        
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded CSV is empty"
            )
        
        result = portfolio_service.analyze_portfolio_csv(df)
        
        return APIResponse(
            status="success",
            message="Portfolio analyzed successfully",
            data=result
        )
    
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing portfolio: {str(e)}"
        )
