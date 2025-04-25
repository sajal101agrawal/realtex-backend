from datetime import datetime
from app import db

class Area(db.Model):
    __tablename__ = 'areas'
    
    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    avg_price = db.Column(db.Float)
    avg_rent = db.Column(db.Float)
    rental_yield = db.Column(db.Float)
    investment_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'area_name': self.area_name,
            'country': self.country,
            'avg_price': self.avg_price,
            'avg_rent': self.avg_rent,
            'rental_yield': self.rental_yield,
            'investment_score': self.investment_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
