
import pandas as pd

def get_risk_summary(df):
    """Generate risk summary statistics that works with any number of platforms"""
    if len(df['Platform'].unique()) == 0:
        # Create empty DataFrame with expected columns if no data
        return pd.DataFrame(columns=['No Risk', 'Liquidity Risk 🟢', 'Revenue Drop Risk 🟠', 'Non-Payment Risk 🔴'])
    
    # Ensure Risk Category column exists
    if 'risk_category' in df.columns and 'Risk Category' not in df.columns:
        df['Risk Category'] = df['risk_category']
    
    # Group by platform and risk category
    risk_summary = df.groupby(['Platform', 'Risk Category']).size().unstack(fill_value=0)
    
    # Ensure all expected risk categories exist
    for category in ['No Risk', 'Liquidity Risk 🟢', 'Revenue Drop Risk 🟠', 'Non-Payment Risk 🔴']:
        if category not in risk_summary.columns:
            risk_summary[category] = 0
    
    # Calculate percentages
    risk_summary_pct = risk_summary.div(risk_summary.sum(axis=1), axis=0)
    
    # Reformat data to long format that works better with Plotly
    if len(risk_summary_pct) == 1:
        # For single platform, transform to long format
        platform_name = risk_summary_pct.index[0]
        risk_summary_pct = risk_summary_pct.reset_index()
    
    return risk_summary_pct

def calculate_risk_metrics(df):
    """Calculate additional risk metrics"""
    # Ensure risk flag columns exist
    if 'liquidity_risk' not in df.columns:
        df['liquidity_risk'] = False
    if 'revenue_drop_risk' not in df.columns:
        df['revenue_drop_risk'] = False
    if 'non_payment_risk' not in df.columns:
        df['non_payment_risk'] = False
        
    metrics = {
        'total_at_risk': len(df[df['Risk Category'] != 'No Risk']),
        'liquidity_risk': len(df[df['liquidity_risk']]),
        'revenue_drop_risk': len(df[df['revenue_drop_risk']]),
        'non_payment_risk': len(df[df['non_payment_risk']]),
    }
    return metrics

def get_risk_category_table():
    """Return the risk category explanation table"""
    risk_data = {
        'Risk Category': [
            'Liquidity Risk 🟢',
            'Revenue Drop Risk 🟠',
            'Non-Payment Risk 🔴'
        ],
        'Definition': [
            'Business revenue is stable, but their overall cash flow health is deteriorating. They might be overleveraged, have high expenses, or be showing early warning signs of financial strain. Repayments are still occurring at the expected percentage, but their total financial health is weakening.',
            'Business revenue has dropped ≥50% for multiple months, meaning their ability to make repayments is significantly reduced. They are still making some repayments, but their funding risk is increasing.',
            'Business has had $0 revenue for 60+ days, meaning no repayments are occurring. This suggests business closure, switching platforms, or severe distress.'
        ],
        'Severity': [
            'Mild',
            'Moderate',
            'Severe'
        ]
    }
    return pd.DataFrame(risk_data)
