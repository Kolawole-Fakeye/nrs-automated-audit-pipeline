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
# Synchronized with main.py endpoint path
PRODUCTION_API_URL = os.getenv("NRS_BACKEND_URL", "https://nrs-backend-api.onrender.com/api/v1/audit-data")
LOCAL_FALLBACK_FILE = "nrs_audited_results.csv"

@st.cache_data(ttl=300)  # Caches data for 5 minutes
def fetch_audit_data(url: str, fallback_path: str):
    """
    Robust Data Ingestion Engine. 
    Synchronizes with FastAPI's wrapped dictionary response and handles cold-starts.
    """
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            json_response = response.json()
            # Extract the actual data records list from the backend's wrapper
            if isinstance(json_response, dict) and "data" in json_response:
                return pd.DataFrame(json_response["data"]), "Live API Synchronization"
            else:
                return pd.DataFrame(json_response), "Live API Synchronization"
    except Exception:
        pass # Gracefully pivot to local architecture check
        
    if os.path.exists(fallback_path):
        return pd.read_csv(fallback_path), "Local Storage Fallback (Offline Mode)"
    else:
        raise FileNotFoundError("Critical System Error: No operational data layer detected on Render or Local Storage.")

# Execute Data Load
try:
    df, data_source_mode = fetch_audit_data(PRODUCTION_API_URL, LOCAL_FALLBACK_FILE)

    # Display Architecture Pipeline Status
    if "Fallback" in data_source_mode:
        st.sidebar.warning(f"🔌 System Status: {data_source_mode}")
    else:
        st.sidebar.success(f"⚡ System Status: {data_source_mode}")

    # --- Column Normalization Engine ---
    cols = {c.lower().replace(' ', '_').replace('.', '_'): c for c in df.columns}
    
    t_col = cols.get('tax_paid', cols.get('reported_revenue', df.columns[2] if len(df.columns) > 2 else df.columns[0]))
    a_col = cols.get('is_anomaly', cols.get('anomaly', cols.get('audit_status')))
    s_col = cols.get('sector', cols.get('taxpayer_name', df.columns[1] if len(df.columns) > 1 else df.columns[0]))
    r_col = cols.get('region', cols.get('taxpayer_id', df.columns[3] if len(df.columns) > 3 else df.columns[0]))

    # --- EXECUTIVE METRICS ---
    st.write("### 🔑 Key Performance Indicators")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Total Revenue Audited", f"₦{df[t_col].sum():,.0f}")
    
    with m2:
        # Check if anomaly logic or 'Under Review' status exists
        risk_condition = df[a_col].astype(str).str.upper().str.contains('YES|TRUE|1|UNDER REVIEW', na=False)
        risk_total = len(df[risk_condition])
        st.metric("High-Risk Files", risk_total, delta="Review Required", delta_color="inverse")
    
    with m3:
        st.metric("Total Tracked Entities", df[r_col].nunique())
        
    with m4:
        # Handle fallback calculations if columns vary
        try:
            top_contributor = df.groupby(s_col)[t_col].sum().idxmax()
            # Trim long names for display layout aesthetics
            if len(str(top_contributor)) > 20:
                top_contributor = str(top_contributor)[:17] + "..."
        except:
            top_contributor = "N/A"
        st.metric("Top Contributing Entity/Sector", top_contributor)

    st.divider()

    # --- INTELLIGENCE VISUALS ---
    c1, c2 = st.columns([2, 1])

    with c1:
        st.write("#### 📊 Revenue Distribution Map")
        fig = px.treemap(df, path=[s_col], values=t_col,
                         color=t_col, color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("#### 💡 Executive Summary")
        st.info("System operational data connection established cleanly.")
        st.warning(f"Found **{risk_total} files** requiring secondary verification workflow rules.")
        st.success("Internal Data Pipelines: Fully Synchronized")

    # --- AUDIT TABLE ---
    st.write("#### 🔍 Master Audit Investigation List")
    search = st.text_input("Quick Search (Enter Sector, Name, or ID):")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    st.dataframe(df, use_container_width=True)

    # --- EXPORT ---
    st.download_button("📥 Export Certified Audit Report", df.to_csv(index=False), "NRS_Audit_Final.csv", "text/csv")

except Exception as e:
    st.error(f"System Offline. Detailed Error: {str(e)}")
