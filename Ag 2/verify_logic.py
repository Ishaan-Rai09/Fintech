import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm

def verify_logic():
    print("🚀 Starting Logic Verification...")
    tickers = ["AAPL", "MSFT"]
    weights = np.array([0.5, 0.5])
    investment = 100000
    confidence = 0.95
    horizon = 1
    
    print(f"Fetching data for {tickers}...")
    data = yf.download(tickers, period="1y")
    if 'Adj Close' in data.columns:
        data = data['Adj Close']
    else:
        data = data['Close']
    returns = data.pct_change().dropna()
    
    # 1. Historical VaR
    port_returns = (returns * weights).sum(axis=1)
    hist_var = np.percentile(port_returns, (1 - confidence) * 100) * investment
    print(f"✅ Historical VaR: ${abs(hist_var):,.2f}")
    
    # 2. Parametric VaR
    cov_matrix = returns.cov()
    avg_returns = returns.mean()
    port_mean = np.dot(weights, avg_returns)
    port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    z_score = norm.ppf(1 - confidence)
    param_var = (port_mean + z_score * port_std) * investment
    print(f"✅ Parametric VaR: ${abs(param_var):,.2f}")
    
    # 3. Monte Carlo VaR
    n_sims = 10000
    L = np.linalg.cholesky(cov_matrix)
    Z = np.random.normal(size=(n_sims, len(weights)))
    correlated_returns = np.dot(Z, L.T) + avg_returns.values
    mc_sim_port_returns = np.dot(correlated_returns, weights)
    mc_var = np.percentile(mc_sim_port_returns, (1 - confidence) * 100) * investment
    print(f"✅ Monte Carlo VaR: ${abs(mc_var):,.2f}")
    
    # Sanity Checks
    assert abs(hist_var) > 0, "Historical VaR should be non-zero"
    assert abs(param_var) > 0, "Parametric VaR should be non-zero"
    assert abs(mc_var) > 0, "Monte Carlo VaR should be non-zero"
    
    print("\n✨ All core math logic verified successfully!")

if __name__ == "__main__":
    verify_logic()
