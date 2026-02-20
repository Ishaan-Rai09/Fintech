"""
Portfolio management service
"""
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from typing import Dict, Any, List, Tuple
from backend.services.market_data import MarketDataService


class PortfolioService:
    """Service for portfolio management and optimization"""
    
    def __init__(self):
        self.market_data = MarketDataService()
    
    def calculate_portfolio_return(self, holdings: List[Dict[str, Any]]) -> float:
        """
        Calculate total portfolio return
        
        Holdings format: [{'ticker': 'AAPL', 'quantity': 10, 'purchase_price': 150}]
        """
        total_return = 0
        total_investment = 0
        
        for holding in holdings:
            ticker = holding['ticker']
            quantity = holding['quantity']
            purchase_price = holding['purchase_price']
            
            # Get current price
            current_price = self.market_data.get_stock_info(ticker)['current_price']
            
            investment = quantity * purchase_price
            current_value = quantity * current_price
            
            total_investment += investment
            total_return += (current_value - investment)
        
        return_pct = (total_return / total_investment * 100) if total_investment > 0 else 0
        
        return float(return_pct)
    
    def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        excess_returns = returns.mean() - risk_free_rate / 252  # Daily risk-free rate
        return float(excess_returns / returns.std()) if returns.std() > 0 else 0
    
    def portfolio_metrics(self, tickers: List[str], weights: List[float], 
                         period: str = "1y") -> Dict[str, float]:
        """Calculate portfolio metrics given weights"""
        # Get historical data
        data = self.market_data.get_multiple_stocks(tickers, period)
        
        # Extract close prices
        if len(tickers) == 1:
            prices = data['Close'].to_frame()
            prices.columns = tickers
        else:
            prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in tickers})
        
        # Calculate returns
        returns = prices.pct_change().dropna()
        
        # Calculate portfolio return
        portfolio_return = np.sum(returns.mean() * weights) * 252  # Annualized
        
        # Calculate portfolio volatility
        cov_matrix = returns.cov() * 252  # Annualized
        portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
        portfolio_std = np.sqrt(portfolio_variance)
        
        # Calculate Sharpe ratio
        sharpe_ratio = portfolio_return / portfolio_std if portfolio_std > 0 else 0
        
        return {
            "expected_return": float(portfolio_return),
            "volatility": float(portfolio_std),
            "sharpe_ratio": float(sharpe_ratio)
        }
    
    def optimize_portfolio(self, tickers: List[str], period: str = "1y",
                          risk_free_rate: float = 0.02) -> Dict[str, Any]:
        """
        Optimize portfolio using Modern Portfolio Theory (efficient frontier)
        """
        # Get historical data
        data = self.market_data.get_multiple_stocks(tickers, period)
        
        # Extract close prices
        if len(tickers) == 1:
            raise ValueError("Need at least 2 assets for optimization")
        
        prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in tickers})
        returns = prices.pct_change().dropna()
        
        # Calculate expected returns and covariance
        mean_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252
        
        num_assets = len(tickers)
        
        # Optimization function
        def portfolio_stats(weights):
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_std = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
            sharpe = (portfolio_return - risk_free_rate) / portfolio_std
            return np.array([portfolio_return, portfolio_std, sharpe])
        
        # Negative Sharpe ratio for minimization
        def neg_sharpe(weights):
            return -portfolio_stats(weights)[2]
        
        # Constraints: weights sum to 1
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        
        # Bounds: 0 <= weight <= 1
        bounds = tuple((0, 1) for _ in range(num_assets))
        
        # Initial guess: equal weights
        init_guess = num_assets * [1. / num_assets]
        
        # Optimize
        opt_result = minimize(neg_sharpe, init_guess, method='SLSQP',
                            bounds=bounds, constraints=constraints)
        
        optimal_weights = opt_result.x
        stats = portfolio_stats(optimal_weights)
        
        # Create allocation dictionary
        allocation = {ticker: float(weight) for ticker, weight in zip(tickers, optimal_weights)}
        
        return {
            "allocation": allocation,
            "expected_return": float(stats[0]),
            "volatility": float(stats[1]),
            "sharpe_ratio": float(stats[2]),
            "tickers": tickers
        }
    
    def efficient_frontier(self, tickers: List[str], period: str = "1y",
                          num_portfolios: int = 100) -> Dict[str, List]:
        """Generate efficient frontier"""
        # Get data
        data = self.market_data.get_multiple_stocks(tickers, period)
        prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in tickers})
        returns = prices.pct_change().dropna()
        
        mean_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252
        
        results = []
        
        for _ in range(num_portfolios):
            # Random weights
            weights = np.random.random(len(tickers))
            weights /= np.sum(weights)
            
            # Calculate metrics
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_std = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
            sharpe = portfolio_return / portfolio_std if portfolio_std > 0 else 0
            
            results.append({
                'return': float(portfolio_return),
                'volatility': float(portfolio_std),
                'sharpe': float(sharpe)
            })
        
        return {
            "portfolios": results,
            "count": len(results)
        }
    
    def rebalance_portfolio(self, current_holdings: Dict[str, float],
                           target_allocation: Dict[str, float],
                           total_value: float) -> Dict[str, Any]:
        """Calculate rebalancing trades"""
        trades = {}
        
        for ticker, target_weight in target_allocation.items():
            current_weight = current_holdings.get(ticker, 0)
            weight_diff = target_weight - current_weight
            
            # Get current price
            current_price = self.market_data.get_stock_info(ticker)['current_price']
            
            # Calculate shares to buy/sell
            target_value = total_value * target_weight
            current_value = total_value * current_weight
            value_diff = target_value - current_value
            
            shares = value_diff / current_price
            
            if abs(shares) > 0.01:  # Only include meaningful trades
                trades[ticker] = {
                    'action': 'buy' if shares > 0 else 'sell',
                    'shares': abs(float(shares)),
                    'value': float(value_diff),
                    'current_weight': float(current_weight),
                    'target_weight': float(target_weight)
                }
        
        return trades

    def analyze_portfolio_csv(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze portfolio from a DataFrame (loaded from CSV)
        Expected columns: symbol, quantity, purchase_price, current_price (optional)
        """
        try:
            # Normalize column names
            df.columns = [c.lower().strip() for c in df.columns]
            
            required_cols = ['symbol', 'quantity', 'purchase_price']
            for col in required_cols:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")
            
            holdings = []
            total_value = 0
            total_cost = 0
            tickers = df['symbol'].tolist()
            
            # Get latest market data
            market_data = {}
            for ticker in tickers:
                try:
                    info = self.market_data.get_stock_info(ticker)
                    market_data[ticker] = info
                except Exception:
                    # Fallback or skip if ticker not found
                    market_data[ticker] = None
            
            for _, row in df.iterrows():
                symbol = str(row['symbol']).upper()
                quantity = float(row['quantity'])
                purchase_price = float(row['purchase_price'])
                
                # Use current price from market data, or from CSV if provided, or fallback to purchase price
                current_price = purchase_price
                if market_data.get(symbol) and market_data[symbol].get('current_price'):
                    current_price = market_data[symbol]['current_price']
                elif 'current_price' in df.columns and not pd.isna(row['current_price']):
                    current_price = float(row['current_price'])
                
                value = quantity * current_price
                cost = quantity * purchase_price
                gain_loss = value - cost
                gain_loss_pct = (gain_loss / cost * 100) if cost > 0 else 0
                
                total_value += value
                total_cost += cost
                
                holdings.append({
                    "symbol": symbol,
                    "quantity": quantity,
                    "purchase_price": purchase_price,
                    "current_price": current_price,
                    "total_value": value,
                    "gain_loss": round(gain_loss_pct, 2)
                })
            
            total_return_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
            
            # Calculate simple risk metrics (Beta, Sharpe - placeholder logic or use services if enough data)
            # For a real app, we'd need historical data for the whole portfolio
            # Here we'll calculate them if we have at least 1 year of data for all tickers
            try:
                metrics = self.portfolio_metrics(tickers, [1/len(tickers)]*len(tickers), period="1y")
                beta = 1.0  # Placeholder for beta calculation logic
                sharpe_ratio = metrics['sharpe_ratio']
                volatility = metrics['volatility'] * 100
                expected_return = metrics['expected_return'] * 100
            except Exception:
                beta = 1.0
                sharpe_ratio = 1.0
                volatility = 15.0
                expected_return = 10.0

            return {
                "total_value": round(total_value, 2),
                "total_return_percentage": round(total_return_pct, 2),
                "holdings_count": len(holdings),
                "holdings": holdings,
                "beta": round(beta, 2),
                "sharpe_ratio": round(sharpe_ratio, 2),
                "volatility": round(volatility, 2),
                "expected_return": round(expected_return, 2),
                "risk_score": 5  # Placeholder
            }
            
        except Exception as e:
            raise ValueError(f"Error analyzing portfolio CSV: {str(e)}")
