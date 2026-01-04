import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuration
st.set_page_config(
    page_title="Land Truth Registry",
    page_icon="🏞️",
    layout="wide"
)

# API Base URL
API_URL = "http://backend:8000"

# Sidebar Navigation
st.sidebar.title("🏞️ Land Truth Registry")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Register Asset", "Log Evidence"]
)

# Helper Functions
def get_assets():
    """Fetch all assets from the API"""
    try:
        response = requests.get(f"{API_URL}/assets/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching assets: {str(e)}")
        return []


def create_asset(name, owner, lat, lon, size):
    """Create a new asset"""
    try:
        payload = {
            "name": name,
            "owner": owner,
            "location_lat": lat,
            "location_lon": lon,
            "size_hectares": size
        }
        response = requests.post(f"{API_URL}/assets/", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error creating asset: {str(e)}")
        return None


def create_evidence(asset_id, evidence_type, description, lat, lon):
    """Log evidence for an asset"""
    try:
        payload = {
            "asset_id": asset_id,
            "evidence_type": evidence_type,
            "description": description,
            "gps_lat": lat,
            "gps_lon": lon
        }
        response = requests.post(f"{API_URL}/evidence/", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error logging evidence: {str(e)}")
        return None


def get_timeline(asset_id):
    """Fetch timeline for an asset"""
    try:
        response = requests.get(f"{API_URL}/assets/{asset_id}/timeline")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching timeline: {str(e)}")
        return []


# Page: Dashboard
if page == "Dashboard":
    st.title("📊 Land Registry Dashboard")
    st.markdown("### Asset Overview & Timeline Inspector")
    
    # Fetch assets
    assets = get_assets()
    
    if assets:
        # Display asset count
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Assets", len(assets))
        with col2:
            total_hectares = sum([asset['size_hectares'] for asset in assets])
            st.metric("Total Land (hectares)", f"{total_hectares:.2f}")
        with col3:
            unique_owners = len(set([asset['owner'] for asset in assets]))
            st.metric("Unique Owners", unique_owners)
        
        st.markdown("---")
        
        # Map visualization
        st.subheader("🗺️ Asset Locations")
        map_data = pd.DataFrame([
            {
                'lat': asset['location_lat'],
                'lon': asset['location_lon'],
                'name': asset['name']
            }
            for asset in assets
        ])
        st.map(map_data, zoom=6)
        
        st.markdown("---")
        
        # Timeline Inspector
        st.subheader("🔍 Timeline Inspector")
        
        # Asset selector
        asset_options = {f"{asset['name']} (ID: {asset['id']})": asset['id'] for asset in assets}
        selected_asset_label = st.selectbox("Select Asset", list(asset_options.keys()))
        
        if selected_asset_label:
            selected_asset_id = asset_options[selected_asset_label]
            
            # Fetch timeline
            timeline = get_timeline(selected_asset_id)
            
            if timeline:
                st.markdown(f"**Timeline for Asset ID {selected_asset_id}**")
                
                # Display timeline events
                for event in timeline:
                    event_type = event['event_type']
                    timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                    description = event['description']
                    
                    # Icon based on event type
                    icon = "🟢" if event_type == "evidence" else "📝"
                    
                    # Display event
                    with st.expander(f"{icon} {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {description}"):
                        if event.get('details'):
                            st.json(event['details'])
            else:
                st.info("No timeline events found for this asset.")
    else:
        st.info("No assets registered yet. Go to 'Register Asset' to add your first asset.")


# Page: Register Asset
elif page == "Register Asset":
    st.title("📝 Register New Asset")
    st.markdown("### Add a new land parcel to the registry")
    
    with st.form("register_asset_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Asset Name*", placeholder="e.g., Mashonaland Plot 4")
            owner = st.text_input("Owner Name*", placeholder="e.g., John Doe")
            size = st.number_input("Size (hectares)*", min_value=0.01, step=0.1, value=1.0)
        
        with col2:
            lat = st.number_input("Latitude*", min_value=-90.0, max_value=90.0, value=-17.8252, step=0.0001, format="%.4f")
            lon = st.number_input("Longitude*", min_value=-180.0, max_value=180.0, value=31.0335, step=0.0001, format="%.4f")
        
        submitted = st.form_submit_button("🚀 Register Asset")
        
        if submitted:
            if name and owner:
                result = create_asset(name, owner, lat, lon, size)
                if result:
                    st.success(f"✅ Asset successfully registered with ID: **{result['id']}**")
                    st.balloons()
                    st.json(result)
            else:
                st.error("Please fill in all required fields.")


# Page: Log Evidence
elif page == "Log Evidence":
    st.title("📸 Log Evidence")
    st.markdown("### Record evidence for an existing asset")
    
    # Fetch assets for dropdown
    assets = get_assets()
    
    if assets:
        with st.form("log_evidence_form"):
            # Asset selector
            asset_options = {f"{asset['name']} (ID: {asset['id']})": asset['id'] for asset in assets}
            selected_asset_label = st.selectbox("Select Asset*", list(asset_options.keys()))
            selected_asset_id = asset_options[selected_asset_label]
            
            col1, col2 = st.columns(2)
            
            with col1:
                evidence_type = st.selectbox(
                    "Evidence Type*",
                    ["Photo", "Document", "Survey", "Inspection", "Harvest Report", "Fencing", "Other"]
                )
                description = st.text_area("Description*", placeholder="Describe the evidence...")
            
            with col2:
                gps_lat = st.number_input("GPS Latitude*", min_value=-90.0, max_value=90.0, value=-17.8252, step=0.0001, format="%.4f")
                gps_lon = st.number_input("GPS Longitude*", min_value=-180.0, max_value=180.0, value=31.0335, step=0.0001, format="%.4f")
            
            submitted = st.form_submit_button("📤 Submit Evidence")
            
            if submitted:
                if description:
                    result = create_evidence(selected_asset_id, evidence_type, description, gps_lat, gps_lon)
                    if result:
                        st.success(f"✅ Evidence logged successfully with ID: **{result['id']}**")
                        st.json(result)
                else:
                    st.error("Please provide a description for the evidence.")
    else:
        st.warning("⚠️ No assets available. Please register an asset first.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Land Truth Registry v1.0**")
st.sidebar.markdown("Immutable land tracking system")
