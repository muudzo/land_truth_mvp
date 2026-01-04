from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Asset Schemas
class AssetCreate(BaseModel):
    """Schema for creating a new asset"""
    name: str = Field(..., min_length=1, max_length=255, description="Asset name")
    owner: str = Field(..., min_length=1, max_length=255, description="Owner name")
    location_lat: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    location_lon: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    size_hectares: float = Field(..., gt=0, description="Size in hectares")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mashonaland Plot 4",
                "owner": "John Doe",
                "location_lat": -17.8252,
                "location_lon": 31.0335,
                "size_hectares": 5.5
            }
        }


class AssetResponse(BaseModel):
    """Schema for asset response"""
    id: int
    name: str
    owner: str
    location_lat: float
    location_lon: float
    size_hectares: float
    created_at: datetime

    class Config:
        from_attributes = True


# Evidence Schemas
class EvidenceCreate(BaseModel):
    """Schema for creating evidence"""
    asset_id: int = Field(..., gt=0, description="Asset ID")
    evidence_type: str = Field(..., min_length=1, max_length=100, description="Type of evidence")
    description: str = Field(..., min_length=1, description="Evidence description")
    gps_lat: float = Field(..., ge=-90, le=90, description="GPS latitude")
    gps_lon: float = Field(..., ge=-180, le=180, description="GPS longitude")

    class Config:
        json_schema_extra = {
            "example": {
                "asset_id": 1,
                "evidence_type": "Photo",
                "description": "Fencing installation completed",
                "gps_lat": -17.8252,
                "gps_lon": 31.0335
            }
        }


class EvidenceResponse(BaseModel):
    """Schema for evidence response"""
    id: int
    asset_id: int
    evidence_type: str
    description: str
    gps_lat: float
    gps_lon: float
    timestamp: datetime

    class Config:
        from_attributes = True


# Timeline Schemas
class TimelineEvent(BaseModel):
    """Unified schema for timeline events (versions and evidence)"""
    event_type: str  # "version" or "evidence"
    timestamp: datetime
    description: str
    details: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "version",
                "timestamp": "2024-01-04T15:30:00",
                "description": "Genesis Creation",
                "details": {"owner": "John Doe", "name": "Mashonaland Plot 4"}
            }
        }


class AssetVersionResponse(BaseModel):
    """Schema for asset version response"""
    id: int
    asset_id: int
    name: str
    owner: str
    change_reason: str
    changed_at: datetime

    class Config:
        from_attributes = True
