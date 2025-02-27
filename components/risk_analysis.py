import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_risk_analysis(df, risk_summary):
    st.header("Risk Analysis")
    
    # Risk distribution
    st.subheader("Risk Distribution by Platform")
    risk_fig = px.bar(
        risk_summary.reset_index(),
        x='platform',
        y=['Low Risk', 'Medium Risk - Revenue Decline', 'High Risk - Slow Repayment', 'High Risk - No Payment'],
        title='Risk Distribution Across Platforms',
        barmode='stack'
    )
    st.plotly_chart(risk_fig, use_container_width=True)
    
    # At-risk loans
    st.subheader("High Risk Loans")
    high_risk_df = df[
        (df['days_no_payment'] >= 60) |
        (df['repayment_velocity'] < 0.3) |
        (df['revenue_decline'])
    ].sort_values('days_no_payment', ascending=False)
    
    st.dataframe(
        high_risk_df[['platform', 'amount', 'repaid_amount', 'days_no_payment', 'risk_category']]
        .head(10)
        .style.format({
            'amount': '${:,.0f}',
            'repaid_amount': '${:,.0f}'
        })
    )
