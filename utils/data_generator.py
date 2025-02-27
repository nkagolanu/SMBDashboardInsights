import pandas as pd
import numpy as np
from datetime import datetime

def load_loan_data():
    """Load loan data from CSV file"""
    df = pd.read_csv('attached_assets/pipe_risk_analysis_data_final_exclusive.csv')

    # Convert date columns to datetime
    df['Loan Funded On'] = pd.to_datetime(df['Loan Funded On'])
    df['Repayment t-1 Date'] = pd.to_datetime(df['Repayment t-1 Date'])
    df['Repayment t-2 Date'] = pd.to_datetime(df['Repayment t-2 Date'])

    # Calculate repayment velocity and total repaid
    df['repaid_amount'] = df['Repayment t-1 Amount'] + df['Repayment t-2 Amount']
    df['repayment_velocity'] = df['repaid_amount'] / df['Loan Amount']

    # Convert boolean risk flags
    df['liquidity_risk'] = df['Liquidity Risk'].astype(bool)
    df['revenue_drop_risk'] = df['Revenue Drop Risk'].astype(bool)
    df['non_payment_risk'] = df['Non-Payment Risk'].astype(bool)

    # Create risk category
    def get_risk_category(row):
        if row['non_payment_risk']:
            return 'Non-Payment Risk 🔴'
        elif row['revenue_drop_risk']:
            return 'Revenue Drop Risk 🟠'
        elif row['liquidity_risk']:
            return 'Liquidity Risk 🟢'
        else:
            return 'No Risk'

    df['risk_category'] = df.apply(get_risk_category, axis=1)

    # Clean up column names
    df = df.rename(columns={
        'Embedded Platform Name': 'platform',
        'SMB Name': 'business_name',
        'Loan Funded On': 'start_date',
        'Loan Amount': 'amount',
        'Pipe Fees': 'fees'
    })

    return df

def get_vintage_data(df):
    """Convert loan data into vintage analysis format"""
    df['vintage'] = df['start_date'].dt.strftime('%Y-%m')
    vintage_summary = df.groupby('vintage').agg({
        'amount': 'sum',
        'repaid_amount': 'sum',
        'business_name': 'count'
    }).reset_index()
    vintage_summary['repayment_rate'] = vintage_summary['repaid_amount'] / vintage_summary['amount']
    return vintage_summary