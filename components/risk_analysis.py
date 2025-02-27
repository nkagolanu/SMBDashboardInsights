import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.risk_analyzer import get_risk_category_table

def render_risk_analysis(df, risk_summary):
    st.header("Risk Analysis")

    # Risk Category Explanation
    st.subheader("Risk Categories Explained")
    risk_table = get_risk_category_table()
    st.dataframe(
        risk_table,
        column_config={
            "Risk Category": st.column_config.Column(width="medium"),
            "Definition": st.column_config.TextColumn(width="large", max_chars=300),
            "Severity": st.column_config.Column(width="small")
        },
        hide_index=True,
        use_container_width=True
    )

    # Risk distribution
    st.subheader("Risk Distribution by Platform")
    risk_colors = {
        'No Risk': '#808080',
        'Liquidity Risk 🟢': '#90EE90',
        'Revenue Drop Risk 🟠': '#FFA500',
        'Non-Payment Risk 🔴': '#FF4B4B'
    }

    risk_fig = px.bar(
        risk_summary.reset_index(),
        x='platform',
        y=['No Risk', 'Liquidity Risk 🟢', 'Revenue Drop Risk 🟠', 'Non-Payment Risk 🔴'],
        title='Risk Distribution Across Platforms',
        barmode='stack',
        color_discrete_map=risk_colors
    )
    st.plotly_chart(risk_fig, use_container_width=True)

    # At-risk loans
    st.subheader("High Risk Loans")
    high_risk_df = df[df['risk_category'] != 'No Risk'].sort_values('risk_category')

    st.dataframe(
        high_risk_df[['business_name', 'platform', 'amount', 'repaid_amount', 'risk_category']]
        .head(10)
        .style.format({
            'amount': '${:,.0f}',
            'repaid_amount': '${:,.0f}'
        })
    )