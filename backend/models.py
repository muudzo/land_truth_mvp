from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Asset(Base):
    """
    Main asset table representing land parcels or properties.
    This is the current state of the asset.
    """
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    owner = Column(String(255), nullable=False)
    location_lat = Column(Float, nullable=False)
    location_lon = Column(Float, nullable=False)
    size_hectares = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    versions = relationship("AssetVersion", back_populates="asset", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="asset", cascade="all, delete-orphan")


class AssetVersion(Base):
    """
    Immutable history table tracking all changes to assets.
    Each row represents a snapshot or change event.
    """
    __tablename__ = "asset_versions"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    change_reason = Column(String(500), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    asset = relationship("Asset", back_populates="versions")


class Evidence(Base):
    """
    Evidence table storing proof of asset status, changes, or events.
    Includes GPS coordinates and timestamps for verification.
    """
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    gps_lat = Column(Float, nullable=False)
    gps_lon = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    asset = relationship("Asset", back_populates="evidence")
