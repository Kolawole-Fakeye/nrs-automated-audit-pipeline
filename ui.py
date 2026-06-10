import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="NRS Tax Integrity & Audit Intelligence",
    page_icon="🦅",
    layout="wide"
)

st.title("🦅 Nigeria Revenue Service (NRS)")
st.subheader("Tax Integrity & Audit Intelligence System")
st.markdown("---")

# 2. FILE INFRASTRUCTURE DATA PATH
PARQUET_FILE_PATH = "nrs_audited_results.parquet"

# 3. ROBUST DATA LOADING LAYER (WITH ANTI-CRASH FALLBACK)
@st.cache_data
def load_and_normalize_data():
    """
    Loads the audit dataset from the high-performance Parquet binary cache.
    If the file doesn't exist, it auto-generates a clean data asset.
    Guarantees all columns are strictly snake_case and lower-case.
    """
    # Fallback asset generation if file is missing
    if not os.path.exists(PARQUET_FILE_PATH):
        fallback_data = {
            "taxpayer_id": ["NRS-2026-001", "NRS-2026-002", "NRS-2026-003"],
            "taxpayer_name": ["Aliko Dangote Industries", "Tony Elumelu Holdings", "Afolabi Systems Ltd"],
            "reported_revenue": [50000000.0, 35000000.0, 12000000.0],
            "tax_paid": [5000000.0, 3500000.0, 1200000.0],
            "audit_status": ["Compliant", "Under Review", "Compliant"],
            "risk_score": [0.12, 0.45, 0.05]
        }
        df_fallback = pd.DataFrame(fallback_data)
        df_fallback.to_parquet(PARQUET_FILE_PATH, index=False)

    # Ingest the Parquet file
    df = pd.read_parquet(PARQUET_FILE_PATH)
    
    # Strict Normalization Guardrail: Force everything to clean, lower snake_case
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    
    return df

# Initialize Dataframe safely
df = load_and_normalize_data()

# 4. MAIN DASHBOARD VISUALIZATION CONTROLLER
if not df.empty:
    
    # Safe Extraction Layer using .get() principles to avoid KeyErrors
    total_taxpayers = len(df)
    total_revenue = df["reported_revenue"].sum() if "reported_revenue" in df.columns else 0.0
    total_tax_paid = df["tax_paid"].sum() if "tax_paid" in df.columns else 0.0
    
    if "audit_status" in df.columns:
        flagged_cases = len(df[df["audit_status"].astype(str).str.lower() == "under review"])
    else:
        flagged_cases = 0

    # SECTION A: CORE KPI SCORECARDS
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Audited Taxpayers", f"{total_taxpayers}")
    col2.metric("Reported Gross Revenue", f"₦{total_revenue:,.2f}")
    col3.metric("Aggregated Tax Recovered", f"₦{total_tax_paid:,.2f}")
    col4.metric("Risk Audits Flagged", f"⚠️ {flagged_cases}")
    
    st.markdown("---")
    
    # SECTION B: INTERACTIVE ANALYTICS VISUALIZATIONS (PLOTLY)
    left_chart, right_chart = st.columns(2)
    
    with left_chart:
        st.subheader("📊 Volumetric Tax Distributions by Status")
        if "audit_status" in df.columns and "reported_revenue" in df.columns:
            fig_bar = px.bar(
                df, 
                x="audit_status", 
                y=["reported_revenue", "tax_paid"],
                barmode="group",
                labels={"value": "Amount (₦)", "audit_status": "Compliance Status"},
                color_discrete_sequence=["#0d6efd", "#ffc107"]
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Metrics data missing for bar distribution.")
            
    with right_chart:
        st.subheader("📈 Institutional Risk Profile Map")
        if "reported_revenue" in df.columns and "risk_score" in df.columns:
            fig_scatter = px.scatter(
                df,
                x="reported_revenue",
                y="risk_score",
                color="audit_status" if "audit_status" in df.columns else None,
                hover_name="taxpayer_name" if "taxpayer_name" in df.columns else None,
                labels={"reported_revenue": "Reported Revenue (₦)", "risk_score": "Audit Risk Index"},
                color_discrete_map={"Compliant": "green", "Under Review": "red"}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Metrics data missing for risk profile scatter.")

    st.markdown("---")
    
    # SECTION C: TRANSACTION COMPLIANCE LEDGER STREAM
    st.subheader("📋 Systemic Compliance Ledger Stream")
    
    if "audit_status" in df.columns:
        unique_statuses = [status.title() for status in df["audit_status"].unique()]
        status_filter = st.selectbox("Filter Logs by Corporate Audit Status:", ["All Records"] + unique_statuses)
        
        if status_filter != "All Records":
            display_df = df[df["audit_status"].astype(str).str.lower() == status_filter.lower()]
        else:
            display_df = df
    else:
        display_df = df
        
    st.dataframe(display_df, use_container_width=True)

else:
    st.error("Critical System Initialization Error: Data processing pipeline offline.")
