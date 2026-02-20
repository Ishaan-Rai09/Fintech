import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from engine import ClientEngine, ConstructionAlgorithm, RebalancingSystem, TaxOptimizer
import datetime

# --- Page Config ---
st.set_page_config(page_title="RoboAdvisor Pro", layout="wide", initial_sidebar_state="expanded")

# --- Custom Styling ---
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .stSidebar {
        background-color: #161b22;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Modules ---
client_engine = ClientEngine()
construction_algo = ConstructionAlgorithm()
rebalancer = RebalancingSystem()
tax_optimizer = TaxOptimizer()

# --- App Layout ---
st.title("🤖 RoboAdvisor Pro")
st.subheader("Intelligent Portfolio Management & Tax Optimization")

with st.sidebar:
    st.header("👤 Client Profile")
    name = st.text_input("Client Name", value="John Doe")
    age = st.slider("Age", 18, 80, 35)
    horizon = st.slider("Investment Horizon (Years)", 1, 40, 15)
    
    st.divider()
    st.header("📋 Risk Assessment")
    q1 = st.radio("What is your primary goal?", ["Capital Preservation", "Moderate Growth", "Maximum Wealth"])
    q2 = st.radio("Reaction to 20% market drop?", ["Sell everything", "Do nothing", "Buy more"])
    
    # Simple logic to convert radio to scores for the engine
    risk_mapping = {"Capital Preservation": 1, "Moderate Growth": 3, "Maximum Wealth": 5,
                    "Sell everything": 1, "Do nothing": 3, "Buy more": 5}
    score_list = [risk_mapping[q1], risk_mapping[q2]]
    
    risk_profile = client_engine.calculate_risk_score(score_list)
    st.success(f"Assessed Risk Profile: **{risk_profile}**")
    
    st.divider()
    st.header("💰 Portfolio Inputs")
    total_val = st.number_input("Total Portfolio Value ($)", value=100000, step=1000)

# --- Tabs for different blocks ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Portfolio Construction", "⚖️ Automated Rebalancing", "📉 Tax Optimization", "📈 Market Simulation"])

# --- 1. Portfolio Construction ---
with tab1:
    st.header("Target Asset Allocation")
    target_alloc = client_engine.get_target_allocation(risk_profile)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Visualizing the target
        df_target = pd.DataFrame(list(target_alloc.items()), columns=['Asset', 'Weight'])
        fig_pie = px.pie(df_target, values='Weight', names='Asset', 
                         title=f"Recommended Allocation for {risk_profile} Profile",
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.write("### Allocation Details")
        st.table(df_target.style.format({'Weight': '{:.0%}'}))
        st.info("The algorithm uses Mean-Variance Optimization to balance yield vs risk based on your inputs.")

# --- 2. Automated Rebalancing ---
with tab2:
    st.header("Drift Detection & Rebalancing")
    
    # Simulated current holdings for demo
    st.write("### Current vs Target")
    sim_current = {
        "equity": target_alloc['equity'] + 0.08,  # Drifted up
        "bonds": target_alloc['bonds'] - 0.06,   # Drifted down
        "cash": target_alloc['cash'] - 0.02
    }
    
    col_bal1, col_bal2 = st.columns(2)
    
    with col_bal1:
        # Comparison Chart
        comparison_data = []
        for asset in target_alloc.keys():
            comparison_data.append({"Asset": asset, "Type": "Target", "Weight": target_alloc[asset]})
            comparison_data.append({"Asset": asset, "Type": "Current", "Weight": sim_current[asset]})
        
        df_comp = pd.DataFrame(comparison_data)
        fig_bar = px.bar(df_comp, x='Asset', y='Weight', color='Type', barmode='group',
                         title="Allocation Drift Analysis")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_bal2:
        needs_rebalance, drifts = rebalancer.check_drift(sim_current, target_alloc)
        if needs_rebalance:
            st.warning("⚠️ Portfolio Drift Detected! Rebalancing required.")
            
            # Current values in dollars
            current_vals = {k: v * total_val for k, v in sim_current.items()}
            orders = rebalancer.generate_orders(current_vals, target_alloc, total_val)
            
            st.write("### Required Trades")
            df_orders = pd.DataFrame(orders)
            st.dataframe(df_orders.style.format({'amount': '${:,.2f}'}))
        else:
            st.success("✅ Portfolio is within drift thresholds.")

# --- 3. Tax Optimization ---
with tab3:
    st.header("Tax-Loss Harvesting Opportunities")
    st.write("Identifying positions with unrealized losses for tax deductions.")
    
    # Simulated holdings
    holdings = [
        {'symbol': 'SPY', 'cost_basis': 450, 'current_price': 380}, # Big loss
        {'symbol': 'QQQ', 'cost_basis': 300, 'current_price': 310}, # Gain
        {'symbol': 'VTI', 'cost_basis': 220, 'current_price': 215}, # Small loss
    ]
    
    df_holdings = pd.DataFrame(holdings)
    df_holdings['unrealized_gl'] = (df_holdings['current_price'] - df_holdings['cost_basis'])
    
    st.write("### Current Positions (Simulated)")
    st.dataframe(df_holdings.style.applymap(lambda x: 'color: red' if x < 0 else 'color: green', subset=['unrealized_gl']))
    
    opportunities = tax_optimizer.identify_harvesting_opportunities(holdings)
    
    if opportunities:
        st.info(f"Found {len(opportunities)} tax harvesting opportunities.")
        for opp in opportunities:
            with st.expander(f"Harvest Loss: {opp['symbol']} (Est. Savings: ${opp['loss_amount'] * 0.25:,.2f})"):
                st.write(f"**Current Loss:** ${opp['loss_amount']:.2f}")
                st.write(f"**Action:** Sell {opp['symbol']} and immediately buy **{opp['replacement_candidate']}**.")
                st.caption("Note: Using replacements avoids the 30-day Wash Sale rule while maintaining market exposure.")
    else:
        st.success("No significant tax harvesting opportunities found at current threshold.")

# --- 4. Market Simulation (MVO Preview) ---
with tab4:
    st.header("MVO Engine Preview")
    st.write("Generating efficient frontier based on mock historical data.")
    
    # Generating dummy returns for optimization preview
    assets = ['Equity ETF', 'Bond ETF', 'Gold', 'Real Estate']
    data = np.random.randn(100, 4) + 0.05
    returns_df = pd.DataFrame(data, columns=assets)
    
    if st.button("Run Optimizer"):
        optimized_weights = construction_algo.optimize_portfolio(returns_df)
        st.success("Optimization Complete!")
        
        df_opt = pd.DataFrame(list(optimized_weights.items()), columns=['Asset', 'Optimized Weight'])
        st.plotly_chart(px.bar(df_opt, x='Asset', y='Optimized Weight', color='Asset', title="Max Sharpe Ratio Weights"))
