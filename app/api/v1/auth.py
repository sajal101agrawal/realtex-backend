from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from app.services.email_service import send_invitation_email
import uuid
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: User email
              example: user@example.com
            password:
              type: string
              description: User password
              example: password123
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            user:
              type: object
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Account is not active. Please complete the invitation process.'}), 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    ---
    tags:
      - Authentication
    security:
      - JWT: []
    responses:
      200:
        description: Token refreshed successfully
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Invalid token
    """
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/accept-invitation', methods=['POST'])
def accept_invitation():
    """
    Accept user invitation and set password
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - token
            - password
          properties:
            token:
              type: string
              description: Invitation token
              example: abc123def456
            password:
              type: string
              description: New password
              example: securepassword123
    responses:
      200:
        description: Invitation accepted successfully
      400:
        description: Invalid request
      404:
        description: Invalid token
    """
    data = request.get_json()
    
    if not data or not data.get('token') or not data.get('password'):
        return jsonify({'message': 'Missing token or password'}), 400
    
    user = User.query.filter_by(invitation_token=data['token']).first()
    
    if not user:
        return jsonify({'message': 'Invalid invitation token'}), 404
    
    user.set_password(data['password'])
    user.is_active = True
    user.invitation_accepted_at = datetime.utcnow()
    user.invitation_token = None
    
    db.session.commit()
    
    return jsonify({'message': 'Invitation accepted successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user information
    ---
    tags:
      - Authentication
    security:
      - JWT: []
    responses:
      200:
        description: User information
        schema:
          type: object
      401:
        description: Invalid token
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200
