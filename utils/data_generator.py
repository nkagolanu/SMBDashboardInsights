import pandas as pd
import numpy as np
from datetime import datetime


def load_loan_data():
    """Load loan data from CSV file"""
    df = pd.read_csv('attached_assets/pipe_risk_analysis_with_repaid.csv')

    # Convert date columns to datetime
    df['Loan Funded On'] = pd.to_datetime(df['Loan Funded On'])

    # Calculate repayment velocity and total repaid
    df['repayment_rate'] = df['Repaid Total So Far'] / df['Loan Amount']

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
    
    # Create Vintage column in Q# YYYY format
    def get_quarter_year(date):
        quarter = f"Q{(date.month-1)//3+1} {date.year}"
        return quarter
        
    # Use 'Loan Funded On' instead of 'Date Funded' since that's the column we have
    df['Vintage'] = df['Loan Funded On'].apply(get_quarter_year)

    # Clean up column names
    df = df.rename(
        columns={
            'Embedded Platform Name': 'Platform',
            'SMB Name': 'Business Name',
            'Loan Funded On': 'Date Funded',
            'Loan Amount': 'Amount',
            'Pipe Fees': 'Pipe Fees',
            'Repaid Total So Far': 'Repaid Amount'
        })

    return df


def get_vintage_data(df):
    """Convert loan data into vintage analysis format"""
    # Use 'Vintage' column we created in load_loan_data
    if 'Vintage' not in df.columns:
        # Create Vintage column if it doesn't exist yet
        df['Vintage'] = df['Date Funded'].apply(lambda date: f"Q{(date.month-1)//3+1} {date.year}")

    # Make sure we're using the renamed column names from load_loan_data
    vintage_summary = df.groupby('Vintage').agg({
        'Amount': 'sum',
        'Repaid Amount': 'sum',
        'Business Name': 'count'
    }).reset_index()

    vintage_summary['repayment_rate'] = vintage_summary[
        'Repaid Amount'] / vintage_summary['Amount']
    return vintage_summary
