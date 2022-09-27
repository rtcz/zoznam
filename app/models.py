from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    icon_uri = Column(String, nullable=False, unique=True)
    description = Column(String)
    disabled = Column(Boolean, nullable=False)
    is_featured = Column(Boolean, nullable=False)

    features = relationship('MovieFeature', back_populates='movie')


class Feature(db.Model):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    movies = relationship('MovieFeature', back_populates='feature')


class MovieFeature(db.Model):
    __tablename__ = 'movies_features'
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    feature_id = Column(Integer, ForeignKey('features.id'), primary_key=True)

    movie = relationship('Movie', back_populates="features")
    feature = relationship('Feature', back_populates="movies")
