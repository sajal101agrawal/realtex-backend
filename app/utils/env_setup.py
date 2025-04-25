from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://realtex_user:securepassword@localhost/realtex_db')

# Create .env file with default values
ENV_CONTENT = f"""# Flask configuration
FLASK_APP=manage.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production

# Database configuration
DATABASE_URL={DATABASE_URL}

# Mail configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@realtex.ai
"""
