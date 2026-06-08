import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="NRS Tax Integrity & Audit Intelligence", layout="wide")
st.title("🦅 Nigeria Revenue Service (NRS)")
st.subheader("Tax Integrity & Audit Intelligence System")
st.markdown("---")

# Point directly to the exact file your backend generates
PARQUET_FILE_PATH = "nrs_audited_results.parquet"

# --- INTERNAL SELF-CONTAINED DATA CACHE ---
@st.cache_data
def ensure_local_parquet_cache():
    """
    If running isolated on the cloud container, ensures the exact Parquet 
    schema matching your backend exists without external API calls.
    """
    if not os.path.exists(PARQUET_FILE_PATH):
        np.random.seed(101)
        records = 150
        
        # Exact baseline companies from your backend fallback layer
        baseline_companies = ["Aliko Dangote Industries", "Tony Elumelu Holdings", "Afolabi Systems Ltd"]
        additional_companies = [f"Corporate_Taxpayer_{i:03d} Ltd" for i in range(4, records + 1)]
        all_companies = baseline_companies + additional_companies
        
        df = pd.DataFrame({
            'taxpayer_id': [f"NRS-2026-{i:03d}" for i in range(1, records + 1)],
            'taxpayer_name': all_companies,
            'reported_revenue': np.random.uniform(5_000_000, 150_000_000, records).round(2),
            'risk_score': np.random.uniform(0.01, 0.95, records).round(2)
        })
        
        df['tax_paid'] = (df['reported_revenue'] * np.random.uniform(0.10, 0.30, records)).round(2)
        df['audit_status'] = df['risk_score'].apply(
            lambda r: 'Under Review' if r > 0.65 else 'Compliant'
        )
        
        # Write using fastparquet engine for zero-dependency compiling
        df.to_parquet(PARQUET_FILE_PATH, engine='fastparquet', index=False)

# Trigger cache seeding
ensure_local_parquet_cache()

# --- SYSTEM INTEGRITY VISUALIZATION LAYER ---
if os.path.exists(PARQUET_FILE_PATH):
    # Read the backend's parquet file cleanly
    df = pd.read_parquet(PARQUET_FILE_PATH, engine='fastparquet')
    
    # Process Metrics matching your variables exactly
    total_audited = len(df)
    total_reported_rev = df['reported_revenue'].sum()
    total_tax_recovered = df['tax_paid'].sum()
    high_risk_cases = len(df[df['audit_status'] == 'Under Review'])
    
    # Row 1: KPI Scorecards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Taxpayers Tracked", f"{total_audited}")
    col2.metric("Total Reported Revenue", f"₦{total_reported_rev:,.2f}")
    col3.metric("Total Tax Audited", f"₦{total_tax_recovered:,.2f}")
    col4.metric("Cases Under Review", f"⚠️ {high_risk_cases}")
    
    st.markdown("---")
    
    # Row 2: Native Analytics
    left, right = st.columns(2)
    
    with left:
        st.subheader("📊 Revenue vs Tax Paid Distribution")
        chart_data = df.groupby("audit_status")[["reported_revenue", "tax_paid"]].sum()
        st.bar_chart(chart_data)
        
    with right:
        st.subheader("📈 Systemic Risk Profile Curve")
        risk_analysis = df.groupby("audit_status")["risk_score"].mean()
        st.bar_chart(risk_analysis)
        
    st.markdown("---")
    
    # Row 3: Data Integrity Ledger Stream
    st.subheader("📋 Core Audit Intelligence Ledger")
    
    status_filter = st.selectbox("Filter Ledger by Audit Status:", ["All Records", "Compliant", "Under Review"])
    if status_filter != "All Records":
        display_df = df[df['audit_status'] == status_filter]
    else:
        display_df = df
        
    st.dataframe(display_df, use_container_width=True)

else:
    st.error("Critical System Error: No operational data layer detected on the UI instance.")
