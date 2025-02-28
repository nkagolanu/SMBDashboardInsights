import pandas as pd
import numpy as np


def load_loan_data():
    """Load loan data from CSV and transform for dashboard use"""
    try:
        # Load CSV file
        df = pd.read_csv('attached_assets/pipe_risk_analysis_with_repaid.csv')

        # Clean up column names for better code readability
        df = df.rename(
            columns={
                'Embedded Platform Name': 'platform',
                'SMB Name': 'business_name',
                'Loan Amount': 'amount',
                'Pipe Fees': 'fees',
                'Loan Funded On': 'funded_date',
                'Repaid Total So Far': 'repayment_amount',
                'Liquidity Risk': 'liquidity_risk',
                'Revenue Drop Risk': 'revenue_drop_risk',
                'Non-Payment Risk': 'non_payment_risk'
            })

        # Set risk category based on flags (mutually exclusive in this dataset)
        df['risk_category'] = 'No Risk'
        df.loc[df['liquidity_risk'] == 1, 'risk_category'] = 'Liquidity Risk'
        df.loc[df['revenue_drop_risk'] == 1,
               'risk_category'] = 'Revenue Drop Risk'
        df.loc[df['non_payment_risk'] == 1,
               'risk_category'] = 'Non-Payment Risk'

        # Convert loan date to datetime and create vintage
        df['funded_date'] = pd.to_datetime(df['funded_date'])
        df['vintage'] = df['loan_funded_on'].dt.strftime('Q%q %Y')

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

    return vintage_data
