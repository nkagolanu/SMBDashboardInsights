import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_portfolio_overview(df):
    st.header("Portfolio Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_deployed = df['Amount'].sum()
        st.metric("Total Capital Deployed", f"${total_deployed:,.0f}")

    with col2:
        total_returned = df['Repaid Amount'].sum()
        st.metric("Total Capital Returned", f"${total_returned:,.0f}")

    with col3:
        # Assuming there's a fees column, otherwise calculating a percentage
        if 'Fees' in df.columns:
            total_fees = df['Pipe Fees'].sum()
        else:
            # Calculate fees as 5% of repaid amount (example calculation)
            total_fees = df['Repaid Amount'].sum() * 0.05
        st.metric("Total Fees Collected", f"${total_fees:,.0f}")

    # Loan distribution by size
    st.subheader("Loan Distribution by Size")

    # Create size categories
    def categorize_loan_size(amount):
        if amount >= 10000 and amount < 50000:
            return "Small ($10K-$50K)"
        elif amount >= 50000 and amount < 150000:
            return "Medium ($50K-$150K)"
        elif amount >= 150000 and amount <= 300000:
            return "Large ($150K-$300K)"
        else:
            return "Other"

    # Apply categorization
    df['Loan Size Category'] = df['Amount'].apply(categorize_loan_size)

    # Filter out "Other" category if needed
    size_df = df[df['Loan Size Category'] != "Other"]

    # Count by category
    size_counts = size_df['Loan Size Category'].value_counts().reset_index()
    size_counts.columns = ['Loan Size Category', 'Count']

    # Ensure proper order
    category_order = [
        "Small ($10K-$50K)", "Medium ($50K-$150K)", "Large ($150K-$300K)"
    ]
    size_counts['Loan Size Category'] = pd.Categorical(
        size_counts['Loan Size Category'],
        categories=category_order,
        ordered=True)
    size_counts = size_counts.sort_values('Loan Size Category')

    # Create the bar chart
    size_fig = px.bar(
        size_counts,
        x='Loan Size Category',
        y='Count',
        title='Distribution of Loans by Size',
        color='Loan Size Category',
        color_discrete_map={
            "Small ($10K-$50K)": "#90EE90",  # Light green
            "Medium ($50K-$150K)": "#4682B4",  # Steel blue
            "Large ($150K-$300K)": "#FFD700"  # Gold
        })
    size_fig.update_layout(xaxis_title='Loan Size Category',
                           yaxis_title='Number of Loans')
    st.plotly_chart(size_fig, use_container_width=True)

    # Risk distribution
    st.subheader("Risk Distribution")
    risk_counts = df['Risk Category'].value_counts()
    risk_fig = px.bar(x=risk_counts.index,
                      y=risk_counts.values,
                      title='Distribution of Risk Flags',
                      color=risk_counts.index,
                      color_discrete_map={
                          'No Risk': '#808080',
                          'Liquidity Risk 🟢': '#90EE90',
                          'Revenue Drop Risk 🟠': '#FFA500',
                          'Non-Payment Risk 🔴': '#FF4B4B'
                      })
    st.plotly_chart(risk_fig, use_container_width=True)
