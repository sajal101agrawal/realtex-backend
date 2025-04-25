from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from app.services.email_service import send_invitation_email
import uuid
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    """
    Create and invite a new user (Admin only)
    ---
    tags:
      - Admin
    security:
      - JWT: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
              description: User email
              example: newuser@example.com
            first_name:
              type: string
              description: User first name
              example: John
            last_name:
              type: string
              description: User last name
              example: Doe
            is_admin:
              type: boolean
              description: Whether the user is an admin
              example: false
    responses:
      201:
        description: User created and invited successfully
      400:
        description: Invalid request
      401:
        description: Unauthorized
      403:
        description: Not an admin
      409:
        description: User already exists
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'message': 'Email is required'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists'}), 409
    
    # Create new user
    new_user = User(
        email=data['email'],
        is_admin=data.get('is_admin', False)
    )
    
    if data.get('first_name'):
        new_user.first_name = data['first_name']
    
    if data.get('last_name'):
        new_user.last_name = data['last_name']
    
    # Generate invitation token
    invitation_token = str(uuid.uuid4())
    new_user.invitation_token = invitation_token
    new_user.invitation_sent_at = datetime.utcnow()
    
    db.session.add(new_user)
    db.session.commit()
    
    # Send invitation email
    send_invitation_email(new_user.email, invitation_token)
    
    return jsonify({
        'message': 'User created and invitation sent successfully',
        'user': new_user.to_dict()
    }), 201

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Get all users (Admin only)
    ---
    tags:
      - Admin
    security:
      - JWT: []
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            type: object
      401:
        description: Unauthorized
      403:
        description: Not an admin
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Get a specific user (Admin only)
    ---
    tags:
      - Admin
    security:
      - JWT: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User details
        schema:
          type: object
      401:
        description: Unauthorized
      403:
        description: Not an admin
      404:
        description: User not found
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update a user (Admin only)
    ---
    tags:
      - Admin
    security:
      - JWT: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User email
            first_name:
              type: string
              description: User first name
            last_name:
              type: string
              description: User last name
            is_admin:
              type: boolean
              description: Whether the user is an admin
            is_active:
              type: boolean
              description: Whether the user is active
    responses:
      200:
        description: User updated successfully
      400:
        description: Invalid request
      401:
        description: Unauthorized
      403:
        description: Not an admin
      404:
        description: User not found
      409:
        description: Email already in use
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    # Check if email is being changed and if it's already in use
    if data.get('email') and data['email'] != user.email:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'Email already in use'}), 409
        user.email = data['email']
    
    # Update other fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Delete a user (Admin only)
    ---
    tags:
      - Admin
    security:
      - JWT: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User deleted successfully
      401:
        description: Unauthorized
      403:
        description: Not an admin
      404:
        description: User not found
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    # Prevent self-deletion
    if int(user_id) == current_user_id:
        return jsonify({'message': 'Cannot delete your own account'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200

@admin_bp.route('/users/<int:user_id>/resend-invitation', methods=['POST'])
@jwt_required()
def resend_invitation(user_id):
    """
    Resend invitation to a user (Admin only)
    ---
    tags:
      - Admin
    security:
      - JWT: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: Invitation resent successfully
      401:
        description: Unauthorized
      403:
        description: Not an admin
      404:
        description: User not found
      400:
        description: User already active
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if user.is_active:
        return jsonify({'message': 'User is already active'}), 400
    
    # Generate new invitation token
    invitation_token = str(uuid.uuid4())
    user.invitation_token = invitation_token
    user.invitation_sent_at = datetime.utcnow()
    
    db.session.commit()
    
    # Send invitation email
    send_invitation_email(user.email, invitation_token)
    
    return jsonify({'message': 'Invitation resent successfully'}), 200
