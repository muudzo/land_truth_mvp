"""
Seed data script for Land Truth Registry MVP.
Creates demo assets with Zimbabwe coordinates and historical data.
"""
import requests
import time
from datetime import datetime, timedelta

API_URL = "http://localhost:8000"
MAX_RETRIES = 30
RETRY_DELAY = 2  # seconds


def wait_for_api():
    """Wait for the API to be available with retry logic"""
    print("Waiting for API to be available...")
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"{API_URL}/")
            if response.status_code == 200:
                print("✅ API is online!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"Attempt {attempt + 1}/{MAX_RETRIES}: API not ready, retrying in {RETRY_DELAY}s...")
        time.sleep(RETRY_DELAY)
    
    print("❌ API failed to start after maximum retries")
    return False


def create_asset(name, owner, lat, lon, size):
    """Create an asset and return its ID"""
    payload = {
        "name": name,
        "owner": owner,
        "location_lat": lat,
        "location_lon": lon,
        "size_hectares": size
    }
    response = requests.post(f"{API_URL}/assets/", json=payload)
    response.raise_for_status()
    asset = response.json()
    print(f"✅ Created asset: {name} (ID: {asset['id']})")
    return asset['id']


def log_evidence(asset_id, evidence_type, description, lat, lon):
    """Log evidence for an asset"""
    payload = {
        "asset_id": asset_id,
        "evidence_type": evidence_type,
        "description": description,
        "gps_lat": lat,
        "gps_lon": lon
    }
    response = requests.post(f"{API_URL}/evidence/", json=payload)
    response.raise_for_status()
    evidence = response.json()
    print(f"  📸 Logged evidence: {evidence_type} - {description}")
    return evidence['id']


def seed_data():
    """Seed the database with demo data"""
    print("\n" + "="*60)
    print("🌱 SEEDING LAND TRUTH REGISTRY DATABASE")
    print("="*60 + "\n")
    
    # Asset 1: Mashonaland Plot 4
    print("📍 Creating Asset 1: Mashonaland Plot 4")
    asset1_id = create_asset(
        name="Mashonaland Plot 4",
        owner="Tendai Moyo",
        lat=-17.8252,
        lon=31.0335,
        size=12.5
    )
    
    # Evidence for Asset 1
    log_evidence(
        asset1_id,
        "Photo",
        "Boundary fencing completed - northern perimeter",
        -17.8250,
        31.0330
    )
    log_evidence(
        asset1_id,
        "Survey",
        "Land survey conducted by Zimbabwe Surveyor General",
        -17.8252,
        31.0335
    )
    log_evidence(
        asset1_id,
        "Document",
        "Title deed registration confirmed at Deeds Office",
        -17.8252,
        31.0335
    )
    log_evidence(
        asset1_id,
        "Inspection",
        "Soil quality assessment - Grade A agricultural land",
        -17.8255,
        31.0340
    )
    
    print()
    
    # Asset 2: Harare Warehouse District
    print("📍 Creating Asset 2: Harare Warehouse District")
    asset2_id = create_asset(
        name="Harare Warehouse District",
        owner="Zimbabwe Commercial Properties Ltd",
        lat=-17.8292,
        lon=31.0522,
        size=3.2
    )
    
    # Evidence for Asset 2
    log_evidence(
        asset2_id,
        "Photo",
        "Warehouse construction phase 1 completed",
        -17.8292,
        31.0522
    )
    log_evidence(
        asset2_id,
        "Document",
        "Building permit approved by Harare City Council",
        -17.8292,
        31.0522
    )
    log_evidence(
        asset2_id,
        "Inspection",
        "Fire safety inspection passed - Certificate issued",
        -17.8290,
        31.0520
    )
    
    print()
    
    # Asset 3: Manicaland Orchard Estate
    print("📍 Creating Asset 3: Manicaland Orchard Estate")
    asset3_id = create_asset(
        name="Manicaland Orchard Estate",
        owner="Nyasha Chikwanha",
        lat=-18.9707,
        lon=32.6729,
        size=25.8
    )
    
    # Evidence for Asset 3
    log_evidence(
        asset3_id,
        "Photo",
        "Citrus orchard planting - 500 trees planted",
        -18.9705,
        32.6725
    )
    log_evidence(
        asset3_id,
        "Harvest Report",
        "First harvest yield: 12 tonnes of oranges",
        -18.9707,
        32.6729
    )
    log_evidence(
        asset3_id,
        "Survey",
        "Irrigation system installation completed",
        -18.9710,
        32.6730
    )
    log_evidence(
        asset3_id,
        "Document",
        "Organic certification awarded by Zimbabwe Organic Producers",
        -18.9707,
        32.6729
    )
    
    print()
    print("="*60)
    print("✅ SEEDING COMPLETE!")
    print("="*60)
    print(f"\nCreated 3 assets with multiple evidence records")
    print(f"You can now access the dashboard at http://localhost:8501")
    print()


if __name__ == "__main__":
    if wait_for_api():
        try:
            seed_data()
        except Exception as e:
            print(f"\n❌ Error during seeding: {str(e)}")
            exit(1)
    else:
        print("\n❌ Could not connect to API. Make sure the backend is running.")
        exit(1)
