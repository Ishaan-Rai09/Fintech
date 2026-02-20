import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import datetime

# --- Page Config & Styling ---
st.set_page_config(page_title="VaultVaR Pro | Portfolio Risk Engine", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        border: 1px solid #38bdf8;
    }
    
    h1, h2, h3 {
        color: #38bdf8 !important;
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    .stSidebar {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #94a3b8;
        padding: 0 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Controls ---
with st.sidebar:
    st.image("https://img.icons8.com/glow/100/null/safe.png", width=80)
    st.title("Risk Configuration")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        ticker1 = st.text_input("Stock A", value="AAPL").upper()
        weight1 = st.number_input("Weight A (%)", min_value=0, max_value=100, value=50) / 100
    with col2:
        ticker2 = st.text_input("Stock B", value="MSFT").upper()
        weight2 = 1.0 - weight1
        st.caption(f"Weight B: **{weight2*100:.1f}%**")

    st.markdown("---")
    initial_investment = st.number_input("Initial Investment ($)", value=100000, step=1000)
    conf_level = st.slider("Confidence Level (%)", 90, 99, 95) / 100
    time_horizon = st.number_input("Time Horizon (Days)", min_value=1, value=1)
    
    st.markdown("---")
    lookback_years = st.slider("Lookback Period (Years)", 1, 10, 2)
    
# --- Data Engine ---
@st.cache_data
def get_data(tickers, period):
    try:
        data = yf.download(tickers, period=period, progress=False)
        if data.empty:
            return None
        
        # Flatten MultiIndex if present
        if isinstance(data.columns, pd.MultiIndex):
            # yfinance v0.2.x with multiple tickers
            if 'Adj Close' in data.columns.levels[0]:
                data = data['Adj Close']
            else:
                data = data['Close']
        else:
            # Single ticker or older structure
            if 'Adj Close' in data.columns:
                data = data[['Adj Close']]
            elif 'Close' in data.columns:
                data = data[['Close']]
                
        return data.ffill().dropna()
    except Exception as e:
        st.error(f"Data Fetching Error: {e}")
        return None

def calculate_returns(df):
    returns = df.pct_change().dropna()
    return returns

# --- VaR Calculation Methods ---

def calc_historical_var(returns, weights, confidence, investment, horizon):
    # If weights is 1D and returns is 2D
    portfolio_returns = (returns * weights).sum(axis=1)
    var_percentile = np.percentile(portfolio_returns, (1 - confidence) * 100)
    var_value = investment * var_percentile * np.sqrt(horizon)
    return var_value, portfolio_returns

def calc_parametric_var(returns, weights, confidence, investment, horizon):
    cov_matrix = returns.cov()
    avg_returns = returns.mean()
    
    port_mean = np.dot(weights, avg_returns)
    port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    z_score = norm.ppf(1 - confidence)
    var_1d = (port_mean + z_score * port_std) * investment
    var_horizon = var_1d * np.sqrt(horizon)
    return var_horizon

def calc_monte_carlo_var(returns, weights, confidence, investment, horizon, n_sims=10000):
    cov_matrix = returns.cov()
    avg_returns = returns.mean()
    
    L = np.linalg.cholesky(cov_matrix)
    Z = np.random.normal(size=(n_sims, len(weights)))
    correlated_returns = np.dot(Z, L.T) + avg_returns.values
    port_sim_returns = np.dot(correlated_returns, weights)
    
    var_percentile = np.percentile(port_sim_returns, (1 - confidence) * 100)
    var_value = investment * var_percentile * np.sqrt(horizon)
    
    return var_value, port_sim_returns

# --- Main App Logic ---
st.title("�️ VaultVaR Pro")
st.markdown("#### High-Precision Portfolio Risk Analytics")

try:
    with st.spinner("Analyzing Market Dynamics..."):
        tickers = [ticker1, ticker2]
        raw_data = get_data(tickers, period=f"{lookback_years}y")
        
        if raw_data is None or len(raw_data) < 2:
            st.error("⚠️ Insufficient data found. Please check your tickers or connectivity.")
            st.stop()
            
        returns = calculate_returns(raw_data)
        weights_arr = np.array([weight1, weight2])

    # -- Calculations --
    hist_var, port_returns = calc_historical_var(returns, weights_arr, conf_level, initial_investment, time_horizon)
    param_var = calc_parametric_var(returns, weights_arr, conf_level, initial_investment, time_horizon)
    mc_var, mc_returns = calc_monte_carlo_var(returns, weights_arr, conf_level, initial_investment, time_horizon)

    # -- Metric Display --
    m1, m2, m3 = st.columns(3)
    
    m1.metric("Historical VaR", f"${abs(hist_var):,.2f}", f"{(1-conf_level)*100:.0f}% Tail")
    m2.metric("Parametric VaR", f"${abs(param_var):,.2f}", "Normal Dist.")
    m3.metric("Monte Carlo VaR", f"${abs(mc_var):,.2f}", f"{10000:,} Trials")

    # -- Visuals --
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["� Equity Curve", "� Distribution Risk", "⚖️ Method Benchmarking"])

    with tab1:
        st.subheader("Simulated Historical Performance")
        port_cum_returns = (1 + (returns * weights_arr).sum(axis=1)).cumprod() - 1
        st.line_chart(port_cum_returns)
        
    with tab2:
        st.subheader("Probabilistic Return Distribution")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.histplot(port_returns, color="#38bdf8", label="Historical", kde=True, stat="density", alpha=0.4)
        sns.histplot(mc_returns, color="#818cf8", label="Monte Carlo", kde=True, stat="density", alpha=0.2)
        
        # Draw VaR lines (standardized to daily for visual check)
        hist_line = hist_var / initial_investment / np.sqrt(time_horizon)
        mc_line = mc_var / initial_investment / np.sqrt(time_horizon)
        
        plt.axvline(hist_line, color='#38bdf8', linestyle='--', linewidth=2, label=f'Hist VaR')
        plt.axvline(mc_line, color='#818cf8', linestyle='--', linewidth=2, label=f'MC VaR')
        
        plt.legend()
        plt.title(f"Density of Returns & Potential Extreme Losses")
        plt.xlabel("Daily Return")
        plt.style.use('dark_background')
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')
        st.pyplot(fig)

    with tab3:
        st.subheader("Loss Magnitude Comparison")
        comparison_df = pd.DataFrame({
            'Method': ['Historical', 'Parametric', 'Monte Carlo'],
            'VaR ($)': [abs(hist_var), abs(param_var), abs(mc_var)]
        })
        st.bar_chart(comparison_df.set_index('Method'))
        
        st.markdown(f"""
        ### � Deep Dive: VaR Methodologies
        
        1.  **Historical VaR** – Uses real past returns. Captures real-world skewness and "fat tails" but is limited to what happened in the {lookback_years}y lookback.
        2.  **Parametric VaR** – Based on the Variance-Covariance matrix. It's clean and mathematical but assumes a **Normal Distribution**, which often underestimates the severity of market crashes.
        3.  **Monte Carlo VaR** – Runs 10,000 simulations using the Cholesky decomposition of your portfolio's covariance. It's the gold standard for stress-testing complex portfolios.
        """)

except Exception as e:
    st.error(f"❌ Analytic Engine Failure: {e}")
    st.info("Check ticker symbols (e.g., TSLA, BTC-USD) and ensure weights total 100%.")

st.markdown("---")
st.caption("VaultVaR Pro v1.0 | Developed for AG-2 FinTech Solutions")
