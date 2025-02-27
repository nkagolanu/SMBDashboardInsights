import streamlit as st
from utils.data_generator import load_loan_data, get_vintage_data
from utils.risk_analyzer import get_risk_summary, calculate_risk_metrics, get_risk_category_table
from components.portfolio_overview import render_portfolio_overview
from components.vintage_analysis import render_vintage_analysis
from components.risk_analysis import render_risk_analysis

st.set_page_config(page_title="AI-Powered Risk Insights Dashboard",
                   page_icon="📊",
                   layout="wide")


# Load real data
@st.cache_data
def load_data():
    df = load_loan_data()
    vintage_data = get_vintage_data(df)
    risk_summary = get_risk_summary(df)
    risk_metrics = calculate_risk_metrics(df)
    return df, vintage_data, risk_summary, risk_metrics


# Load data
df, vintage_data, risk_summary, risk_metrics = load_data()

# Main navigation
st.title("AI-Powered Risk Insights Dashboard")

# Platform selection in session state
if 'selected_platform' not in st.session_state:
    st.session_state.selected_platform = 'Priority'  # Set default platform

# Create tabs
overview, portfolio = st.tabs(["Overview", "Portfolio Analysis"])

with overview:
    st.header("Dashboard Overview")

    st.markdown("""
    ### Purpose
    This AI-powered dashboard provides comprehensive risk insights for Pipe's embedded finance portfolio:

    🎯 **Portfolio Monitoring**
    - Track active advances and repayment performance across platforms
    - Monitor total capital deployed and risk exposure

    📈 **Vintage Analysis**
    - Analyze loan performance by cohort
    - Identify trends in repayment patterns

    ⚠️ **Risk Analysis**
    - AI-driven risk categorization
    - Early detection of repayment issues and revenue decline
    """)

    # Risk Category Explanation
    risk_table = get_risk_category_table()

    st.subheader("Risk Categories Explained")

    st.data_editor(risk_table,
                   column_config={
                       "Risk Category":
                       st.column_config.Column(width=250),
                       "Definition":
                       st.column_config.Column(
                           width=700,
                           help="Detailed explanation of the risk.",
                           required=True),
                       "Severity":
                       st.column_config.Column(width=150,
                                               help="Risk severity",
                                               disabled=True)
                   },
                   hide_index=True,
                   use_container_width=True)

    st.markdown("---")
    st.subheader("Platform Selection")
    st.markdown(
        "Use the selector below to focus on specific lending partners.")

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

    st.session_state.selected_platform = st.selectbox("Select Platform",
                                                      options=platform_options,
                                                      index=default_index)

# Filter data based on selected platform
filtered_df = df
if st.session_state.selected_platform != 'All':
    filtered_df = df[df['platform'] == st.session_state.selected_platform]

# Render portfolio analysis with all components
with portfolio:
    st.header("Portfolio Analysis")

    # Portfolio Overview Section
    render_portfolio_overview(filtered_df)

    st.markdown("---")

    # Vintage Analysis Section
    render_vintage_analysis(filtered_df, get_vintage_data(filtered_df))

    st.markdown("---")

    # Risk Analysis Section
    render_risk_analysis(filtered_df, get_risk_summary(filtered_df))

# Add download functionality
if st.sidebar.button("Export Data"):
    csv = filtered_df.to_csv(index=False)
    st.sidebar.download_button(label="Download CSV",
                               data=csv,
                               file_name="loan_portfolio.csv",
                               mime="text/csv")
