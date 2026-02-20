"""
Transaction API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.models.transaction import Transaction
from backend.schemas.auth import APIResponse
from backend.services.transaction_analyzer import TransactionAnalyzer
from backend.services.data_service import DataService
from datetime import datetime, date
from typing import Optional

router = APIRouter(prefix="/transactions", tags=["Transactions"])

analyzer = TransactionAnalyzer()
data_service = DataService()


@router.get("/summary", response_model=APIResponse)
async def get_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get transaction summary for user
    """
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    transactions = query.all()
    
    if not transactions:
        return APIResponse(
            status="success",
            message="No transactions found",
            data={"count": 0}
        )
    
    # Convert to DataFrame for analysis
    import pandas as pd
    df = pd.DataFrame([{
        'transaction_date': t.transaction_date,
        'amount': float(t.amount),
        'category': t.category,
        'description': t.description
    } for t in transactions])
    
    # Generate summaries
    daily = analyzer.daily_summary(df)
    monthly = analyzer.monthly_aggregation(df)
    trends = analyzer.spending_trends(df)
    
    return APIResponse(
        status="success",
        message="Transaction summary generated",
        data={
            "total_transactions": len(transactions),
            "daily_summary": daily.to_dict('records')[:10],  # Last 10 days
            "monthly_summary": monthly.to_dict('records'),
            "trends": trends
        }
    )


@router.post("/analyze", response_model=APIResponse)
async def analyze_transactions(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze uploaded transaction file
    """
    try:
        content = await file.read()
        df = data_service.load_csv(content)
        
        # Perform various analyses
        daily = analyzer.daily_summary(df)
        monthly = analyzer.monthly_aggregation(df)
        
        category_analysis = None
        if 'category' in df.columns:
            category_analysis = analyzer.category_analysis(df)
        
        trends = analyzer.spending_trends(df)
        
        return APIResponse(
            status="success",
            message="Transaction analysis complete",
            data={
                "daily_summary": daily.to_dict('records')[:10],
                "monthly_summary": monthly.to_dict('records'),
                "category_analysis": category_analysis.to_dict('records') if category_analysis is not None else None,
                "trends": trends
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing transactions: {str(e)}"
        )


@router.post("/detect-fraud", response_model=APIResponse)
async def detect_fraud(
    file: UploadFile = File(...),
    contamination: float = 0.1,
    current_user: User = Depends(get_current_user)
):
    """
    Detect suspicious transactions using ML
    """
    try:
        content = await file.read()
        df = data_service.load_csv(content)
        
        if 'amount' not in df.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'amount' column required in data"
            )
        
        # Detect fraud
        suspicious_indices = analyzer.detect_fraud(df, contamination=contamination)
        
        # Get outliers
        outliers_iqr = analyzer.outlier_detection(df, method='iqr')
        outliers_zscore = analyzer.outlier_detection(df, method='zscore')
        
        # Get suspicious transactions
        suspicious_transactions = df.iloc[suspicious_indices].to_dict('records')
        
        return APIResponse(
            status="success",
            message=f"Found {len(suspicious_indices)} suspicious transactions",
            data={
                "ml_detection": {
                    "suspicious_count": len(suspicious_indices),
                    "suspicious_transactions": suspicious_transactions[:20]  # Limit to 20
                },
                "iqr_outliers": outliers_iqr,
                "zscore_outliers": outliers_zscore
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting fraud: {str(e)}"
        )


@router.get("/suspicious", response_model=APIResponse)
async def get_suspicious_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get flagged suspicious transactions for user
    """
    suspicious = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_suspicious == True
    ).all()
    
    return APIResponse(
        status="success",
        message=f"Found {len(suspicious)} suspicious transactions",
        data={
            "count": len(suspicious),
            "transactions": [{
                "id": t.id,
                "date": str(t.transaction_date),
                "amount": float(t.amount),
                "description": t.description,
                "category": t.category
            } for t in suspicious]
        }
    )
