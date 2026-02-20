import pytest
import pandas as pd
import numpy as np
from engine import ClientEngine, ConstructionAlgorithm, RebalancingSystem, TaxOptimizer

@pytest.fixture
def client_engine():
    return ClientEngine()

@pytest.fixture
def rebalancer():
    return RebalancingSystem(drift_threshold=0.05)

@pytest.fixture
def tax_opt():
    return TaxOptimizer(loss_threshold=0.1)

def test_risk_scoring(client_engine):
    # Moderate scenario
    assert client_engine.calculate_risk_score([3, 3, 3]) == "Moderate"
    # Conservative scenario
    assert client_engine.calculate_risk_score([1, 1, 2]) == "Conservative"
    # Aggressive scenario
    assert client_engine.calculate_risk_score([5, 5, 4]) == "Aggressive"

def test_target_allocation(client_engine):
    alloc = client_engine.get_target_allocation("Aggressive")
    assert alloc["equity"] == 0.8
    assert sum(alloc.values()) == pytest.approx(1.0)

def test_drift_detection(rebalancer):
    target = {"equity": 0.5, "bonds": 0.5}
    # No drift
    current_no_drift = {"equity": 0.52, "bonds": 0.48}
    needs_rebalance, _ = rebalancer.check_drift(current_no_drift, target)
    assert needs_rebalance is False
    
    # Significant drift
    current_drift = {"equity": 0.60, "bonds": 0.40}
    needs_rebalance, _ = rebalancer.check_drift(current_drift, target)
    assert needs_rebalance is True

def test_rebalancing_orders(rebalancer):
    target = {"equity": 0.5, "bonds": 0.5}
    current_vals = {"equity": 600, "bonds": 400}
    total_val = 1000
    orders = rebalancer.generate_orders(current_vals, target, total_val)
    
    # Should sell $100 equity, buy $100 bonds
    equity_order = next(o for o in orders if o['asset'] == 'equity')
    bond_order = next(o for o in orders if o['asset'] == 'bonds')
    
    assert equity_order['action'] == "SELL"
    assert equity_order['amount'] == 100
    assert bond_order['action'] == "BUY"
    assert bond_order['amount'] == 100

def test_tax_harvesting(tax_opt):
    holdings = [
        {'symbol': 'SPY', 'cost_basis': 100, 'current_price': 85}, # 15% loss > 10% threshold
        {'symbol': 'VTI', 'cost_basis': 100, 'current_price': 95}  # 5% loss < 10% threshold
    ]
    opps = tax_opt.identify_harvesting_opportunities(holdings)
    assert len(opps) == 1
    assert opps[0]['symbol'] == 'SPY'
    assert opps[0]['replacement_candidate'] == 'IVV'

def test_optimization_logic():
    algo = ConstructionAlgorithm()
    assets = ['A', 'B']
    # Perfect negative correlation should result in 50/50 split for min variance
    data = {'A': [0.1, -0.1, 0.1, -0.1], 'B': [-0.1, 0.1, -0.1, 0.1]}
    returns_df = pd.DataFrame(data)
    weights = algo.optimize_portfolio(returns_df)
    assert weights['A'] == pytest.approx(0.5, abs=0.01)
    assert weights['B'] == pytest.approx(0.5, abs=0.01)
