import streamlit as st
from utils.data_generator import load_loan_data, get_vintage_data
from utils.risk_analyzer import get_risk_summary, calculate_risk_metrics, get_risk_category_table
from components.portfolio_overview import render_portfolio_overview
from components.vintage_analysis import render_vintage_analysis
from components.risk_analysis import render_risk_analysis
from components.data_display import render_data_display #Added from original

st.set_page_config(page_title="AI-Powered Risk Insights Dashboard",
                   page_icon="📊",
                   layout="wide")

# Hide the sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

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
st.title("Risk Insights Dashboard")

# Platform selection in session state
if 'selected_platform' not in st.session_state:
    st.session_state.selected_platform = 'Priority'  # Set default platform

# Create tabs
overview, portfolio, data_tab = st.tabs([ #Added data_tab from original
    "Overview",
    "Portfolio Analysis",
    "Data" #Added from original
])

with overview:
    st.header("Dashboard Overview")

    st.markdown("""
    Welcome to the **Pipe Risk Insights Dashboard**. This tool provides real-time visibility into loan performance across embedded finance platforms, focusing on three key risk areas:

    📈 **Portfolio Overview**
    - Total capital deployed and returned
    - Platform-specific performance metrics
    - Loan size distribution

    📊 **Vintage Analysis**
    - Cohort performance tracking
    - Repayment velocity trends
    - Vintage comparison

    ⚠️ **Risk Analysis**
    - AI-driven risk categorization
    - Early detection of repayment issues and revenue decline
    """)

    # Risk Category Explanation
    st.subheader("Risk Categories Explained")
    risk_table = get_risk_category_table() #Using the function from original code.  Assumed to exist.
    st.dataframe(
        risk_table,
        column_config={
            "Risk Category": st.column_config.Column(width=200),
            "Definition": st.column_config.Column(width=800),
            "Severity": st.column_config.Column(width=150)
        },
        hide_index=True
    )

    st.markdown("---")
    st.subheader("Platform Selection")
    st.markdown("Use the selector below to focus on specific lending partners.")

    # Platform selection
    platforms = sorted(df['platform'].unique().tolist())
    # Ensure Priority is first in the list after 'All'
    if 'Priority' in platforms:
        platforms.remove('Priority')
        platform_options = ['All', 'Priority'] + platforms
    else:
        platform_options = ['All'] + platforms

    # Find the index of Priority
    default_index = platform_options.index('Priority') if 'Priority' in platform_options else 0 #Handle case where Priority might not exist

    st.session_state.selected_platform = st.selectbox(
        "Select Platform",
        options=platform_options,
        index=default_index
    )

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

with data_tab: #Data tab content from original code.
    render_data_display(filtered_df)