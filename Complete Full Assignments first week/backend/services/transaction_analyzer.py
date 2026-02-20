"""
Transaction analysis service
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any, List
from datetime import datetime, timedelta


class TransactionAnalyzer:
    """Service for analyzing financial transactions"""
    
    @staticmethod
    def daily_summary(transactions_df: pd.DataFrame, date_col: str = 'transaction_date',
                      amount_col: str = 'amount') -> pd.DataFrame:
        """Generate daily transaction summary"""
        df = transactions_df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        
        summary = df.groupby(df[date_col].dt.date).agg({
            amount_col: ['sum', 'mean', 'count', 'std']
        }).reset_index()
        
        summary.columns = ['date', 'total_amount', 'avg_amount', 'transaction_count', 'std_amount']
        return summary
    
    @staticmethod
    def monthly_aggregation(transactions_df: pd.DataFrame, date_col: str = 'transaction_date',
                           amount_col: str = 'amount') -> pd.DataFrame:
        """Generate monthly transaction aggregation"""
        df = transactions_df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        
        df['year_month'] = df[date_col].dt.to_period('M')
        
        summary = df.groupby('year_month').agg({
            amount_col: ['sum', 'mean', 'count', 'min', 'max']
        }).reset_index()
        
        summary.columns = ['year_month', 'total', 'average', 'count', 'min', 'max']
        summary['year_month'] = summary['year_month'].astype(str)
        
        return summary
    
    @staticmethod
    def category_analysis(transactions_df: pd.DataFrame, category_col: str = 'category',
                         amount_col: str = 'amount') -> pd.DataFrame:
        """Analyze transactions by category"""
        if category_col not in transactions_df.columns:
            raise ValueError(f"Column '{category_col}' not found")
        
        analysis = transactions_df.groupby(category_col).agg({
            amount_col: ['sum', 'mean', 'count']
        }).reset_index()
        
        analysis.columns = ['category', 'total_amount', 'avg_amount', 'count']
        analysis = analysis.sort_values('total_amount', ascending=False)
        
        # Calculate percentage
        analysis['percentage'] = (analysis['total_amount'] / analysis['total_amount'].sum() * 100).round(2)
        
        return analysis
    
    @staticmethod
    def detect_fraud(transactions_df: pd.DataFrame, amount_col: str = 'amount',
                     contamination: float = 0.1) -> List[int]:
        """
        Detect suspicious transactions using Isolation Forest
        
        Returns list of suspicious transaction indices
        """
        if amount_col not in transactions_df.columns:
            raise ValueError(f"Column '{amount_col}' not found")
        
        # Prepare features
        X = transactions_df[amount_col].values.reshape(-1, 1)
        
        # Train Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso_forest.fit_predict(X)
        
        # Get suspicious transactions (outliers labeled as -1)
        suspicious_indices = np.where(predictions == -1)[0].tolist()
        
        return suspicious_indices
    
    @staticmethod
    def outlier_detection(transactions_df: pd.DataFrame, amount_col: str = 'amount',
                         method: str = 'iqr') -> Dict[str, Any]:
        """
        Detect outliers using statistical methods
        
        Methods: 'iqr' (Interquartile Range), 'zscore' (Z-Score)
        """
        if amount_col not in transactions_df.columns:
            raise ValueError(f"Column '{amount_col}' not found")
        
        data = transactions_df[amount_col].dropna()
        outliers = []
        
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = transactions_df[
                (transactions_df[amount_col] < lower_bound) | 
                (transactions_df[amount_col] > upper_bound)
            ].index.tolist()
            
            return {
                "method": "IQR",
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "outlier_count": len(outliers),
                "outlier_indices": outliers
            }
        
        elif method == 'zscore':
            mean = data.mean()
            std = data.std()
            z_scores = np.abs((data - mean) / std)
            
            outliers = transactions_df[z_scores > 3].index.tolist()
            
            return {
                "method": "Z-Score",
                "mean": float(mean),
                "std": float(std),
                "threshold": 3.0,
                "outlier_count": len(outliers),
                "outlier_indices": outliers
            }
        
        else:
            raise ValueError(f"Unknown method: {method}")
    
    @staticmethod
    def spending_trends(transactions_df: pd.DataFrame, date_col: str = 'transaction_date',
                       amount_col: str = 'amount', days: int = 30) -> Dict[str, Any]:
        """Analyze spending trends over specified days"""
        df = transactions_df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        
        # Filter recent transactions
        cutoff_date = df[date_col].max() - timedelta(days=days)
        recent_df = df[df[date_col] >= cutoff_date]
        
        # Calculate metrics
        total_spent = recent_df[amount_col].sum()
        avg_daily = total_spent / days
        avg_transaction = recent_df[amount_col].mean()
        transaction_count = len(recent_df)
        
        # Calculate trend (simple linear regression on daily totals)
        daily_totals = recent_df.groupby(recent_df[date_col].dt.date)[amount_col].sum()
        if len(daily_totals) > 1:
            x = np.arange(len(daily_totals))
            slope = np.polyfit(x, daily_totals.values, 1)[0]
            trend = "increasing" if slope > 0 else "decreasing"
        else:
            slope = 0
            trend = "stable"
        
        return {
            "period_days": days,
            "total_spent": float(total_spent),
            "avg_daily_spending": float(avg_daily),
            "avg_transaction_amount": float(avg_transaction),
            "transaction_count": transaction_count,
            "trend": trend,
            "trend_slope": float(slope)
        }
