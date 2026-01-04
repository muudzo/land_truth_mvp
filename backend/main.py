from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db, init_db
from models import Asset, AssetVersion, Evidence
from schemas import (
    AssetCreate, AssetResponse, 
    EvidenceCreate, EvidenceResponse,
    TimelineEvent, AssetVersionResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="Land Truth Registry API",
    description="Immutable land registry system with evidence tracking",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Land Truth Registry API",
        "version": "1.0.0"
    }


@app.post("/assets/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED, tags=["Assets"])
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    """
    Create a new asset and initialize its version history with a Genesis block.
    
    CRITICAL: This endpoint implements the "Genesis Creation" pattern.
    Every new asset gets an immediate AssetVersion entry to anchor its history.
    """
    # Create the asset
    db_asset = Asset(
        name=asset.name,
        owner=asset.owner,
        location_lat=asset.location_lat,
        location_lon=asset.location_lon,
        size_hectares=asset.size_hectares
    )
    db.add(db_asset)
    db.flush()  # Flush to get the ID without committing
    
    # CRITICAL: Create Genesis version entry
    genesis_version = AssetVersion(
        asset_id=db_asset.id,
        name=asset.name,
        owner=asset.owner,
        change_reason="Genesis Creation"
    )
    db.add(genesis_version)
    db.commit()
    db.refresh(db_asset)
    
    return db_asset


@app.get("/assets/", response_model=List[AssetResponse], tags=["Assets"])
def get_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all assets with pagination.
    """
    assets = db.query(Asset).offset(skip).limit(limit).all()
    return assets


@app.get("/assets/{asset_id}", response_model=AssetResponse, tags=["Assets"])
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific asset by ID.
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )
    return asset


@app.post("/evidence/", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED, tags=["Evidence"])
def create_evidence(evidence: EvidenceCreate, db: Session = Depends(get_db)):
    """
    Log evidence for an asset.
    Validates that the asset exists before creating evidence.
    """
    # Verify asset exists
    asset = db.query(Asset).filter(Asset.id == evidence.asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {evidence.asset_id} not found"
        )
    
    # Create evidence
    db_evidence = Evidence(
        asset_id=evidence.asset_id,
        evidence_type=evidence.evidence_type,
        description=evidence.description,
        gps_lat=evidence.gps_lat,
        gps_lon=evidence.gps_lon
    )
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    
    return db_evidence


@app.get("/assets/{asset_id}/timeline", response_model=List[TimelineEvent], tags=["Timeline"])
def get_asset_timeline(asset_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the complete timeline for an asset.
    
    Merges AssetVersion and Evidence records into a unified timeline,
    sorted by timestamp in descending order (most recent first).
    """
    # Verify asset exists
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )
    
    # Fetch versions
    versions = db.query(AssetVersion).filter(AssetVersion.asset_id == asset_id).all()
    
    # Fetch evidence
    evidence_records = db.query(Evidence).filter(Evidence.asset_id == asset_id).all()
    
    # Build unified timeline
    timeline = []
    
    # Add version events
    for version in versions:
        timeline.append(TimelineEvent(
            event_type="version",
            timestamp=version.changed_at,
            description=version.change_reason,
            details={
                "name": version.name,
                "owner": version.owner,
                "version_id": version.id
            }
        ))
    
    # Add evidence events
    for evidence in evidence_records:
        timeline.append(TimelineEvent(
            event_type="evidence",
            timestamp=evidence.timestamp,
            description=f"{evidence.evidence_type}: {evidence.description}",
            details={
                "evidence_type": evidence.evidence_type,
                "gps_lat": evidence.gps_lat,
                "gps_lon": evidence.gps_lon,
                "evidence_id": evidence.id
            }
        ))
    
    # Sort by timestamp descending (most recent first)
    timeline.sort(key=lambda x: x.timestamp, reverse=True)
    
    return timeline


@app.get("/evidence/", response_model=List[EvidenceResponse], tags=["Evidence"])
def get_all_evidence(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all evidence records with pagination.
    """
    evidence = db.query(Evidence).offset(skip).limit(limit).all()
    return evidence
