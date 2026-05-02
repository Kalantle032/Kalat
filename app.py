import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px

# --- CONNECTION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- NAVIGATION ---
st.sidebar.title("🧺 Laundry OS")
role = st.sidebar.radio("Select Dashboard", ["Workforce (Staff)", "Client (Hospital)", "Admin (Manager)"])

# --- 1. WORKFORCE DASHBOARD (Action Oriented) ---
if role == "Workforce (Staff)":
    st.header("📲 Floor Operations")
    qr_code = st.text_input("Scan QR Code")
    status = st.selectbox("Update To", ["Dirty", "Washing", "Drying", "Ready"])
    
    if st.button("Log Activity"):
        supabase.table("linen_items").update({"status": status}).eq("qr_code", qr_code).execute()
        st.success(f"Item {qr_code} is now {status}")

# --- 2. CLIENT DASHBOARD (Transparency Oriented) ---
elif role == "Client (Hospital)":
    st.header("🏥 Hospital Inventory Portal")
    client_name = st.selectbox("Select Hospital", ["City General", "St. Jude's"]) # In production, this is fixed by login
    
    res = supabase.table("linen_items").select("*").eq("client_name", client_name).execute()
    df = pd.DataFrame(res.data)
    
    col1, col2 = st.columns(2)
    col1.metric("Ready for Pickup", len(df[df['status'] == 'Ready']))
    col2.metric("Currently in Wash", len(df[df['status'] == 'Washing']))
    
    st.subheader("Item Tracker")
    st.dataframe(df)

# --- 3. ADMIN DASHBOARD (Insights Oriented) ---
elif role == "Admin (Manager)":
    st.header("📊 Operational Intelligence")
    res = supabase.table("linen_items").select("*").execute()
    df = pd.DataFrame(res.data)

    # Analytics: Status Breakdown
    fig = px.bar(df, x='status', title="Facility-Wide Throughput", color='status')
    st.plotly_chart(fig, use_container_width=True)

    # Fleet Health Metric (Example)
    st.info("System Alert: Machine #3 is running 15% slower than average.")
