import pandas as pd
import numpy as np


def load_loan_data():
    """Load loan data from CSV and transform for dashboard use"""
    try:
        # Print current directory for debugging
        import os
        print(f"Current directory: {os.getcwd()}")
        print(f"Files in attached_assets: {os.listdir('attached_assets')}")

        # Load CSV file
        file_path = 'attached_assets/pipe_final_data.csv'
        print(f"Attempting to load file: {file_path}")
        df = pd.read_csv(file_path)

        # Print column names for debugging
        print(f"CSV columns: {df.columns.tolist()}")
        
        # Print max loan amount with more details
        try:
            max_amount = df['Loan Amount'].max()
            print(f"Max loan amount: ${max_amount:,.0f}")
            print(f"Sample data: {df['Loan Amount'].head().tolist()}")
        except Exception as e:
            print(f"Error calculating max loan amount: {e}")
            print(f"Columns available: {df.columns.tolist()}")

        # Clean up column names for better code readability
        df = df.rename(
            columns={
                'Embedded Platform Name': 'platform',
                'SMB Name': 'business_name',
                'Loan Amount': 'amount',
                'Pipe Fees': 'fees',
                'Loan Funded On': 'funded_date',
                'Repaid Total So Far': 'repaid_amount',  # Fixed column name
                'Liquidity Risk': 'liquidity_risk',
                'Revenue Drop Risk': 'revenue_drop_risk',
                'Non-Payment Risk': 'non_payment_risk'
            })

        print("DataFrame head:")
        print(df.head())  # Use parentheses to actually call the method

        # Set risk category based on flags (mutually exclusive in this dataset)
        df['risk_category'] = 'No Risk'
        df.loc[df['liquidity_risk'] == 1, 'risk_category'] = 'Liquidity Risk'
        df.loc[df['revenue_drop_risk'] == 1,
               'risk_category'] = 'Revenue Drop Risk'
        df.loc[df['non_payment_risk'] == 1,
               'risk_category'] = 'Non-Payment Risk'

        # Convert loan date to datetime and create vintage
        df['funded_date'] = pd.to_datetime(df['funded_date'])

        # Create vintage using quarter calculation
        df['quarter'] = df['funded_date'].dt.quarter
        df['year'] = df['funded_date'].dt.year
        df['vintage'] = 'Q' + df['quarter'].astype(
            str) + ' ' + df['year'].astype(str)

        # Drop helper columns
        df = df.drop(['quarter', 'year'], axis=1)

        # Add default platform if missing
        if 'platform' not in df.columns:
            print(
                "Warning: 'platform' column not found in CSV, adding default value"
            )
            df['platform'] = 'Priority'  # Default platform

        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame if loading fails


def get_vintage_data(df):
    """Calculate vintage performance metrics"""
    if df.empty:
        return pd.DataFrame()

    # Group by vintage and calculate metrics
    vintage_data = df.groupby('vintage').agg({
        'amount': 'sum',
        'repaid_amount': 'sum'
    }).reset_index()

    # Calculate repayment rate
    vintage_data['repayment_rate'] = vintage_data[
        'repaid_amount'] / vintage_data['amount']
    
    # Add risk analysis metrics
    risk_by_vintage = df.groupby(['vintage', 'risk_category']).size().unstack(fill_value=0).reset_index()
    if 'Non-Payment Risk' in risk_by_vintage.columns:
        risk_by_vintage['total_loans'] = risk_by_vintage.drop('vintage', axis=1).sum(axis=1)
        risk_by_vintage['non_payment_risk_pct'] = (risk_by_vintage['Non-Payment Risk'] / 
                                                  risk_by_vintage['total_loans'] * 100)
        
        # Merge risk metrics with vintage data
        vintage_data = pd.merge(vintage_data, 
                              risk_by_vintage[['vintage', 'Non-Payment Risk', 'non_payment_risk_pct']], 
                              on='vintage', how='left')

    return vintage_data
