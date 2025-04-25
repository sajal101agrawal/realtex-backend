from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Import config here to avoid circular imports
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)
    
    # Import and configure Swagger here to avoid circular imports
    from app.utils.swagger_utils import configure_swagger
    configure_swagger(app)
    
    # Register blueprints
    from app.api.v1.auth import auth_bp
    from app.api.v1.admin import admin_bp
    from app.api.v1.predictions import predictions_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(predictions_bp, url_prefix='/api/v1/predictions')
    
    @app.route('/')
    def index():
        return {
            "message": "Realtex AI API is running",
            "documentation": "/api/docs/",
            "version": "1.0.0"
        }
    
    return app
