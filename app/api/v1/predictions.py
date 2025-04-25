from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.property import Property
from app.models.prediction import Prediction
from app.models.area import Area
from app.models.user import User
from app import db
import datetime

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/price', methods=['POST'])
@jwt_required()
def predict_price():
    """
    Predict property price
    ---
    tags:
      - Predictions
    security:
      - JWT: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - location
            - size_sqft
            - num_bedrooms
            - num_bathrooms
            - property_type
          properties:
            location:
              type: string
              description: Property location (city, country)
              example: "London, UK"
            size_sqft:
              type: number
              description: Property size in square feet
              example: 1200
            num_bedrooms:
              type: integer
              description: Number of bedrooms
              example: 3
            num_bathrooms:
              type: integer
              description: Number of bathrooms
              example: 2
            property_type:
              type: string
              description: Type of property
              example: "Apartment"
    responses:
      200:
        description: Price prediction
        schema:
          type: object
          properties:
            predicted_price:
              type: number
      400:
        description: Invalid request
      401:
        description: Unauthorized
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    required_fields = ['location', 'size_sqft', 'num_bedrooms', 'num_bathrooms', 'property_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Simple dummy prediction for demonstration
    # In a real implementation, this would use a trained ML model
    base_price = 200000
    location_factor = 1.0
    
    if 'London' in data['location']:
        location_factor = 2.5
    elif 'New York' in data['location']:
        location_factor = 3.0
    elif 'Paris' in data['location']:
        location_factor = 2.2
    elif 'Dubai' in data['location']:
        location_factor = 1.8
    
    property_type_factor = 1.0
    if data['property_type'] == 'Detached House':
        property_type_factor = 1.5
    elif data['property_type'] == 'Semi-detached House':
        property_type_factor = 1.3
    elif data['property_type'] == 'Townhouse':
        property_type_factor = 1.2
    elif data['property_type'] == 'Villa':
        property_type_factor = 1.8
    
    predicted_price = (
        base_price +
        (data['size_sqft'] * 200) +
        (data['num_bedrooms'] * 25000) +
        (data['num_bathrooms'] * 15000)
    ) * location_factor * property_type_factor
    
    return jsonify({'predicted_price': predicted_price}), 200

@predictions_bp.route('/rent', methods=['POST'])
@jwt_required()
def predict_rent():
    """
    Predict property rental yield
    ---
    tags:
      - Predictions
    security:
      - JWT: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - location
            - size_sqft
            - num_bedrooms
            - num_bathrooms
            - property_type
          properties:
            location:
              type: string
              description: Property location (city, country)
              example: "London, UK"
            size_sqft:
              type: number
              description: Property size in square feet
              example: 1200
            num_bedrooms:
              type: integer
              description: Number of bedrooms
              example: 3
            num_bathrooms:
              type: integer
              description: Number of bathrooms
              example: 2
            property_type:
              type: string
              description: Type of property
              example: "Apartment"
    responses:
      200:
        description: Rental yield prediction
        schema:
          type: object
          properties:
            predicted_monthly_rent:
              type: number
            predicted_annual_rent:
              type: number
            predicted_rental_yield:
              type: number
      400:
        description: Invalid request
      401:
        description: Unauthorized
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    required_fields = ['location', 'size_sqft', 'num_bedrooms', 'num_bathrooms', 'property_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Get predicted price first
    price_response = predict_price()
    predicted_price = price_response[0].json['predicted_price']
    
    # Simple dummy rent prediction for demonstration
    # In a real implementation, this would use a trained ML model
    base_rent = 1000
    location_factor = 1.0
    
    if 'London' in data['location']:
        location_factor = 1.8
    elif 'New York' in data['location']:
        location_factor = 2.2
    elif 'Paris' in data['location']:
        location_factor = 1.6
    elif 'Dubai' in data['location']:
        location_factor = 1.4
    
    property_type_factor = 1.0
    if data['property_type'] == 'Detached House':
        property_type_factor = 1.3
    elif data['property_type'] == 'Semi-detached House':
        property_type_factor = 1.2
    elif data['property_type'] == 'Townhouse':
        property_type_factor = 1.1
    elif data['property_type'] == 'Villa':
        property_type_factor = 1.5
    
    predicted_monthly_rent = (
        base_rent +
        (data['size_sqft'] * 0.5) +
        (data['num_bedrooms'] * 300) +
        (data['num_bathrooms'] * 150)
    ) * location_factor * property_type_factor
    
    predicted_annual_rent = predicted_monthly_rent * 12
    predicted_rental_yield = (predicted_annual_rent / predicted_price) * 100
    
    return jsonify({
        'predicted_monthly_rent': predicted_monthly_rent,
        'predicted_annual_rent': predicted_annual_rent,
        'predicted_rental_yield': predicted_rental_yield
    }), 200

@predictions_bp.route('/capital-growth', methods=['POST'])
@jwt_required()
def predict_capital_growth():
    """
    Predict property capital growth
    ---
    tags:
      - Predictions
    security:
      - JWT: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - location
            - property_type
          properties:
            location:
              type: string
              description: Property location (city, country)
              example: "London, UK"
            property_type:
              type: string
              description: Type of property
              example: "Apartment"
    responses:
      200:
        description: Capital growth prediction
        schema:
          type: object
          properties:
            predicted_capital_growth_1y:
              type: number
            predicted_capital_growth_3y:
              type: number
            predicted_capital_growth_5y:
              type: number
      400:
        description: Invalid request
      401:
        description: Unauthorized
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    required_fields = ['location', 'property_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Simple dummy capital growth prediction for demonstration
    # In a real implementation, this would use a trained ML model
    base_growth_1y = 3.0
    base_growth_3y = 9.5
    base_growth_5y = 16.0
    
    location_factor = 1.0
    if 'London' in data['location']:
        location_factor = 1.2
    elif 'New York' in data['location']:
        location_factor = 1.3
    elif 'Paris' in data['location']:
        location_factor = 1.1
    elif 'Dubai' in data['location']:
        location_factor = 1.4
    
    property_type_factor = 1.0
    if data['property_type'] == 'Detached House':
        property_type_factor = 1.1
    elif data['property_type'] == 'Land Plot':
        property_type_factor = 1.2
    
    predicted_capital_growth_1y = base_growth_1y * location_factor * property_type_factor
    predicted_capital_growth_3y = base_growth_3y * location_factor * property_type_factor
    predicted_capital_growth_5y = base_growth_5y * location_factor * property_type_factor
    
    return jsonify({
        'predicted_capital_growth_1y': predicted_capital_growth_1y,
        'predicted_capital_growth_3y': predicted_capital_growth_3y,
        'predicted_capital_growth_5y': predicted_capital_growth_5y
    }), 200

@predictions_bp.route('/area-score', methods=['GET'])
@jwt_required()
def get_area_score():
    """
    Get investment score for an area
    ---
    tags:
      - Predictions
    security:
      - JWT: []
    parameters:
      - name: area
        in: query
        type: string
        required: true
        description: Area name
      - name: country
        in: query
        type: string
        required: true
        description: Country
    responses:
      200:
        description: Area investment score
        schema:
          type: object
          properties:
            area_name:
              type: string
            country:
              type: string
            investment_score:
              type: number
            avg_price:
              type: number
            avg_rent:
              type: number
            rental_yield:
              type: number
      400:
        description: Invalid request
      401:
        description: Unauthorized
      404:
        description: Area not found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'message': 'Unauthorized'}), 401
    
    area_name = request.args.get('area')
    country = request.args.get('country')
    
    if not area_name or not country:
        return jsonify({'message': 'Area name and country are required'}), 400
    
    # Check if area exists in database
    area = Area.query.filter_by(area_name=area_name, country=country).first()
    
    # If area doesn't exist, create dummy data
    # In a real implementation, this would use a trained ML model
    if not area:
        # Generate dummy data based on area name
        investment_score = 65.0
        avg_price = 350000.0
        avg_rent = 1500.0
        rental_yield = 5.1
        
        if 'London' in area_name or 'New York' in area_name:
            investment_score = 78.5
            avg_price = 750000.0
            avg_rent = 3000.0
            rental_yield = 4.8
        elif 'Paris' in area_name or 'Berlin' in area_name:
            investment_score = 72.0
            avg_price = 550000.0
            avg_rent = 2200.0
            rental_yield = 4.8
        elif 'Dubai' in area_name:
            investment_score = 81.0
            avg_price = 650000.0
            avg_rent = 3500.0
            rental_yield = 6.5
        
        # Create new area record
        area = Area(
            area_name=area_name,
            country=country,
            avg_price=avg_price,
            avg_rent=avg_rent,
            rental_yield=rental_yield,
            investment_score=investment_score
        )
        db.session.add(area)
        db.session.commit()
    
    return jsonify({
        'area_name': area.area_name,
        'country': area.country,
        'investment_score': area.investment_score,
        'avg_price': area.avg_price,
        'avg_rent': area.avg_rent,
        'rental_yield': area.rental_yield
    }), 200
