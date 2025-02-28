import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def analyze_repayment_velocity(df):
    """Analyze the repayment velocity across different vintages"""
    if df.empty or 'repaid_amount' not in df.columns or 'amount' not in df.columns:
        return pd.DataFrame()
    
    # Calculate repayment percentage for each loan
    df_copy = df.copy()
    df_copy['repayment_pct'] = df_copy['repaid_amount'] / df_copy['amount'] * 100
    
    # Group by vintage and calculate velocity metrics
    velocity_data = df_copy.groupby('vintage').agg({
        'repayment_pct': ['mean', 'median', 'std', 'count'],
        'amount': 'sum',
        'repaid_amount': 'sum'
    })
    
    # Flatten the multi-index columns
    velocity_data.columns = ['avg_repayment_pct', 'median_repayment_pct', 
                             'std_repayment_pct', 'loan_count', 
                             'total_amount', 'total_repaid']
    
    # Calculate overall repayment rate
    velocity_data['overall_repayment_rate'] = velocity_data['total_repaid'] / velocity_data['total_amount'] * 100
    
    # Reset index to make vintage a column
    velocity_data = velocity_data.reset_index()
    
    # Sort by vintage chronologically
    def vintage_sort_key(vintage_str):
        # Parse 'Q1 2024' format into a sortable value
        try:
            quarter = int(vintage_str[1])
            year = int(vintage_str.split()[1])
            return year * 10 + quarter
        except:
            return 0  # Default for any unparseable vintages
            
    velocity_data['sort_key'] = velocity_data['vintage'].apply(vintage_sort_key)
    velocity_data = velocity_data.sort_values('sort_key')
    velocity_data = velocity_data.drop('sort_key', axis=1)
    
    return velocity_data


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

        # Sort by vintage chronologically 
        def vintage_sort_key(vintage_str):
            # Parse 'Q1 2024' format into a sortable value
            try:
                quarter = int(vintage_str[1])
                year = int(vintage_str.split()[1])
                return year * 10 + quarter
            except:
                return 0  # Default for any unparseable vintages
                
        vintage_risk['sort_key'] = vintage_risk['vintage'].apply(vintage_sort_key)
        vintage_risk = vintage_risk.sort_values('sort_key')
        vintage_risk = vintage_risk.drop('sort_key', axis=1)

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
        
        # Repayment Velocity Analysis
        st.markdown("---")
        st.subheader("Repayment Velocity Analysis")
        
        velocity_data = analyze_repayment_velocity(df)
        
        if not velocity_data.empty:
            # Create charts for repayment velocity
            col1, col2 = st.columns(2)
            
            with col1:
                # Overall repayment rate by vintage
                fig1 = px.line(velocity_data, 
                              x='vintage', 
                              y='overall_repayment_rate',
                              title='Overall Repayment Rate by Vintage',
                              markers=True,
                              color_discrete_sequence=['#4682B4'])
                fig1.update_layout(yaxis_title='Repayment Rate (%)',
                                  margin=dict(t=30, b=0, l=0, r=0))
                st.plotly_chart(fig1, use_container_width=True)
                
                # Identify trends
                latest_vintages = velocity_data.tail(3)['vintage'].tolist()
                latest_rates = velocity_data.tail(3)['overall_repayment_rate'].tolist()
                
                if len(latest_rates) >= 2:
                    if latest_rates[-1] > latest_rates[-2]:
                        st.success(f"👍 Latest vintage ({latest_vintages[-1]}) shows improved repayment rate compared to previous vintage.")
                    elif latest_rates[-1] < latest_rates[-2]:
                        st.warning(f"⚠️ Latest vintage ({latest_vintages[-1]}) shows decreased repayment rate compared to previous vintage.")
            
            with col2:
                # Loan-level repayment analysis
                fig2 = px.bar(velocity_data,
                             x='vintage',
                             y=['avg_repayment_pct', 'median_repayment_pct'],
                             title='Average vs Median Repayment Percentage by Vintage',
                             barmode='group',
                             color_discrete_sequence=['#90EE90', '#FFA500'])
                fig2.update_layout(yaxis_title='Repayment Percentage (%)',
                                  margin=dict(t=30, b=0, l=0, r=0),
                                  legend_title_text='Metric')
                st.plotly_chart(fig2, use_container_width=True)
            
            # Detailed velocity metrics table
            st.write("**Detailed Repayment Velocity Metrics**")
            
            # Format the table columns for better readability
            display_velocity = velocity_data.copy()
            for col in ['avg_repayment_pct', 'median_repayment_pct', 'overall_repayment_rate']:
                display_velocity[col] = display_velocity[col].round(1).astype(str) + '%'
            
            display_velocity['total_amount'] = display_velocity['total_amount'].apply(lambda x: f"${x:,.0f}")
            display_velocity['total_repaid'] = display_velocity['total_repaid'].apply(lambda x: f"${x:,.0f}")
            
            # Display table with key metrics
            st.dataframe(display_velocity[[
                'vintage', 'loan_count', 'total_amount', 'total_repaid',
                'avg_repayment_pct', 'median_repayment_pct', 'overall_repayment_rate'
            ]], use_container_width=True)
            
            # Key insights
            st.markdown("### Key Insights")
            
            # Find vintage with highest repayment rate
            best_vintage = velocity_data.loc[velocity_data['overall_repayment_rate'].idxmax()]
            worst_vintage = velocity_data.loc[velocity_data['overall_repayment_rate'].idxmin()]
            
            st.write(f"✅ **Best performing vintage**: {best_vintage['vintage']} with {best_vintage['overall_repayment_rate']:.1f}% repayment rate")
            st.write(f"⚠️ **Worst performing vintage**: {worst_vintage['vintage']} with {worst_vintage['overall_repayment_rate']:.1f}% repayment rate")
            
            # Calculate repayment velocity over time
            if len(velocity_data) > 2:
                velocity_trend = np.polyfit(range(len(velocity_data)), velocity_data['overall_repayment_rate'], 1)[0]
                if velocity_trend > 0:
                    st.success(f"📈 Overall repayment velocity is **increasing** across vintages at approximately {abs(velocity_trend):.2f}% per vintage")
                elif velocity_trend < 0:
                    st.warning(f"📉 Overall repayment velocity is **decreasing** across vintages at approximately {abs(velocity_trend):.2f}% per vintage")
                else:
                    st.info("➡️ Overall repayment velocity is relatively stable across vintages")
        else:
            st.write("Insufficient data to analyze repayment velocity.")