"""
Time series forecasting module
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from typing import Dict, Any, Tuple


class TimeSeriesForecaster:
    """Time series forecasting service"""
    
    @staticmethod
    def prepare_time_series(df: pd.DataFrame, date_col: str, value_col: str) -> pd.Series:
        """Prepare time series data"""
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        df = df.set_index(date_col)
        return df[value_col]
    
    @staticmethod
    def linear_forecast(data: pd.Series, periods: int = 30) -> Dict[str, Any]:
        """
        Simple linear regression forecast
        """
        # Prepare data
        X = np.arange(len(data)).reshape(-1, 1)
        y = data.values
        
        # Fit model
        model = LinearRegression()
        model.fit(X, y)
        
        # Forecast
        future_X = np.arange(len(data), len(data) + periods).reshape(-1, 1)
        forecast = model.predict(future_X)
        
        # Calculate trend
        slope = model.coef_[0]
        trend = "increasing" if slope > 0 else "decreasing"
        
        return {
            "model": "linear_regression",
            "forecast": forecast.tolist(),
            "trend": trend,
            "slope": float(slope),
            "intercept": float(model.intercept_),
            "periods": periods
        }
    
    @staticmethod
    def arima_forecast(data: pd.Series, order: Tuple[int, int, int] = (1, 1, 1),
                       periods: int = 30) -> Dict[str, Any]:
        """
        ARIMA forecast
        
        Args:
            order: (p, d, q) ARIMA parameters
            periods: Number of periods to forecast
        """
        try:
            # Fit ARIMA model
            model = ARIMA(data, order=order)
            fitted_model = model.fit()
            
            # Forecast
            forecast = fitted_model.forecast(steps=periods)
            
            # Get confidence intervals
            forecast_obj = fitted_model.get_forecast(steps=periods)
            conf_int = forecast_obj.conf_int()
            
            return {
                "model": "arima",
                "order": order,
                "forecast": forecast.tolist(),
                "confidence_interval": {
                    "lower": conf_int.iloc[:, 0].tolist(),
                    "upper": conf_int.iloc[:, 1].tolist()
                },
                "aic": float(fitted_model.aic),
                "bic": float(fitted_model.bic),
                "periods": periods
            }
        
        except Exception as e:
            raise ValueError(f"ARIMA forecast failed: {str(e)}")
    
    @staticmethod
    def moving_average(data: pd.Series, window: int = 7) -> pd.Series:
        """Calculate moving average"""
        return data.rolling(window=window).mean()
    
    @staticmethod
    def exponential_smoothing(data: pd.Series, alpha: float = 0.3) -> pd.Series:
        """Simple exponential smoothing"""
        return data.ewm(alpha=alpha, adjust=False).mean()
    
    @staticmethod
    def seasonal_decomposition(data: pd.Series, period: int = 12) -> Dict[str, Any]:
        """Decompose time series into trend, seasonal, and residual components"""
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        try:
            decomposition = seasonal_decompose(data, model='additive', period=period)
            
            return {
                "trend": decomposition.trend.dropna().tolist(),
                "seasonal": decomposition.seasonal.dropna().tolist(),
                "residual": decomposition.resid.dropna().tolist()
            }
        except Exception as e:
            raise ValueError(f"Seasonal decomposition failed: {str(e)}")
    
    @staticmethod
    def auto_forecast(data: pd.Series, periods: int = 30) -> Dict[str, Any]:
        """
        Automatic forecast - tries multiple methods and returns best
        """
        results = {}
        
        # Try linear forecast
        try:
            results['linear'] = TimeSeriesForecaster.linear_forecast(data, periods)
        except:
            pass
        
        # Try ARIMA with different orders
        for order in [(1, 1, 1), (2, 1, 2), (1, 0, 1)]:
            try:
                arima_result = TimeSeriesForecaster.arima_forecast(data, order, periods)
                if 'arima' not in results or arima_result['aic'] < results['arima']['aic']:
                    results['arima'] = arima_result
            except:
                continue
        
        # Return best model (lowest AIC for ARIMA, or linear if ARIMA failed)
        if 'arima' in results:
            return results['arima']
        elif 'linear' in results:
            return results['linear']
        else:
            raise ValueError("All forecasting methods failed")
