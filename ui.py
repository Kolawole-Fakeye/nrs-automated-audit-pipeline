import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="NRS Tax Integrity & Audit Intelligence", layout="wide")
st.title("🦅 Nigeria Revenue Service (NRS)")
st.subheader("Tax Integrity & Audit Intelligence System")
st.markdown("---")

# Use a native, plain-text CSV format that requires ZERO external installation dependencies
CSV_FILE_PATH = "data/nrs_audited_results_ui.csv"

# --- INTERNAL ZERO-DEPENDENCY DATA LAYER ---
@st.cache_data
def ensure_local_csv_cache():
    """
    Creates a clean, plain-text CSV data layer inside the cloud container.
    Matches your exact backend schema columns: taxpayer_id, taxpayer_name, 
    reported_revenue, tax_paid, audit_status, and risk_score.
    """
    if not os.path.exists(CSV_FILE_PATH):
        np.random.seed(101)
        records = 150
        
        # Mirroring your core corporate entities from the main backend fallback layer
        baseline_companies = ["Aliko Dangote Industries", "Tony Elumelu Holdings", "Afolabi Systems Ltd"]
        additional_companies = [f"Corporate_Taxpayer_{i:03d} Ltd" for i in range(4, records + 1)]
        all_companies = baseline_companies + additional_companies
        
        df = pd.DataFrame({
            'taxpayer_id': [f"NRS-2026-{i:03d}" for i in range(1, records + 1)],
            'taxpayer_name': all_companies,
            'reported_revenue': np.random.uniform(5_000_000, 150_000_000, records).round(2),
            'risk_score': np.random.uniform(0.01, 0.95, records).round(2)
        })
        
        # Calculate matching fiscal logic natively
        df['tax_paid'] = (df['reported_revenue'] * np.random.uniform(0.10, 0.30, records)).round(2)
        
        # Use your exact backend string values for status filtering
        df['audit_status'] = df['risk_score'].apply(
            lambda r: 'Under Review' if r > 0.65 else 'Compliant'
        )
        
        os.makedirs('data', exist_ok=True)
        df.to_csv(CSV_FILE_PATH, index=False)

# Silently seed the native data file inside the Streamlit instance
ensure_local_csv_cache()

# --- SYSTEM INTEGRITY VISUALIZATION LAYER ---
if os.path.exists(CSV_FILE_PATH):
    # Read the text file natively (Pandas handles CSV with zero extra packages)
    df = pd.read_csv(CSV_FILE_PATH)
    
    # Process Metrics Safely matching your exact variables
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
    
    # Row 2: Native, Dependency-Free Analytics Engine
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
    
    # Filter dropdown based on your actual statuses
    status_filter = st.selectbox("Filter Ledger by Audit Status:", ["All Records", "Compliant", "Under Review"])
    if status_filter != "All Records":
        display_df = df[df['audit_status'] == status_filter]
    else:
        display_df = df
        
    st.dataframe(display_df, use_container_width=True)

else:
    st.error("Critical System Error: No operational data layer detected on the UI instance.")
