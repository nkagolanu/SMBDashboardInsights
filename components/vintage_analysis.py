
import streamlit as st
import plotly.express as px
import pandas as pd

def render_vintage_analysis(df, vintage_data):
    st.header("Vintage & Cohort Analysis")

    # Create a new vintage-based risk analysis
    st.subheader("Vintage Risk Analysis")
    
    if not df.empty and 'vintage' in df.columns and 'risk_category' in df.columns:
        # Group by vintage and count risk categories
        vintage_risk = df.groupby(['vintage', 'risk_category']).size().unstack(fill_value=0).reset_index()
        
        # Ensure 'Non-Payment Risk' column exists
        if 'Non-Payment Risk' not in vintage_risk.columns:
            vintage_risk['Non-Payment Risk'] = 0
        
        # Calculate total loans per vintage for percentage
        vintage_risk['Total Loans'] = vintage_risk.drop('vintage', axis=1).sum(axis=1)
        vintage_risk['Non-Payment Risk %'] = (vintage_risk['Non-Payment Risk'] / vintage_risk['Total Loans'] * 100).round(1)
        
        # Sort by vintage
        vintage_risk = vintage_risk.sort_values('vintage')
        
        # Create risk analysis charts
        fig1 = px.bar(vintage_risk, 
                    x='vintage', 
                    y='Non-Payment Risk',
                    title='Number of Non-Payment Risk Loans by Vintage',
                    color_discrete_sequence=['#FF4B4B'])
        
        fig2 = px.line(vintage_risk, 
                      x='vintage', 
                      y='Non-Payment Risk %',
                      title='Percentage of Non-Payment Risk Loans by Vintage',
                      markers=True,
                      color_discrete_sequence=['#FF4B4B'])
        fig2.update_layout(yaxis_title='Non-Payment Risk %')
        
        # Display charts
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Display data table with all risk categories
        st.subheader("Vintage Risk Breakdown")
        risk_columns = [col for col in vintage_risk.columns if col != 'vintage' and 'Risk' in col and '%' not in col]
        display_cols = ['vintage'] + risk_columns + ['Total Loans', 'Non-Payment Risk %']
        
        st.dataframe(vintage_risk[display_cols], use_container_width=True)
        
        # Identify highest risk vintages
        st.subheader("Highest Risk Vintages")
        high_risk_vintages = vintage_risk.sort_values('Non-Payment Risk %', ascending=False).head(3)
        st.write("Top 3 vintages with highest percentage of Non-Payment Risk:")
        for _, row in high_risk_vintages.iterrows():
            st.write(f"**{row['vintage']}**: {row['Non-Payment Risk %']}% of loans ({row['Non-Payment Risk']} out of {row['Total Loans']} loans)")
            
        # Show detailed loan data for highest risk vintage
        if not high_risk_vintages.empty:
            highest_risk_vintage = high_risk_vintages.iloc[0]['vintage']
            st.subheader(f"Detailed Non-Payment Risk Loans for {highest_risk_vintage}")
            high_risk_loans = df[(df['vintage'] == highest_risk_vintage) & 
                                 (df['risk_category'] == 'Non-Payment Risk')]
            
            display_cols = ['business_name', 'platform', 'amount', 'funded_date', 'risk_category']
            display_cols = [col for col in display_cols if col in high_risk_loans.columns]
            
            st.dataframe(high_risk_loans[display_cols].head(10), use_container_width=True)
    else:
        st.warning("Missing required data for vintage risk analysis.")
