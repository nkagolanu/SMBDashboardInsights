import pandas as pd

def get_risk_summary(df):
    """Generate risk summary statistics"""
    risk_summary = df.groupby(['platform', 'risk_category']).size().unstack(fill_value=0)
    risk_summary_pct = risk_summary.div(risk_summary.sum(axis=1), axis=0)
    return risk_summary_pct

def calculate_risk_metrics(df):
    """Calculate additional risk metrics"""
    metrics = {
        'total_at_risk': len(df[df['risk_category'] != 'No Risk']),
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