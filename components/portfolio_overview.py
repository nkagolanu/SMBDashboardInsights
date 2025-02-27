import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_portfolio_overview(df):
    st.header("Portfolio Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_deployed = df['amount'].sum()
        st.metric("Total Capital Deployed", f"${total_deployed:,.0f}")

    with col2:
        active_loans = len(df)
        st.metric("Active Advances", f"{active_loans:,}")

    with col3:
        avg_repayment = (df['repaid_amount'].sum() / df['amount'].sum()) * 100
        st.metric("Overall Repayment Rate", f"{avg_repayment:.1f}%")

    with col4:
        at_risk = len(df[df['Risk Flags'].notna() & (df['Risk Flags'] != 'None')])
        st.metric("Loans at Risk", f"{at_risk:,}")

    # Platform breakdown
    st.subheader("Advances by Platform")
    platform_fig = px.pie(
        df,
        values='amount',
        names='platform',
        title='Capital Deployment by Platform'
    )
    st.plotly_chart(platform_fig, use_container_width=True)

    # Repayment trends
    st.subheader("Repayment Performance")
    repayment_fig = go.Figure()
    for platform in df['platform'].unique():
        platform_data = df[df['platform'] == platform]
        repayment_fig.add_trace(go.Box(
            y=platform_data['repayment_velocity'],
            name=platform,
            boxpoints='all'
        ))
    repayment_fig.update_layout(
        title='Repayment Velocity Distribution by Platform',
        yaxis_title='Repayment Velocity'
    )
    st.plotly_chart(repayment_fig, use_container_width=True)

    # Risk distribution
    st.subheader("Risk Distribution")
    risk_counts = df['Risk Flags'].fillna('None').value_counts()
    risk_fig = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        title='Distribution of Risk Flags'
    )
    st.plotly_chart(risk_fig, use_container_width=True)