import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# 1. Official NRS Branding & Setup
st.set_page_config(page_title="Nigeria Revenue Service Portal", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #1e3a8a; }
    .stAlert { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# Branding Header
col_header, col_logo = st.columns([4, 1])
with col_header:
    st.title("🇳🇬 Nigeria Revenue Service (NRS)")
    st.subheader("Tax Integrity & Audit Intelligence System")
    st.caption("Strategic Data Analysis Unit | Abuja HQ")

# 2. Dynamic Environment & Secure Data Ingestion
# Reads your production Render/Railway URL if available; defaults to local machine for testing
PRODUCTION_API_URL = os.getenv("NRS_BACKEND_URL", "https://nrs-backend-api.onrender.com/data")
LOCAL_FALLBACK_FILE = "nrs_audited_results.csv"

@st.cache_data(ttl=300)  # Caches data for 5 minutes to prevent hammering your API
def fetch_audit_data(url: str, fallback_path: str):
    """
    Robust Data Ingestion Engine. 
    Attempts live backend synchronization, falling back gracefully to a localized
    cached data state if the production server environment is spinning down.
    """
    try:
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            return pd.DataFrame(response.json()), "Live API Synchronization"
    except Exception:
        pass # Gracefully pivot to local architecture check
        
    if os.path.exists(fallback_path):
        return pd.read_csv(fallback_path), "Local Storage Fallback (Offline Mode)"
    else:
        raise FileNotFoundError("Critical System Error: No operational data layer detected.")

# Execute Data Load
try:
    df, data_source_mode = fetch_audit_data(PRODUCTION_API_URL, LOCAL_FALLBACK_FILE)

    # Display Architecture Pipeline Status to Recruiters
    if "Fallback" in data_source_mode:
        st.sidebar.warning(f"🔌 System Status: {data_source_mode}")
    else:
        st.sidebar.success(f"⚡ System Status: {data_source_mode}")

    # --- Column Normalization Engine ---
    cols = {c.lower().replace(' ', '_').replace('.', '_'): c for c in df.columns}
    
    t_col = cols.get('tax_paid', df.columns[2] if len(df.columns) > 2 else df.columns[0])
    a_col = cols.get('is_anomaly', cols.get('anomaly'))
    s_col = cols.get('sector', df.columns[1] if len(df.columns) > 1 else df.columns[0])
    r_col = cols.get('region', df.columns[3] if len(df.columns) > 3 else df.columns[0])

    # --- EXECUTIVE METRICS ---
    st.write("### 🔑 Key Performance Indicators")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Total Revenue Audited", f"₦{df[t_col].sum():,.0f}")
    
    with m2:
        if a_col:
            risk_total = len(df[df[a_col].astype(str).str.upper().str.contains('YES|TRUE|1', na=False)])
            st.metric("High-Risk Files", risk_total, delta="Review Required", delta_color="inverse")
        else:
            st.metric("High-Risk Files", "0", delta="No Column Match")
    
    with m3:
        st.metric("Active Tax Jurisdictions", df[r_col].nunique())
        
    with m4:
        top_contributor = df.groupby(s_col)[t_col].sum().idxmax()
        st.metric("Top Contributing Sector", top_contributor)

    st.divider()

    # --- INTELLIGENCE VISUALS ---
    c1, c2 = st.columns([2, 1])

    with c1:
        st.write("#### 📊 Revenue Density (Region & Sector)")
        fig = px.treemap(df, path=[r_col, s_col], values=t_col,
                         color=t_col, color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("#### 💡 Executive Summary")
        top_reg = df.groupby(r_col)[t_col].sum().idxmax()
        st.info(f"**{top_reg}** is the primary revenue driver in this batch.")
        if a_col:
            st.warning(f"Found **{risk_total} anomalies** requiring secondary verification.")
        st.success("Internal Systems: Synchronized")

    # --- AUDIT TABLE ---
    st.write("#### 🔍 Master Audit Investigation List")
    search = st.text_input("Quick Search (Enter Sector, Region, or ID):")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    st.dataframe(df, use_container_width=True)

    # --- EXPORT ---
    st.download_button("📥 Export Certified Audit Report", df.to_csv(index=False), "NRS_Audit_Final.csv", "text/csv")

except Exception as e:
    st.error(f"System Offline. Detailed Error: {str(e)}")
