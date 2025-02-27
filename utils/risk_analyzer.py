import pandas as pd

def categorize_risk(loan):
    """Categorize loan risk based on existing risk flags"""
    if pd.isna(loan['Risk Flags']) or loan['Risk Flags'] == 'None':
        return 'Low Risk'
    elif 'Non-payment' in loan['risk_flags']:
        return 'High Risk - No Payment'
    elif 'Slow Repayment Velocity' in loan['risk_flags']:
        return 'High Risk - Slow Repayment'
    elif 'Revenue Drop Risk' in loan['risk_flags']:
        return 'Medium Risk - Revenue Decline'
    return 'Low Risk'

def get_risk_summary(df):
    """Generate risk summary statistics"""
    df['risk_category'] = df.apply(categorize_risk, axis=1)
    risk_summary = df.groupby(['platform', 'risk_category']).size().unstack(fill_value=0)
    risk_summary_pct = risk_summary.div(risk_summary.sum(axis=1), axis=0)
    return risk_summary_pct

def calculate_risk_metrics(df):
    """Calculate additional risk metrics"""
    metrics = {
        'total_at_risk': len(df[df['Risk Flags'].notna()]),
        'slow_repayment': len(df[df['risk_flags'].apply(lambda x: 'Slow Repayment Velocity' in x)]),
        'revenue_drop': len(df[df['risk_flags'].apply(lambda x: 'Revenue Drop Risk' in x)]),
        'no_payment': len(df[df['risk_flags'].apply(lambda x: 'Non-payment' in x)]),
    }
    return metrics