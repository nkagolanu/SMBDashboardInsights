import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render_risk_analysis(df, risk_summary):
    st.header("Risk Analysis")

    # Risk distribution
    st.subheader("Risk Distribution by Platform") 
    risk_colors = {
        'No Risk': '#808080',
        'Liquidity Risk': '#90EE90',
        'Revenue Drop Risk': '#FFA500',
        'Non-Payment Risk': '#FF4B4B'
    }

    # Count risk categories directly from the DataFrame
    if not df.empty:
        # Create a summary DataFrame that works with any number of platforms
        risk_counts = df.groupby('risk_category').size().reset_index(
            name='count')
        risk_counts['percentage'] = risk_counts['count'] / len(df) * 100

        fig = go.Figure()
        for i, row in risk_counts.iterrows():
            risk_category = row['risk_category']
            fig.add_trace(
                go.Bar(x=[risk_category],
                       y=[row['percentage']],
                       name=risk_category,
                       marker_color=risk_colors.get(risk_category, '#808080')))

        fig.update_layout(title='Risk Distribution',
                          xaxis_title='Risk Category',
                          yaxis_title='Percentage (%)',
                          barmode='group',
                          margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected platform.")

    # At-risk loans
    st.subheader("High Risk Loans")
    high_risk_df = df[df['risk_category'] != 'No Risk'].sort_values(
        'risk_category')

    st.dataframe(high_risk_df[[
        'business_name', 'platform', 'amount', 'repaid_amount', 'risk_category'
    ]].head(10).style.format({
        'amount': '${:,.0f}',
        'repaid_amount': '${:,.0f}'
    }))
