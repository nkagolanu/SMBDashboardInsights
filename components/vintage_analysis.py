import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_vintage_analysis(df, vintage_data):
    st.header("Vintage & Cohort Analysis")
    
    # Platform filter
    selected_platform = st.selectbox(
        "Select Platform",
        ['All'] + list(df['platform'].unique())
    )
    
    filtered_df = df
    if selected_platform != 'All':
        filtered_df = df[df['platform'] == selected_platform]
    
    # Vintage performance chart
    st.subheader("Vintage Performance")
    vintage_fig = px.line(
        vintage_data,
        x='vintage',
        y='repayment_rate',
        title='Repayment Rate by Vintage'
    )
    st.plotly_chart(vintage_fig, use_container_width=True)
    
    # Cohort table
    st.subheader("Vintage Cohort Analysis")
    cohort_metrics = filtered_df.groupby('vintage').agg({
        'amount': 'sum',
        'repaid_amount': 'sum',
        'loan_id': 'count'
    }).reset_index()
    
    cohort_metrics['repayment_rate'] = (
        cohort_metrics['repaid_amount'] / cohort_metrics['amount']
    )
    
    st.dataframe(
        cohort_metrics.style.format({
            'amount': '${:,.0f}',
            'repaid_amount': '${:,.0f}',
            'repayment_rate': '{:.1%}'
        })
    )
