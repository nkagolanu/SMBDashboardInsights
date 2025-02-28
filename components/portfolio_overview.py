import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_portfolio_overview(df, platform_name="All"):
    st.header(f"{platform_name} Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_deployed = df['amount'].sum()
        st.metric("Total Capital Deployed", f"${total_deployed:,.0f}")

    with col2:
        total_returned = df['repaid_amount'].sum()
        st.metric("Total Capital Returned", f"${total_returned:,.0f}")

    with col3:
        total_fees = df['fees'].sum()
        st.metric("Total Fees Collected", f"${total_fees:,.0f}")

    col1, col2, col3 = st.columns(3)
    with col1:
        total_outstanding_loans = df['amount'].count()
        st.metric("Total Outstanding Loans", f"{total_outstanding_loans}")

    with col2:
        avg_loan_amount = df['amount'].mean()
        st.metric("Average Loan Amount", f"${avg_loan_amount:,.0f}")

    # Loan distribution by size
    st.markdown("---")
    st.subheader("Loan Distribution by Size")

    # Create size categories
    def categorize_loan_size(amount):
        if amount >= 10000 and amount < 50000:
            return "Small ($10K-$50K)"
        elif amount >= 50000 and amount < 150000:
            return "Medium ($50K-$150K)"
        elif amount >= 150000:
            return "Large (>$150K)"
        else:
            return "Other"

    # Apply categorization
    df['loan_size_category'] = df['amount'].apply(categorize_loan_size)

    # Filter out "Other" category if needed
    size_df = df[df['loan_size_category'] != "Other"]

    # Count by category
    size_counts = size_df['loan_size_category'].value_counts().reset_index()
    size_counts.columns = ['loan_size_category', 'Count']

    # Ensure proper order
    category_order = [
        "Small ($10K-$50K)", "Medium ($50K-$150K)", "Large (>$150K)"
    ]
    size_counts['loan_size_category'] = pd.Categorical(
        size_counts['loan_size_category'],
        categories=category_order,
        ordered=True)
    size_counts = size_counts.sort_values('loan_size_category')

    # Create the bar chart
    size_fig = px.bar(
        size_counts,
        x='loan_size_category',
        y='Count',
        title='',
        color='loan_size_category',
        color_discrete_map={
            "Small ($10K-$50K)": "#90EE90",  # Light green
            "Medium ($50K-$150K)": "#4682B4",  # Steel blue
            "Large (>$150K)": "#FFD700"  # Gold
        })
    size_fig.update_layout(xaxis_title='Loan Size Category',
                           yaxis_title='Number of Loans',
                           margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(size_fig, use_container_width=True)

    st.markdown("---")

    # Risk distribution as pie chart
    st.subheader("Risk Distribution")
    risk_counts = df['risk_category'].value_counts()
    risk_fig = px.pie(values=risk_counts.values,
                      names=risk_counts.index,
                      title='',
                      color=risk_counts.index,
                      color_discrete_map={
                          'No Risk': '#808080',
                          'Liquidity Risk': '#90EE90',
                          'Revenue Drop Risk': '#FFA500',
                          'Non-Payment Risk': '#FF4B4B'
                      })
    risk_fig.update_traces(textposition='inside', textinfo='percent+label')
    risk_fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(risk_fig, use_container_width=True)
    st.markdown("---")
