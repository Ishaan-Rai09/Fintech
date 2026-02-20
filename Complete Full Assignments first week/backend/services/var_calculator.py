"""
Value at Risk (VaR) calculator
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from scipy import stats


class VaRCalculator:
    """Service for calculating Value at Risk using multiple methods"""
    
    @staticmethod
    def historical_simulation(returns: pd.Series, confidence_level: float = 0.95) -> float:
        """
        Calculate VaR using historical simulation method
        """
        var_percentile = (1 - confidence_level) * 100
        var = np.percentile(returns, var_percentile)
        return float(var)
    
    @staticmethod
    def parametric_var(returns: pd.Series, confidence_level: float = 0.95) -> float:
        """
        Calculate VaR using variance-covariance (parametric) method
        Assumes normal distribution
        """
        mean = returns.mean()
        std = returns.std()
        
        # Z-score for confidence level
        z_score = stats.norm.ppf(1 - confidence_level)
        
        var = mean + z_score * std
        return float(var)
    
    @staticmethod
    def monte_carlo_var(returns: pd.Series, confidence_level: float = 0.95,
                       num_simulations: int = 10000) -> Dict[str, Any]:
        """
        Calculate VaR using Monte Carlo simulation
        """
        mean = returns.mean()
        std = returns.std()
        
        # Generate random returns
        simulated_returns = np.random.normal(mean, std, num_simulations)
        
        # Calculate VaR
        var_percentile = (1 - confidence_level) * 100
        var = np.percentile(simulated_returns, var_percentile)
        
        return {
            "var": float(var),
            "mean": float(mean),
            "std": float(std),
            "simulations": num_simulations,
            "simulated_returns": simulated_returns[:1000].tolist()  # Return first 1000
        }
    
    @staticmethod
    def calculate_all_methods(returns: pd.Series, confidence_level: float = 0.95,
                             portfolio_value: float = 100000) -> Dict[str, Any]:
        """
        Calculate VaR using all three methods and compare
        """
        # Historical
        hist_var = VaRCalculator.historical_simulation(returns, confidence_level)
        hist_var_dollar = hist_var * portfolio_value
        
        # Parametric
        param_var = VaRCalculator.parametric_var(returns, confidence_level)
        param_var_dollar = param_var * portfolio_value
        
        # Monte Carlo
        mc_result = VaRCalculator.monte_carlo_var(returns, confidence_level)
        mc_var = mc_result["var"]
        mc_var_dollar = mc_var * portfolio_value
        
        return {
            "confidence_level": confidence_level,
            "portfolio_value": portfolio_value,
            "historical_simulation": {
                "var_pct": float(hist_var * 100),
                "var_dollar": float(hist_var_dollar),
                "description": "Based on actual historical returns distribution"
            },
            "parametric": {
                "var_pct": float(param_var * 100),
                "var_dollar": float(param_var_dollar),
                "description": "Assumes normal distribution of returns"
            },
            "monte_carlo": {
                "var_pct": float(mc_var * 100),
                "var_dollar": float(mc_var_dollar),
                "simulations": mc_result["simulations"],
                "description": "Based on simulated random scenarios"
            }
        }
    
    @staticmethod
    def expected_shortfall(returns: pd.Series, confidence_level: float = 0.95) -> float:
        """
        Calculate Expected Shortfall (Conditional VaR)
        Average loss beyond VaR
        """
        var = VaRCalculator.historical_simulation(returns, confidence_level)
        
        # Get returns worse than VaR
        tail_returns = returns[returns <= var]
        
        if len(tail_returns) == 0:
            return var
        
        es = tail_returns.mean()
        return float(es)
    
    @staticmethod
    def dual_stock_var(ticker1: str, ticker2: str, weights: List[float],
                      confidence_level: float = 0.95, period: str = "1y",
                      portfolio_value: float = 100000) -> Dict[str, Any]:
        """
        Calculate VaR for a two-stock portfolio
        """
        from backend.services.market_data import MarketDataService
        
        market_data = MarketDataService()
        
        # Get historical data
        data = market_data.get_multiple_stocks([ticker1, ticker2], period)
        
        # Calculate returns
        prices1 = data[ticker1]['Close']
        prices2 = data[ticker2]['Close']
        
        returns1 = prices1.pct_change().dropna()
        returns2 = prices2.pct_change().dropna()
        
        # Portfolio returns
        portfolio_returns = weights[0] * returns1 + weights[1] * returns2
        
        # Calculate VaR using all methods
        var_results = VaRCalculator.calculate_all_methods(
            portfolio_returns, confidence_level, portfolio_value
        )
        
        # Add expected shortfall
        es = VaRCalculator.expected_shortfall(portfolio_returns, confidence_level)
        
        var_results["expected_shortfall"] = {
            "es_pct": float(es * 100),
            "es_dollar": float(es * portfolio_value)
        }
        
        var_results["portfolio_info"] = {
            "tickers": [ticker1, ticker2],
            "weights": weights,
            "correlation": float(returns1.corr(returns2))
        }
        
        return var_results
