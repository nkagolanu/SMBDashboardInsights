import streamlit as st
import pandas as pd
from utils.data_generator import load_loan_data, get_vintage_data
from utils.risk_analyzer import get_risk_summary, calculate_risk_metrics
from components.portfolio_overview import render_portfolio_overview
from components.vintage_analysis import render_vintage_analysis
from components.risk_analysis import render_risk_analysis
from components.data_display import render_data_display

st.set_page_config(page_title="AI-Powered Risk Insights Dashboard",
                   page_icon="📊",
                   layout="wide",
                   initial_sidebar_state="collapsed")

# Hide the sidebar hamburger menu completely
hide_streamlit_style = """
<style>
    div[data-testid="collapsedControl"] {
        display: none
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Load real data
@st.cache_data
def load_data():
    df = load_loan_data()
    vintage_data = get_vintage_data(df)
    risk_summary = get_risk_summary(df)
    risk_metrics = calculate_risk_metrics(df)
    return df, vintage_data, risk_summary, risk_metrics


# Load data with error handling
try:
    df, vintage_data, risk_summary, risk_metrics = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    df = pd.DataFrame()
    vintage_data = pd.DataFrame()
    risk_summary = pd.DataFrame()
    risk_metrics = {}

# Main navigation
st.title("Risk Insights Dashboard")

# Platform selection in session state
if 'selected_platform' not in st.session_state:
    st.session_state.selected_platform = 'Priority'  # Set default platform

# Create tabs
overview, portfolio, data_tab = st.tabs(
    ["Overview", "Portfolio Analysis", "Data"])

with overview:
    st.markdown("### Portfolio Selection")

    # Platform selection
    platforms = sorted(df['platform'].unique().tolist())
    # Ensure Priority is first in the list after 'All'
    if 'Priority' in platforms:
        platforms.remove('Priority')
        platform_options = ['All', 'Priority'] + platforms
    else:
        platform_options = ['All'] + platforms

    # Find the index of Priority
    default_index = platform_options.index('Priority')

    st.session_state.selected_platform = st.selectbox(
        "Select Platform to run analysis",
        options=platform_options,
        index=default_index)

    st.markdown("---")

    st.markdown("""
    ### Purpose

    The **Pipe Risk Insights Dashboard** provides a real-time view of loan performance across embedded finance platforms. It helps the Risk Team track total lending activity, repayment trends, and emerging risks using three key risk categories: **Liquidity Risk, Revenue Drop Risk, and Non-Payment Risk.**

    With this dashboard, users can:

    ✅ **Monitor outstanding lending activity** across platforms with high-level metrics (total loans, fees, and loan distribution).  
    ✅ **Analyze loan vintages** to assess repayment trends over time.  
    ✅ **Identify early warning signs** using risk metrics tailored for revenue-based financing.  

    This enables **data-driven underwriting adjustments** and **proactive risk mitigation** to optimize Pipe's lending strategy.
    """)

    # Risk Category Explanation
    data = {
        "Risk Category":
        ["Liquidity Risk", "Revenue Drop Risk", "Non-Payment Risk"],
        "Definition": [
            "Business revenue is stable, but their overall cash flow health is deteriorating. They might be overleveraged, have high expenses, or be showing early warning signs of financial strain. Repayments are still occurring at the expected percentage, but their total financial health is weakening.",
            "Business revenue has dropped ≥50% for multiple months, meaning their ability to make repayments is significantly reduced. They are still making some repayments, but their funding risk is increasing.",
            "Business has had $0 revenue for 60+ days, meaning no repayments are occurring. This suggests business closure, switching platforms, or severe distress."
        ],
        "Severity": ["Mild", "Moderate", "Severe"]
    }

    # Convert DataFrame
    risk_table = pd.DataFrame(data)

    # Force Streamlit to render HTML correctly
    def format_html(text):
        return f'<div style="text-align: left; word-wrap: break-word; white-space: pre-wrap;">{text}</div>'

    risk_table["Definition"] = risk_table["Definition"].apply(format_html)

    st.markdown("#### Risk Categories")

    # Use Markdown-rendered table for styling
    st.markdown("""
        <style>
            thead th {
                text-align: left !important;  /* Left-align headers */
            }
            tbody tr td {
                white-space: pre-wrap !important;
                word-wrap: break-word !important;
                text-align: left !important;  /* Left-aligns text */
            }
            tbody tr td:nth-child(3) {
                white-space: nowrap !important;
                text-align: center !important;  /* Centers the Severity column */
            }
        </style>
    """,
                unsafe_allow_html=True)

    # Render as HTML for proper text wrapping and alignment
    st.write(risk_table.to_html(escape=False, index=False),
             unsafe_allow_html=True)

    st.markdown("**Why these Three Risk Metrics**")

    st.markdown(
        "Traditional delinquency metrics like 90 days past due may not work for Pipe’s revenue-based financing because there are no fixed repayment schedules—repayments fluctuate with revenue. Instead, these three risk metrics are one way to capture signs of financial distress."
    )

    st.markdown("---")

# Filter data based on selected platform
filtered_df = df
if st.session_state.selected_platform != 'All':
    filtered_df = df[df['platform'] == st.session_state.selected_platform]

# Render portfolio analysis with all components
with portfolio:

    # Portfolio Overview Section
    render_portfolio_overview(filtered_df, st.session_state.selected_platform)

    st.markdown("---")

    # Vintage Analysis Section
    render_vintage_analysis(filtered_df, get_vintage_data(filtered_df))

    st.markdown("---")

# Data tab content
with data_tab:
    render_data_display(filtered_df)

# Remove sidebar export since we have it in the Data tab now
