import streamlit as st
from supabase import create_client, Client

# --- 1. CONNECT TO DATABASE ---
# This pulls the keys you just saved in the Streamlit Secrets tab
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Laundry OI", layout="wide")

# --- 2. THE LOGIC ---
def get_inventory():
    # Pulls the latest data from your Supabase 'linen_items' table
    response = supabase.table("linen_items").select("*").execute()
    return response.data

st.title("Hospital Linen Tracking System")

# Admin Scan Section
with st.expander("📷 Scan / Update Item"):
    qr_code = st.text_input("Enter QR ID")
    status = st.selectbox("New Status", ["Dirty", "Washing", "Ready", "Dispatched"])
    
    if st.button("Update System"):
        supabase.table("linen_items").update({"status": status}).eq("qr_code", qr_code).execute()
        st.success(f"Item {qr_code} updated!")
        st.rerun()

# Real-time Dashboard View
st.subheader("Live Operational View")
data = get_inventory()
if data:
    st.table(data)
else:
    st.write("No items scanned yet.")
