from flask import Flask
from flasgger import Swagger

def configure_swagger(app):
    """
    Configure Swagger documentation for the Flask application
    
    Args:
        app (Flask): Flask application instance
    """
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Realtex AI API",
            "description": "API documentation for Realtex AI real estate platform",
            "version": "1.0.0",
            "contact": {
                "email": "support@realtex.ai"
            },
        },
        "securityDefinitions": {
            "JWT": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        },
        "security": [
            {
                "JWT": []
            }
        ],
        "tags": [
            {
                "name": "Authentication",
                "description": "User authentication endpoints"
            },
            {
                "name": "Admin",
                "description": "Admin user management endpoints"
            },
            {
                "name": "Predictions",
                "description": "Real estate prediction endpoints"
            }
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
