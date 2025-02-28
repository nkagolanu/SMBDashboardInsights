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

    # Count risk categories directly from the DataFrame
    if not df.empty:
        # Create a summary DataFrame that works with any number of platforms
        risk_counts = df.groupby('Risk Category').size().reset_index(name='count')
        risk_counts['percentage'] = risk_counts['count'] / len(df) * 100

        fig = go.Figure()
        for i, row in risk_counts.iterrows():
            risk_category = row['Risk Category']
            fig.add_trace(go.Bar(
                x=[risk_category],
                y=[row['percentage']],
                name=risk_category,
                marker_color=risk_colors.get(risk_category, '#808080')
            ))

        fig.update_layout(
            title='Risk Distribution',
            xaxis_title='Risk Category',
            yaxis_title='Percentage (%)',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected platform.")

    # At-risk loans
    st.subheader("High Risk Loans")
    high_risk_df = df[df['Risk Category'] != 'No Risk'].sort_values('Risk Category')

    st.dataframe(
        high_risk_df[['Business Name', 'Platform', 'Amount', 'Repaid Amount', 'Risk Category']]
        .head(10)
        .style.format({
            'Amount': '${:,.0f}',
            'Repaid Amount': '${:,.0f}'
        })
    )