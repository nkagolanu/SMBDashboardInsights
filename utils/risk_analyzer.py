import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

def calculate_risk_score(loan_data):
    """Calculate risk scores for loans using an isolation forest"""
    features = [
        'repayment_velocity',
        'days_no_payment',
        'revenue_decline'
    ]
    
    X = loan_data[features].copy()
    X['revenue_decline'] = X['revenue_decline'].astype(int)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    risk_scores = iso_forest.fit_predict(X_scaled)
    
    # Convert to probability-like scores (0-1 where 1 is highest risk)
    risk_scores = (risk_scores == -1).astype(float)
    
    return risk_scores

def categorize_risk(loan):
    """Categorize loan risk based on various factors"""
    if loan['days_no_payment'] >= 60:
        return 'High Risk - No Payment'
    elif loan['repayment_velocity'] < 0.3:
        return 'High Risk - Slow Repayment'
    elif loan['revenue_decline']:
        return 'Medium Risk - Revenue Decline'
    return 'Low Risk'

def get_risk_summary(df):
    """Generate risk summary statistics"""
    df['risk_category'] = df.apply(categorize_risk, axis=1)
    risk_summary = df.groupby(['platform', 'risk_category']).size().unstack(fill_value=0)
    risk_summary_pct = risk_summary.div(risk_summary.sum(axis=1), axis=0)
    return risk_summary_pct
