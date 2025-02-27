import streamlit as st
from utils.data_generator import generate_loan_data, get_vintage_data
from utils.risk_analyzer import calculate_risk_score, get_risk_summary
from components.portfolio_overview import render_portfolio_overview
from components.vintage_analysis import render_vintage_analysis
from components.risk_analysis import render_risk_analysis

st.set_page_config(
    page_title="AI-Powered Risk Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# Generate mock data
@st.cache_data
def load_data():
    df = generate_loan_data()
    df['risk_score'] = calculate_risk_score(df)
    vintage_data = get_vintage_data(df)
    risk_summary = get_risk_summary(df)
    return df, vintage_data, risk_summary

# Load data
df, vintage_data, risk_summary = load_data()

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
st.sidebar.warning("Note: Filters coming in next release")
