import numpy as np
import pandas as pd
from scipy.optimize import minimize

class ClientEngine:
    """Manages client profiles and risk assessment."""
    def __init__(self):
        self.risk_profiles = {
            "Conservative": {"equity": 0.2, "bonds": 0.7, "cash": 0.1},
            "Moderate": {"equity": 0.5, "bonds": 0.4, "cash": 0.1},
            "Aggressive": {"equity": 0.8, "bonds": 0.15, "cash": 0.05}
        }

    def calculate_risk_score(self, answers):
        """Simple scoring logic based on questionnaire answers."""
        # Answers is a list of integers 1-5
        score = sum(answers) / len(answers)
        if score <= 2: return "Conservative"
        if score <= 4: return "Moderate"
        return "Aggressive"

    def get_target_allocation(self, profile):
        return self.risk_profiles.get(profile, self.risk_profiles["Moderate"])

class ConstructionAlgorithm:
    """Handles asset allocation using MVO principles."""
    def optimize_portfolio(self, returns_df, target_risk=None):
        """
        Simplified Markowitz Optimization.
        In a real app, this would use covariance matrices and historical returns.
        """
        num_assets = len(returns_df.columns)
        args = (returns_df.mean(), returns_df.cov())
        
        def portfolio_variance(weights, mean_returns, cov_matrix):
            return np.dot(weights.T, np.dot(cov_matrix, weights))

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(num_assets))
        initial_guess = num_assets * [1. / num_assets]
        
        optimized = minimize(portfolio_variance, initial_guess, args=args,
                             method='SLSQP', bounds=bounds, constraints=constraints)
        
        return dict(zip(returns_df.columns, optimized.x))

class RebalancingSystem:
    """Detects portfolio drift and generates rebalancing orders."""
    def __init__(self, drift_threshold=0.05):
        self.drift_threshold = drift_threshold

    def check_drift(self, current_alloc, target_alloc):
        """Returns True if any asset has drifted beyond threshold."""
        drifts = {}
        needs_rebalance = False
        for asset, target in target_alloc.items():
            current = current_alloc.get(asset, 0)
            drift = abs(current - target)
            drifts[asset] = drift
            if drift > self.drift_threshold:
                needs_rebalance = True
        return needs_rebalance, drifts

    def generate_orders(self, current_values, target_alloc, total_value):
        """Calculates trades to move from current to target."""
        orders = []
        for asset, target_pct in target_alloc.items():
            target_value = total_value * target_pct
            current_value = current_values.get(asset, 0)
            diff = target_value - current_value
            if abs(diff) > 1: # Minimum trade size $1
                orders.append({
                    "asset": asset,
                    "action": "BUY" if diff > 0 else "SELL",
                    "amount": abs(diff)
                })
        return orders

class TaxOptimizer:
    """Implements Tax-Loss Harvesting (TLH) logic."""
    def __init__(self, loss_threshold=0.1):
        self.loss_threshold = loss_threshold

    def identify_harvesting_opportunities(self, holdings):
        """
        Expects holdings as list of dicts: 
        {'symbol': 'AAPL', 'cost_basis': 150, 'current_price': 130}
        """
        opportunities = []
        for item in holdings:
            loss_pct = (item['cost_basis'] - item['current_price']) / item['cost_basis']
            if loss_pct >= self.loss_threshold:
                opportunities.append({
                    "symbol": item['symbol'],
                    "loss_amount": item['cost_basis'] - item['current_price'],
                    "replacement_candidate": self._get_replacement(item['symbol'])
                })
        return opportunities

    def _get_replacement(self, symbol):
        """Returns a correlated but not identical asset (to avoid wash sales)."""
        replacements = {
            "SPY": "IVV",
            "VOO": "SPY",
            "VTI": "SCHB",
            "QQQ": "VGT"
        }
        return replacements.get(symbol, "Direct Indexing / Cash")
