import pandas as pd
import numpy as np
from datetime import datetime

def load_loan_data():
    """Load loan data from CSV file"""
    df = pd.read_csv('attached_assets/Pipe_Risk_Analysis_Dataset.csv')

    # Convert date columns to datetime
    df['Loan Funded On'] = pd.to_datetime(df['Loan Funded On'])
    df['Repayment t-1 Date'] = pd.to_datetime(df['Repayment t-1 Date'])
    df['Repayment t-2 Date'] = pd.to_datetime(df['Repayment t-2 Date'])

    # Calculate repayment velocity and total repaid
    df['repaid_amount'] = df['Repayment t-1 Amount'] + df['Repayment t-2 Amount']
    df['repayment_velocity'] = df['repaid_amount'] / df['Loan Amount']

    # Convert risk flags to list
    df['risk_flags'] = df['Risk Flags'].fillna('None').str.split(', ')

    # Calculate revenue decline
    df['revenue_decline'] = (df['Revenue t-1 Amount'] < df['Revenue t-2 Amount'] * 0.5)

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