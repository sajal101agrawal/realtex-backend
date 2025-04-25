from datetime import datetime
from app import db

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    predicted_sale_price = db.Column(db.Float, nullable=False)
    predicted_rental_yield = db.Column(db.Float, nullable=False)
    predicted_capital_growth_1y = db.Column(db.Float, nullable=False)
    predicted_capital_growth_3y = db.Column(db.Float, nullable=False)
    predicted_capital_growth_5y = db.Column(db.Float, nullable=False)
    investment_score = db.Column(db.Float, nullable=False)
    model_version = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'predicted_sale_price': self.predicted_sale_price,
            'predicted_rental_yield': self.predicted_rental_yield,
            'predicted_capital_growth_1y': self.predicted_capital_growth_1y,
            'predicted_capital_growth_3y': self.predicted_capital_growth_3y,
            'predicted_capital_growth_5y': self.predicted_capital_growth_5y,
            'investment_score': self.investment_score,
            'model_version': self.model_version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
