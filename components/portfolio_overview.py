import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_portfolio_overview(df):
    st.header("Portfolio Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_deployed = df['Amount'].sum()
        st.metric("Total Capital Deployed", f"${total_deployed:,.0f}")

    with col2:
        active_loans = len(df)
        st.metric("Active Advances", f"{active_loans:,}")

    with col3:
        avg_repayment = (df['Repaid Amount'].sum() / df['Amount'].sum()) * 100
        st.metric("Overall Repayment Rate", f"{avg_repayment:.1f}%")

    with col4:
        at_risk = len(df[df['risk_category'] != 'No Risk'])
        st.metric("Loans at Risk", f"{at_risk:,}")

    # Repayment trends
    st.subheader("Repayment Performance")
    repayment_fig = go.Figure()
    for platform in df['Platform'].unique():
        platform_data = df[df['Platform'] == platform]
        repayment_fig.add_trace(go.Box(
            y=platform_data['repayment_rate'],  # Changed from repayment_velocity to repayment_rate
            name=platform,
            boxpoints='all'
        ))
    repayment_fig.update_layout(
        title='Repayment Rate Distribution by Platform',
        yaxis_title='Repayment Rate'
    )
    st.plotly_chart(repayment_fig, use_container_width=True)

    # Risk distribution
    st.subheader("Risk Distribution")
    risk_counts = df['risk_category'].value_counts()
    risk_fig = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        title='Distribution of Risk Flags',
        color=risk_counts.index,
        color_discrete_map={
            'No Risk': '#808080',
            'Liquidity Risk 🟢': '#90EE90',
            'Revenue Drop Risk 🟠': '#FFA500',
            'Non-Payment Risk 🔴': '#FF4B4B'
        }
    )
    st.plotly_chart(risk_fig, use_container_width=True)