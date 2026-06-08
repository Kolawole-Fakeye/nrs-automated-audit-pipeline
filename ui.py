import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="NRS Tax Integrity & Audit Intelligence", layout="wide")
st.title("🦅 Nigeria Revenue Service (NRS)")
st.subheader("Tax Integrity & Audit Intelligence System")
st.markdown("---")

# The dedicated tax data file pathway
DATA_PATH = "data/tax_compliance_telemetry.csv"

# --- INTERNAL SELF-SEEDING TAX AUDIT DATA LAYER ---
@st.cache_data
def seed_tax_data():
    """Generates corporate tax compliance telemetry locally inside the cloud container"""
    if not os.path.exists(DATA_PATH):
        np.random.seed(101)
        records = 200
        sectors = ['Manufacturing', 'Oil & Gas', 'Telecommunications', 'Financial Services', 'Maritime & Logistics']
        states = ['Lagos', 'Rivers', 'FCT Abuja', 'Kano', 'Delta']
        
        df = pd.DataFrame({
            'taxpayer_id': [f"RC-{np.random.randint(100000, 999999)}" for _ in range(records)],
            'company_name': [f"Corporate_Asset_{i:03d} Ltd" for i in range(1, records + 1)],
            'sector': np.random.choice(sectors, records),
            'registered_state': np.random.choice(states, records, p=[0.4, 0.2, 0.2, 0.1, 0.1]),
            'reported_revenue_ngn': np.random.uniform(50_000_000, 2_500_000_000, records).round(2)
        })
        
        # Algorithmic Audit Indicators
        df['effective_tax_rate'] = df['sector'].apply(
            lambda s: np.random.uniform(0.05, 0.15) if s in ['Oil & Gas', 'Financial Services'] else np.random.uniform(0.18, 0.32)
        )
        df['tax_paid_ngn'] = (df['reported_revenue_ngn'] * df['effective_tax_rate']).round(2)
        
        # Fraud/Risk Flagging Heuristics
        df['variance_score'] = np.random.uniform(0.0, 1.0, records)
        df['audit_risk_status'] = df.apply(
            lambda row: 'CRITICAL (High Risk)' if row['effective_tax_rate'] < 0.12 and row['variance_score'] > 0.7 
            else 'REVIEW REQUIRED' if row['effective_tax_rate'] < 0.18 or row['variance_score'] > 0.5 
            else 'COMPLIANT', axis=1
        )
        
        os.makedirs('data', exist_ok=True)
        df.to_csv(DATA_PATH, index=False)

# Seed the tax data file silently behind the scenes
seed_tax_data()

# --- TAX SYSTEM VISUALIZATION LAYER ---
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    
    # Core Fiscal KPIs
    total_taxpayers = len(df)
    total_revenue = df['reported_revenue_ngn'].sum()
    total_tax_collected = df['tax_paid_ngn'].sum()
    flagged_cases = len(df[df['audit_risk_status'] == 'CRITICAL (High Risk)'])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Taxpayers Audited", f"{total_taxpayers}")
    col2.metric("Total Reported Revenue", f"₦{total_revenue:,.2f}")
    col3.metric("Total Tax Recovered", f"₦{total_tax_collected:,.2f}")
    col4.metric("Critical Risk Flags", f"⚠️ {flagged_cases} Cases")
    
    st.markdown("---")
    
    # Analytics Row (Using Native, Bulletproof Streamlit Charts)
    left, right = st.columns(2)
    
    with left:
        st.subheader("📊 Sector Risk Exposure (Avg Risk Variance)")
        sector_analysis = df.groupby("sector")["variance_score"].mean()
        st.bar_chart(sector_analysis)
        
    with right:
        st.subheader("📍 Compliance Tax Density by Region")
        state_risk = df.groupby("registered_state")["tax_paid_ngn"].sum()
        st.bar_chart(state_risk)
        
    st.markdown("---")
    
    # Raw Audit Ledger Stream
    st.subheader("📋 System Audit Log & Fraud Risk Matrix")
    
    # Dropdown interactive filtering built natively
    status_filter = st.selectbox("Filter Ledger by Risk Profile:", ['ALL'] + list(df['audit_risk_status'].unique()))
    if status_filter != 'ALL':
        filtered_df = df[df['audit_risk_status'] == status_filter]
    else:
        filtered_df = df
        
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.error("NRS Tax System Audit Core Initialization Failed.")
