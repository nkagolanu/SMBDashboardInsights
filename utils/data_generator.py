import pandas as pd
import numpy as np
from datetime import datetime


def load_loan_data():
    """Load loan data from CSV or create synthetic data"""
    try:
        # Try to load from a CSV file
        df = pd.read_csv('attached_assets/pipe_risk_analysis_with_repaid.csv')

        # Adjust financial values by dividing by 10
        if 'Amount' in df.columns:
            df['Amount'] = df['Amount'] / 10
        if 'Repaid Amount' in df.columns:
            df['Repaid Amount'] = df['Repaid Amount'] / 10
        if 'Pipe Fees' in df.columns:
            df['Pipe Fees'] = df['Pipe Fees'] / 10

        # Add risk flags if missing
        if 'liquidity_risk' not in df.columns:
            df['liquidity_risk'] = False
        if 'revenue_drop_risk' not in df.columns:
            df['revenue_drop_risk'] = False
        if 'non_payment_risk' not in df.columns:
            df['non_payment_risk'] = False

        # Ensure Risk Category exists
        if 'Risk Category' not in df.columns:
            df['Risk Category'] = 'No Risk'
            # Set risk categories based on flags
            df.loc[df['liquidity_risk'], 'Risk Category'] = 'Liquidity Risk 🟢'
            df.loc[df['revenue_drop_risk'], 'Risk Category'] = 'Revenue Drop Risk 🟠'
            df.loc[df['non_payment_risk'], 'Risk Category'] = 'Non-Payment Risk 🔴'

        return df
    except FileNotFoundError:
        print("CSV file not found. Using synthetic data.")
        # Generate synthetic data if the CSV file is not found
        num_rows = 100
        df = pd.DataFrame({
            'Date Funded': pd.to_datetime(['2023-01-15'] * num_rows),
            'Platform': ['Platform A'] * num_rows,
            'Business Name': ['Business ' + str(i) for i in range(1, num_rows + 1)],
            'Amount': np.random.randint(1000, 10000, num_rows) / 10,  # Adjust to be smaller
            'Pipe Fees': np.random.randint(100, 500, num_rows) / 10,  # Adjust to be smaller
            'Repaid Amount': np.random.randint(0, 10000, num_rows) / 10,  # Adjust to be smaller
            'Liquidity Risk': np.random.choice([True, False], num_rows),
            'Revenue Drop Risk': np.random.choice([True, False], num_rows),
            'Non-Payment Risk': np.random.choice([True, False], num_rows)

        })
        # Convert date columns to datetime
        df['Date Funded'] = pd.to_datetime(df['Date Funded'])
        return df


def get_vintage_data(df):
    """Convert loan data into vintage analysis format"""
    # Check which date column is available
    date_column = None
    if 'Date Funded' in df.columns:
        date_column = 'Date Funded'
    elif 'Loan Funded On' in df.columns:
        date_column = 'Loan Funded On'
    
    # Use 'Vintage' column we created in load_loan_data
    if 'Vintage' not in df.columns and date_column is not None:
        # Create Vintage column if it doesn't exist yet
        df['Vintage'] = df[date_column].apply(lambda date: f"Q{(date.month-1)//3+1} {date.year}")
    elif 'Vintage' not in df.columns:
        # If no date column available, create a default vintage
        df['Vintage'] = 'Q1 2023'  # Default value
    
    # Columns to aggregate
    agg_dict = {}
    if 'Amount' in df.columns:
        agg_dict['Amount'] = 'sum'
    if 'Repaid Amount' in df.columns:
        agg_dict['Repaid Amount'] = 'sum'
    if 'Business Name' in df.columns:
        agg_dict['Business Name'] = 'count'
    
    # Make sure we're using the renamed column names from load_loan_data
    vintage_summary = df.groupby('Vintage').agg(agg_dict).reset_index()
    
    # Calculate repayment rate if both columns exist
    if 'Amount' in vintage_summary.columns and 'Repaid Amount' in vintage_summary.columns:
        vintage_summary['repayment_rate'] = vintage_summary['Repaid Amount'] / vintage_summary['Amount']
    else:
        # Add a default repayment rate if data is missing
        vintage_summary['repayment_rate'] = 0.5  # Default 50% repayment rate
    
    return vintage_summary