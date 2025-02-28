import pandas as pd


def get_risk_summary(df):
    """Generate risk summary statistics that works with any number of platforms"""
    if len(df['platform'].unique()) == 0:
        # Create empty DataFrame with expected columns if no data
        return pd.DataFrame(columns=[
            'No Risk', 'Liquidity Risk', 'Revenue Drop Risk',
            'Non-Payment Risk'
        ])

    # Group by platform and risk category
    risk_summary = df.groupby(['platform',
                               'risk_category']).size().unstack(fill_value=0)

    # Ensure all expected risk categories exist
    for category in [
            'No Risk', 'Liquidity Risk', 'Revenue Drop Risk',
            'Non-Payment Risk'
    ]:
        if category not in risk_summary.columns:
            risk_summary[category] = 0

    # Calculate percentages
    risk_summary_pct = risk_summary.div(risk_summary.sum(axis=1), axis=0)

    return risk_summary_pct


def calculate_risk_metrics(df):
    """Calculate additional risk metrics"""
    metrics = {
        'total_at_risk': len(df[df['risk_category'] != 'No Risk']),
        'liquidity_risk': len(df[df['liquidity_risk'] == 1]),
        'revenue_drop_risk': len(df[df['revenue_drop_risk'] == 1]),
        'non_payment_risk': len(df[df['non_payment_risk'] == 1]),
    }
    return metrics
