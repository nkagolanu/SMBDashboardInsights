import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_loan_data(n_loans=1000):
    """Generate mock loan data for the dashboard"""
    platforms = ['Priority', 'Boulevard', 'Housecall Pro']
    industries = ['Retail', 'Services', 'Healthcare', 'Technology']
    regions = ['West', 'East', 'North', 'South']
    
    np.random.seed(42)
    
    data = {
        'loan_id': range(1, n_loans + 1),
        'platform': np.random.choice(platforms, n_loans),
        'industry': np.random.choice(industries, n_loans),
        'region': np.random.choice(regions, n_loans),
        'amount': np.random.uniform(10000, 500000, n_loans),
        'start_date': [
            (datetime.now() - timedelta(days=np.random.randint(0, 365)))
            for _ in range(n_loans)
        ],
        'repaid_amount': None,
        'revenue_share': np.random.uniform(0.05, 0.15, n_loans),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate repaid amounts based on time elapsed and some randomness
    df['repaid_amount'] = df.apply(
        lambda x: x['amount'] * (
            (datetime.now() - x['start_date']).days / 365
        ) * (0.8 + np.random.uniform(0, 0.4)),
        axis=1
    )
    
    # Add risk factors
    df['repayment_velocity'] = df['repaid_amount'] / df['amount']
    df['revenue_decline'] = np.random.choice([True, False], n_loans, p=[0.1, 0.9])
    df['days_no_payment'] = np.random.choice(
        [0, 15, 30, 45, 60, 90],
        n_loans,
        p=[0.7, 0.1, 0.1, 0.05, 0.03, 0.02]
    )
    
    return df

def get_vintage_data(df):
    """Convert loan data into vintage analysis format"""
    df['vintage'] = df['start_date'].dt.to_period('Q')
    vintage_summary = df.groupby('vintage').agg({
        'amount': 'sum',
        'repaid_amount': 'sum',
        'loan_id': 'count'
    }).reset_index()
    vintage_summary['repayment_rate'] = vintage_summary['repaid_amount'] / vintage_summary['amount']
    return vintage_summary
