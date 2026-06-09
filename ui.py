import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

st.set_page_config(page_title="NRS Tax Integrity & Audit Intelligence", layout="wide")
st.title("🦅 Nigeria Revenue Service (NRS)")
st.subheader("Tax Integrity & Audit Intelligence System")
st.markdown("---")

# Backend API Endpoint Configuration
BACKEND_API_URL = "http://localhost:8000/api/v1/audit-data"
PARQUET_FILE_PATH = "nrs_audited_results.parquet"

# --- CORE DATA INGESTION OR CHECKSUM FALLBACK ---
@st.cache_data
def load_audit_pipeline_data():
    """
    Attempts to pull data dynamically from your FastAPI backend endpoint.
    Falls back to the local Apache Parquet binary file if the service is offline.
    """
    try:
        # Attempt to stream payload via FastAPI backend REST route
        response = requests.get(BACKEND_API_URL, timeout=3)
        if response.status_code == 200:
            payload = response.json()
            return pd.DataFrame(payload["data"])
    except Exception:
        # Silent failover to reading the high-performance local Parquet cache
        pass
        
    if os.path.exists(PARQUET_FILE_PATH):
        return pd.read_parquet(PARQUET_FILE_PATH)
    
    # Ultimate fail-safe data array if container boots cold with no prior state
    fallback_data = {
        "taxpayer_id": ["NRS-2026-001", "NRS-2026-002", "NRS-2026-003"],
        "taxpayer_name": ["Aliko Dangote Industries", "Tony Elumelu Holdings", "Afolabi Systems Ltd"],
        "reported_revenue": [50000000.0, 35000000.0, 12000000.0],
        "tax_paid": [5000000.0, 3500000.0, 1200000.0],
        "audit_status": ["Compliant", "Under Review", "Compliant"],
        "risk_score": [0.12, 0.45, 0.05]
    }
    return pd.DataFrame(fallback_data)

# Ingest and map core records dataframe
df = load_audit_pipeline_data()

# Ensure case-insensitivity alignment with your main.py standardized columns
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

if not df.empty:
    # Process core analytics variables 
    total_taxpayers = len(df)
    total_revenue = df['reported_revenue'].sum()
    total_tax_paid = df['tax_paid'].sum()
    flagged_cases = len(df[df['audit_status'].str.lower() == 'under review'])
    
    # Row 1: KPI Summary Scorecards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Audited Taxpayers", f"{total_taxpayers}")
    col2.metric("Reported Gross Revenue", f"₦{total_revenue:,.2f}")
    col3.metric("Aggregated Tax Recovered", f"₦{total_tax_paid:,.2f}")
    col4.metric("Risk Audits Flagged", f"⚠️ {flagged_cases}")
    
    st.markdown("---")
    
    # Row 2: Advanced Interactive Plotly Visualizations
    left, right = st.columns(2)
    
    with left:
        st.subheader("📊 Tax Contributions vs Gross Revenue")
        # Creating an interactive grouped bar chart using your Plotly dependency
        fig_bar = px.bar(
            df, 
            x="audit_status", 
            y=["reported_revenue", "tax_paid"],
            barmode="group",
            labels={"value": "Amount (₦)", "audit_status": "Compliance Classification"},
            color_discrete_sequence=["#1f77b4", "#ff7f0e"]
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with right:
        st.subheader("📈 Institutional Risk Profile Breakdown")
        # Creating an interactive scatter profile mapping revenue sizes against calculated risk scores
        fig_scatter = px.scatter(
            df,
            x="reported_revenue",
            y="risk_score",
            color="audit_status",
            hover_name="taxpayer_name",
            labels={"reported_revenue": "Reported Revenue (₦)", "risk_score": "Audit Risk Score Index"},
            color_discrete_map={"Compliant": "green", "Under Review": "red"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.markdown("---")
    
    # Row 3: Transaction Records Filter Interface
    st.subheader("📋 Systemic Compliance Ledger Stream")
    
    status_options = ["All Records"] + [status.title() for status in df['audit_status'].unique()]
    status_filter = st.selectbox("Filter Audit Stream by Status:", status_options)
    
    if status_filter != "All Records":
        display_df = df[df['audit_status'].str.lower() == status_filter.lower()]
    else:
        display_df = df
        
    st.dataframe(display_df, use_container_width=True)

else:
    st.error("Critical System Error: Operational data layer parsing failed.")
