from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Video(db.Model):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    icon_uri = Column(String, nullable=False)
    description = Column(String)
    disabled = Column(Boolean, nullable=False)
    is_featured = Column(Boolean, nullable=False)

    features = relationship('VideoFeature', back_populates='video')


class Feature(db.Model):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    videos = relationship('VideoFeature', back_populates='feature')


class VideoFeature(db.Model):
    __tablename__ = 'videos_features'
    video_id = Column(Integer, ForeignKey('videos.id'), primary_key=True)
    feature_id = Column(Integer, ForeignKey('features.id'), primary_key=True)

    video = relationship('Video', back_populates="features")
    feature = relationship('Feature', back_populates="videos")
