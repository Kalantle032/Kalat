import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIG & UI ---
st.set_page_config(page_title="Laundry OI System", layout="wide")
st.title("🧺 Laundry Operational Intelligence")

# Simulated Data (In production, replace with: st.connection('supabase'))
data = {
    'Item ID': ['QR001', 'QR002', 'QR003', 'QR004'],
    'Client': ['City General Hospital', 'Grand Plaza Hotel', 'City General Hospital', 'City General Hospital'],
    'Status': ['Washing', 'Ready', 'Dirty', 'In-Service'],
    'Last Update': ['2026-05-02 10:00', '2026-05-02 11:30', '2026-05-02 12:00', '2026-05-02 12:45']
}
df = pd.DataFrame(data)

# --- SIDEBAR NAV ---
role = st.sidebar.selectbox("Login Role", ["Admin (Laundry)", "Client (Hospital)"])

if role == "Admin (Laundry)":
    st.header("Admin Operations Center")
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Throughput", "1,240 items/day", "+5%")
    col2.metric("Active Washers", "8/10", "-2")
    col3.metric("Loss Rate", "0.4%", "Stable")

    # Workflow Automation Section
    st.subheader("Update Workflow")
    qr_input = st.text_input("Scan QR Code (or type ID)")
    new_stat = st.selectbox("Action", ["Move to Washing", "Mark as Ready", "Dispatch to Client"])
    if st.button("Update Status"):
        st.success(f"Item {qr_input} updated to {new_stat}")

elif role == "Client (Hospital)":
    st.header("Hospital Management Dashboard")
    client_df = df[df['Client'] == 'City General Hospital']
    
    # Real-time Insights
    st.write("Current Inventory Status:")
    fig = px.pie(client_df, names='Status', hole=0.4, title="Your Linen Distribution")
    st.plotly_chart(fig)
    
    st.table(client_df)
