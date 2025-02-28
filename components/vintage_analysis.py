
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


import streamlit as st
import plotly.express as px
import pandas as pd

def render_vintage_analysis(df, vintage_data):
    st.header("Vintage & Cohort Analysis")

    # Vintage performance chart
    st.subheader("Vintage Performance")
    
    # Check if vintage_data has required columns
    if 'vintage' in vintage_data.columns and 'repayment_rate' in vintage_data.columns:
        vintage_fig = px.line(vintage_data,
                            x='vintage',
                            y='repayment_rate',
                            title='Repayment Rate by Vintage')
        st.plotly_chart(vintage_fig, use_container_width=True)
    else:
        st.warning("Missing required columns for vintage analysis.")

    # Cohort table
    st.subheader("Vintage Cohort Analysis")
    
    # Dynamically get column names for consistency
    amount_col = 'Amount' if 'Amount' in df.columns else 'amount'
    repaid_col = 'Repaid Amount' if 'Repaid Amount' in df.columns else 'repaid_amount'
    business_col = 'Business Name' if 'Business Name' in df.columns else 'business_name'
    vintage_col = 'Vintage' if 'Vintage' in df.columns else 'vintage'
    
    # Check if the Vintage column exists
    if vintage_col in df.columns:
        # Check what columns are available and adjust accordingly
        agg_dict = {}
        if amount_col in df.columns:
            agg_dict[amount_col] = 'sum'
        if repaid_col in df.columns:
            agg_dict[repaid_col] = 'sum'
        if business_col in df.columns:
            agg_dict[business_col] = 'count'
        
        if agg_dict:  # Only proceed if we have columns to aggregate
            cohort_metrics = df.groupby(vintage_col).agg(agg_dict).reset_index()
            
            # Calculate repayment rate if both columns exist
            if amount_col in cohort_metrics.columns and repaid_col in cohort_metrics.columns:
                cohort_metrics['Repayment Rate'] = (cohort_metrics[repaid_col] /
                                                cohort_metrics[amount_col])
                
                # Format display
                st.dataframe(
                    cohort_metrics.style.format({
                        amount_col: '${:,.0f}',
                        repaid_col: '${:,.0f}',
                        'Repayment Rate': '{:.1%}'
                    }))
            else:
                st.dataframe(cohort_metrics)
        else:
            st.warning("No suitable columns found for cohort analysis.")
    else:
        st.warning("Vintage column not found in dataset.")
