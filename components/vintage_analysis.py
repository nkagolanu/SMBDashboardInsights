import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_vintage_analysis(df, vintage_data):
    st.header("Vintage & Cohort Analysis")

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
    cohort_metrics = df.groupby('vintage').agg({
        'amount': 'sum',
        'repaid_amount': 'sum',
        'business_name': 'count'
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