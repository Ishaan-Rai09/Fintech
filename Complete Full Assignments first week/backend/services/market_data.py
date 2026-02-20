"""
Market data service using YFinance
"""
import yfinance as yf
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class MarketDataService:
    """Service for fetching stock market data"""
    
    @staticmethod
    def get_stock_info(ticker: str) -> Dict[str, Any]:
        """Get comprehensive stock information"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "ticker": ticker,
                "name": info.get('longName', ''),
                "sector": info.get('sector', ''),
                "industry": info.get('industry', ''),
                "current_price": info.get('currentPrice'),
                "market_cap": info.get('marketCap'),
                "pe_ratio": info.get('trailingPE'),
                "dividend_yield": info.get('dividendYield'),
                "52_week_high": info.get('fiftyTwoWeekHigh'),
                "52_week_low": info.get('fiftyTwoWeekLow')
            }
        except Exception as e:
            raise ValueError(f"Error fetching stock info for {ticker}: {str(e)}")
    
    @staticmethod
    def get_historical_data(ticker: str, period: str = "1y", 
                           interval: str = "1d") -> pd.DataFrame:
        """
        Get historical price data
        
        Periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        Intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            return df
        except Exception as e:
            raise ValueError(f"Error fetching historical data for {ticker}: {str(e)}")
    
    @staticmethod
    def get_multiple_stocks(tickers: List[str], period: str = "1y") -> pd.DataFrame:
        """Get historical data for multiple stocks"""
        try:
            data = yf.download(tickers, period=period, group_by='ticker')
            return data
        except Exception as e:
            raise ValueError(f"Error fetching multiple stocks: {str(e)}")
    
    @staticmethod
    def get_dividends(ticker: str) -> pd.DataFrame:
        """Get dividend history"""
        try:
            stock = yf.Ticker(ticker)
            return stock.dividends
        except Exception as e:
            raise ValueError(f"Error fetching dividends for {ticker}: {str(e)}")
    
    @staticmethod
    def get_financials(ticker: str) -> Dict[str, pd.DataFrame]:
        """Get financial statements"""
        try:
            stock = yf.Ticker(ticker)
            return {
                "income_statement": stock.financials,
                "balance_sheet": stock.balance_sheet,
                "cash_flow": stock.cashflow
            }
        except Exception as e:
            raise ValueError(f"Error fetching financials for {ticker}: {str(e)}")
    
    @staticmethod
    def get_recommendations(ticker: str) -> pd.DataFrame:
        """Get analyst recommendations"""
        try:
            stock = yf.Ticker(ticker)
            return stock.recommendations
        except Exception as e:
            return pd.DataFrame()
    
    @staticmethod
    def calculate_returns(ticker: str, period: str = "1y") -> Dict[str, float]:
        """Calculate various return metrics"""
        try:
            df = MarketDataService.get_historical_data(ticker, period)
            
            if df.empty:
                raise ValueError("No data available")
            
            # Calculate returns
            start_price = df['Close'].iloc[0]
            end_price = df['Close'].iloc[-1]
            total_return = ((end_price - start_price) / start_price) * 100
            
            # Daily returns
            daily_returns = df['Close'].pct_change().dropna()
            avg_daily_return = daily_returns.mean() * 100
            volatility = daily_returns.std() * 100
            
            return {
                "total_return_pct": float(total_return),
                "avg_daily_return_pct": float(avg_daily_return),
                "volatility_pct": float(volatility),
                "sharpe_ratio": float(avg_daily_return / volatility) if volatility > 0 else 0,
                "period": period
            }
        except Exception as e:
            raise ValueError(f"Error calculating returns for {ticker}: {str(e)}")
