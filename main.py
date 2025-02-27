import streamlit as st
from utils.data_generator import load_loan_data, get_vintage_data
from utils.risk_analyzer import categorize_risk, get_risk_summary, calculate_risk_metrics
from components.portfolio_overview import render_portfolio_overview
from components.vintage_analysis import render_vintage_analysis
from components.risk_analysis import render_risk_analysis

st.set_page_config(
    page_title="AI-Powered Risk Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

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

tab1, tab2, tab3 = st.tabs([
    "Portfolio Overview",
    "Vintage Analysis",
    "Risk Analysis"
])

with tab1:
    render_portfolio_overview(df)

with tab2:
    render_vintage_analysis(df, vintage_data)

with tab3:
    render_risk_analysis(df, risk_summary)

# Add download functionality
if st.sidebar.button("Export Data"):
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="loan_portfolio.csv",
        mime="text/csv"
    )

# Add filters in sidebar
st.sidebar.header("Filters")
selected_platform = st.sidebar.selectbox(
    "Select Platform",
    ['All'] + sorted(df['platform'].unique().tolist())
)

if selected_platform != 'All':
    df = df[df['platform'] == selected_platform]
    st.experimental_rerun()