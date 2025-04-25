from datetime import datetime
from app import db

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    size_sqft = db.Column(db.Float, nullable=False)
    num_bedrooms = db.Column(db.Integer, nullable=False)
    num_bathrooms = db.Column(db.Integer, nullable=False)
    listing_price = db.Column(db.Float, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with predictions
    predictions = db.relationship('Prediction', backref='property', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'postcode': self.postcode,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'size_sqft': self.size_sqft,
            'num_bedrooms': self.num_bedrooms,
            'num_bathrooms': self.num_bathrooms,
            'listing_price': self.listing_price,
            'property_type': self.property_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
