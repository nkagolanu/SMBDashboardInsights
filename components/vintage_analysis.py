import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_vintage_analysis(df, vintage_data):
    st.subheader("Vintage & Cohort Analysis")
    if not df.empty and 'vintage' in df.columns and 'risk_category' in df.columns:
        # Group by vintage and count risk categories
        vintage_risk = df.groupby(
            ['vintage',
             'risk_category']).size().unstack(fill_value=0).reset_index()

        # Ensure 'Non-Payment Risk' column exists
        if 'Non-Payment Risk' not in vintage_risk.columns:
            vintage_risk['Non-Payment Risk'] = 0

        # Calculate total loans per vintage for percentage
        vintage_risk['Total Loans'] = vintage_risk.drop('vintage',
                                                        axis=1).sum(axis=1)
        vintage_risk['Non-Payment Risk %'] = (
            vintage_risk['Non-Payment Risk'] / vintage_risk['Total Loans'] *
            100).round(1)

        # Sort by vintage
        vintage_risk = vintage_risk.sort_values('vintage')

        # Identify highest risk vintages
        high_risk_vintages = vintage_risk.sort_values('Non-Payment Risk %',
                                                      ascending=False).head(3)
        st.write("Top 3 vintages with highest percentage of Non-Payment Risk:")
        for _, row in high_risk_vintages.iterrows():
            st.write(
                f"**{row['vintage']}**: {row['Non-Payment Risk %']}% of loans ({row['Non-Payment Risk']} out of {row['Total Loans']} loans)"
            )

        # Create risk analysis charts

        fig2 = px.line(vintage_risk,
                       x='vintage',
                       y='Non-Payment Risk %',
                       title='Percentage of Non-Payment Risk Loans by Vintage',
                       markers=True,
                       color_discrete_sequence=['#FF4B4B'])
        fig2.update_layout(yaxis_title='Non-Payment Risk %',
                           margin=dict(t=30, b=0, l=0, r=0))

        # Display charts
        st.plotly_chart(fig2, use_container_width=True)

        # Display data table with all risk categories
        st.write("**Vintage Risk Breakdown**")
        risk_columns = [
            col for col in vintage_risk.columns
            if col != 'vintage' and 'Risk' in col and '%' not in col
        ]
        display_cols = ['vintage'] + risk_columns + ['Total Loans']

        st.dataframe(vintage_risk[display_cols], use_container_width=True)