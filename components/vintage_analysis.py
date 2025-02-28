import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render_vintage_analysis(df, vintage_data):
    st.header("Vintage & Cohort Analysis")

    # Vintage performance chart
    st.subheader("Vintage Performance")
    vintage_fig = px.line(vintage_data,
                          x='vintage',
                          y='repayment_rate',
                          title='Repayment Rate by Vintage')
    st.plotly_chart(vintage_fig, use_container_width=True)

    # Cohort table
    st.subheader("Vintage Cohort Analysis")
    cohort_metrics = df.groupby('vintage').agg({
        'Amount': 'sum',
        'Repaid Amount': 'sum',
        'Business Name': 'count'
    }).reset_index()

    cohort_metrics['Repayment Rate'] = (cohort_metrics['Repaid Amount'] /
                                        cohort_metrics['Amount'])

    st.dataframe(
        cohort_metrics.style.format({
            'Amount': '${:,.0f}',
            'Repaid Amount': '${:,.0f}',
            'Repayment Rate': '{:.1%}'
        }))
