import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Income Tax Calculator FY 2024-25",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f23 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 16px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .metric-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .regime-card {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(0, 212, 255, 0.1) 100%);
        border-radius: 20px;
        padding: 28px;
        border: 1px solid rgba(124, 58, 237, 0.3);
        margin: 10px 0;
    }
    
    .regime-card-new {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(124, 58, 237, 0.5);
    }
    
    .savings-badge {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
    }
    
    h1 {
        background: linear-gradient(90deg, #00d4ff, #7c3aed, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
    }
    
    .stRadio > div {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Tax Calculation Functions
def calculate_new_regime_tax(income: float) -> tuple:
    """Calculate tax under New Regime FY 2024-25"""
    standard_deduction = 75000
    taxable_income = max(0, income - standard_deduction)
    
    slabs = [
        (300000, 0),
        (400000, 0.05),
        (300000, 0.10),
        (200000, 0.15),
        (300000, 0.20),
        (float('inf'), 0.30)
    ]
    
    tax = 0
    remaining = taxable_income
    slab_breakdown = []
    
    for limit, rate in slabs:
        if remaining <= 0:
            break
        taxable_in_slab = min(remaining, limit)
        tax_in_slab = taxable_in_slab * rate
        if taxable_in_slab > 0 and rate > 0:
            slab_breakdown.append({
                'slab': f'{int(rate*100)}%',
                'amount': taxable_in_slab,
                'tax': tax_in_slab
            })
        tax += tax_in_slab
        remaining -= limit
    
    # Rebate under 87A - if taxable income <= 7L, full rebate up to 25000
    rebate = 0
    if taxable_income <= 700000:
        rebate = min(tax, 25000)
        tax = max(0, tax - rebate)
    
    # Add 4% Health and Education Cess
    cess = tax * 0.04
    total_tax = tax + cess
    
    return total_tax, taxable_income, rebate, cess, slab_breakdown, standard_deduction

def calculate_old_regime_tax(income: float, age: str, deductions: dict) -> tuple:
    """Calculate tax under Old Regime"""
    # Standard Deduction
    standard_deduction = 50000
    
    # Calculate total deductions
    total_deductions = standard_deduction
    total_deductions += min(deductions.get('section_80c', 0), 150000)
    total_deductions += min(deductions.get('section_80d', 0), 75000)
    total_deductions += deductions.get('hra', 0)
    total_deductions += min(deductions.get('section_80ccd', 0), 50000)
    total_deductions += deductions.get('home_loan_interest', 0)
    total_deductions += deductions.get('other_deductions', 0)
    
    taxable_income = max(0, income - total_deductions)
    
    # Tax slabs based on age
    if age == "Below 60":
        basic_exemption = 250000
        slabs = [
            (250000, 0.05),
            (500000, 0.20),
            (float('inf'), 0.30)
        ]
    elif age == "60-80 (Senior)":
        basic_exemption = 300000
        slabs = [
            (200000, 0.05),
            (500000, 0.20),
            (float('inf'), 0.30)
        ]
    else:  # Super Senior
        basic_exemption = 500000
        slabs = [
            (500000, 0.20),
            (float('inf'), 0.30)
        ]
    
    tax = 0
    remaining = max(0, taxable_income - basic_exemption)
    slab_breakdown = []
    
    for limit, rate in slabs:
        if remaining <= 0:
            break
        taxable_in_slab = min(remaining, limit)
        tax_in_slab = taxable_in_slab * rate
        if taxable_in_slab > 0:
            slab_breakdown.append({
                'slab': f'{int(rate*100)}%',
                'amount': taxable_in_slab,
                'tax': tax_in_slab
            })
        tax += tax_in_slab
        remaining -= limit
    
    # Rebate under 87A
    rebate = 0
    if taxable_income <= 500000:
        rebate = min(tax, 12500)
        tax = max(0, tax - rebate)
    
    # Health and Education Cess
    cess = tax * 0.04
    total_tax = tax + cess
    
    return total_tax, taxable_income, rebate, cess, slab_breakdown, total_deductions

def format_currency(amount: float) -> str:
    """Format amount in Indian currency style"""
    if amount >= 10000000:
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:
        return f"₹{amount/100000:.2f} L"
    else:
        return f"₹{amount:,.0f}"

# Main App
st.title("💰 Income Tax Calculator")
st.markdown("##### FY 2024-25 (AY 2025-26) | India")

# Sidebar - Input Section
with st.sidebar:
    st.markdown("### 📋 Personal Details")
    
    age_group = st.selectbox(
        "Age Group",
        ["Below 60", "60-80 (Senior)", "Above 80 (Super Senior)"],
        help="Tax slabs differ based on age under old regime"
    )
    
    st.markdown("---")
    st.markdown("### 💵 Income Details")
    
    salary_income = st.number_input(
        "Salary Income (Annual)",
        min_value=0,
        max_value=100000000,
        value=1000000,
        step=10000,
        format="%d"
    )
    
    other_income = st.number_input(
        "Other Income",
        min_value=0,
        max_value=50000000,
        value=0,
        step=10000,
        format="%d",
        help="Interest, rental income, etc."
    )
    
    total_income = salary_income + other_income
    
    st.markdown("---")
    st.markdown("### 🏦 Deductions (Old Regime)")
    
    with st.expander("Section 80C (Max ₹1.5L)", expanded=True):
        sec_80c = st.number_input(
            "80C Investments",
            min_value=0,
            max_value=150000,
            value=150000,
            step=1000,
            help="PPF, ELSS, LIC, EPF, etc."
        )
    
    with st.expander("Section 80D - Medical Insurance"):
        sec_80d = st.number_input(
            "Medical Insurance Premium",
            min_value=0,
            max_value=75000,
            value=25000,
            step=1000,
            help="Self, family & parents"
        )
    
    with st.expander("HRA Exemption"):
        hra = st.number_input(
            "HRA Exemption Amount",
            min_value=0,
            max_value=500000,
            value=0,
            step=1000
        )
    
    with st.expander("Other Deductions"):
        sec_80ccd = st.number_input(
            "80CCD(1B) - NPS (Max ₹50K)",
            min_value=0,
            max_value=50000,
            value=0,
            step=1000
        )
        
        home_loan = st.number_input(
            "Home Loan Interest (80EEA)",
            min_value=0,
            max_value=200000,
            value=0,
            step=1000
        )
        
        other_ded = st.number_input(
            "Other Deductions",
            min_value=0,
            max_value=500000,
            value=0,
            step=1000
        )

# Prepare deductions dictionary
deductions = {
    'section_80c': sec_80c,
    'section_80d': sec_80d,
    'hra': hra,
    'section_80ccd': sec_80ccd,
    'home_loan_interest': home_loan,
    'other_deductions': other_ded
}

# Calculate taxes for both regimes
new_tax, new_taxable, new_rebate, new_cess, new_breakdown, new_std_ded = calculate_new_regime_tax(total_income)
old_tax, old_taxable, old_rebate, old_cess, old_breakdown, old_total_ded = calculate_old_regime_tax(total_income, age_group, deductions)

# Determine better regime
tax_savings = abs(new_tax - old_tax)
better_regime = "New Regime" if new_tax <= old_tax else "Old Regime"

# Main Content
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <p class="metric-label">Gross Income</p>
        <p class="metric-value">{}</p>
    </div>
    """.format(format_currency(total_income)), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <p class="metric-label">Tax Savings Potential</p>
        <p class="metric-value">{}</p>
    </div>
    """.format(format_currency(tax_savings)), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <p class="metric-label">Recommended Regime</p>
        <p class="metric-value" style="font-size: 1.8rem;">{}</p>
    </div>
    """.format(better_regime), unsafe_allow_html=True)

st.markdown("---")

# Regime Comparison
col_old, col_new = st.columns(2)

with col_old:
    st.markdown("""
    <div class="regime-card">
        <h3 style="color: #a78bfa; margin-top: 0;">📜 Old Tax Regime</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.metric("Taxable Income", format_currency(old_taxable))
    st.metric("Total Deductions", format_currency(old_total_ded))
    st.metric("Tax Before Rebate", format_currency(old_tax + old_rebate - old_cess))
    
    if old_rebate > 0:
        st.metric("Rebate u/s 87A", f"-{format_currency(old_rebate)}")
    
    st.metric("Health & Education Cess (4%)", format_currency(old_cess))
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #7c3aed, #a78bfa); padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px;">
        <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">TOTAL TAX PAYABLE</p>
        <p style="margin: 0; color: white; font-size: 2rem; font-weight: 700;">{format_currency(old_tax)}</p>
    </div>
    """, unsafe_allow_html=True)

with col_new:
    st.markdown("""
    <div class="regime-card regime-card-new">
        <h3 style="color: #00d4ff; margin-top: 0;">✨ New Tax Regime</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.metric("Taxable Income", format_currency(new_taxable))
    st.metric("Standard Deduction", format_currency(new_std_ded))
    st.metric("Tax Before Rebate", format_currency(new_tax + new_rebate - new_cess))
    
    if new_rebate > 0:
        st.metric("Rebate u/s 87A", f"-{format_currency(new_rebate)}")
    
    st.metric("Health & Education Cess (4%)", format_currency(new_cess))
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #0891b2, #00d4ff); padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px;">
        <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">TOTAL TAX PAYABLE</p>
        <p style="margin: 0; color: white; font-size: 2rem; font-weight: 700;">{format_currency(new_tax)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Visual Comparison
st.markdown("### 📊 Tax Comparison")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Bar Chart Comparison
    fig_bar = go.Figure(data=[
        go.Bar(
            name='Tax Amount',
            x=['Old Regime', 'New Regime'],
            y=[old_tax, new_tax],
            marker=dict(
                color=['#7c3aed', '#00d4ff'],
                line=dict(width=0)
            ),
            text=[format_currency(old_tax), format_currency(new_tax)],
            textposition='outside',
            textfont=dict(color='white', size=14)
        )
    ])
    
    fig_bar.update_layout(
        title="Tax Comparison",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        xaxis=dict(showgrid=False),
        height=400
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    # Income Breakdown Pie Chart
    if better_regime == "New Regime":
        labels = ['Tax', 'Standard Deduction', 'Take Home']
        values = [new_tax, new_std_ded, total_income - new_tax - new_std_ded]
        colors = ['#ef4444', '#f59e0b', '#10b981']
    else:
        labels = ['Tax', 'Deductions', 'Take Home']
        values = [old_tax, old_total_ded, total_income - old_tax - old_total_ded]
        colors = ['#ef4444', '#f59e0b', '#10b981']
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(color='white', size=12)
    )])
    
    fig_pie.update_layout(
        title=f"Income Breakdown ({better_regime})",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=400,
        annotations=[dict(
            text=format_currency(total_income - (new_tax if better_regime == "New Regime" else old_tax)),
            x=0.5, y=0.5,
            font_size=18,
            font_color='#10b981',
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# Tax Slabs Reference
st.markdown("---")
st.markdown("### 📋 Tax Slabs Reference (FY 2024-25)")

col_slab1, col_slab2 = st.columns(2)

with col_slab1:
    st.markdown("#### Old Regime (Below 60)")
    old_slab_df = pd.DataFrame({
        'Income Range': ['Up to ₹2.5L', '₹2.5L - ₹5L', '₹5L - ₹10L', 'Above ₹10L'],
        'Tax Rate': ['Nil', '5%', '20%', '30%']
    })
    st.table(old_slab_df)

with col_slab2:
    st.markdown("#### New Regime")
    new_slab_df = pd.DataFrame({
        'Income Range': ['Up to ₹3L', '₹3L - ₹7L', '₹7L - ₹10L', '₹10L - ₹12L', '₹12L - ₹15L', 'Above ₹15L'],
        'Tax Rate': ['Nil', '5%', '10%', '15%', '20%', '30%']
    })
    st.table(new_slab_df)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.5); padding: 20px;">
    <p>⚠️ This calculator is for informational purposes only. Please consult a tax professional for accurate tax planning.</p>
    <p>Built with ❤️ using Streamlit | FY 2024-25</p>
</div>
""", unsafe_allow_html=True)
