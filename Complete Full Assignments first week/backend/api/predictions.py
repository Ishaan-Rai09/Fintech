"""
Predictions API endpoints
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.schemas.auth import APIResponse
from backend.services.data_service import DataService
from backend.ml.time_series import TimeSeriesForecaster

router = APIRouter(prefix="/predictions", tags=["Predictions"])

data_service = DataService()
forecaster = TimeSeriesForecaster()


@router.post("/forecast", response_model=APIResponse)
async def forecast_time_series(
    file: UploadFile = File(...),
    date_column: str = "date",
    value_column: str = "value",
    method: str = "auto",
    periods: int = 30,
    current_user: User = Depends(get_current_user)
):
    """
    Perform time series forecasting
    
    Methods: auto, linear, arima
    Use cases: car purchase forecast, loan repayment, house price prediction
    """
    try:
        # Load data
        content = await file.read()
        df = data_service.load_csv(content)
        
        if date_column not in df.columns or value_column not in df.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Columns '{date_column}' and '{value_column}' required"
            )
        
        # Prepare time series
        ts_data = forecaster.prepare_time_series(df, date_column, value_column)
        
        # Forecast based on method
        if method == "auto":
            result = forecaster.auto_forecast(ts_data, periods)
        elif method == "linear":
            result = forecaster.linear_forecast(ts_data, periods)
        elif method == "arima":
            result = forecaster.arima_forecast(ts_data, periods=periods)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown method: {method}"
            )
        
        # Add historical data
        result["historical_data"] = ts_data.tail(50).tolist()
        result["historical_dates"] = ts_data.tail(50).index.astype(str).tolist()
        
        return APIResponse(
            status="success",
            message=f"Forecast generated using {result['model']}",
            data=result
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error forecasting: {str(e)}"
        )


@router.post("/moving-average", response_model=APIResponse)
async def calculate_moving_average(
    file: UploadFile = File(...),
    date_column: str = "date",
    value_column: str = "value",
    window: int = 7,
    current_user: User = Depends(get_current_user)
):
    """
    Calculate moving average for time series
    """
    try:
        content = await file.read()
        df = data_service.load_csv(content)
        
        ts_data = forecaster.prepare_time_series(df, date_column, value_column)
        ma = forecaster.moving_average(ts_data, window)
        
        return APIResponse(
            status="success",
            message=f"{window}-period moving average calculated",
            data={
                "original": ts_data.tolist(),
                "moving_average": ma.dropna().tolist(),
                "window": window
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating moving average: {str(e)}"
        )
