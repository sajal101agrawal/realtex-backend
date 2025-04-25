# Realtex AI - Flask Backend

A Flask backend for the Realtex AI real estate platform with Swagger documentation and admin invitation functionality.

## Features

- User authentication with JWT
- Admin user management system
- User invitation system with email notifications
- Real estate property price prediction
- Rental yield estimation
- Capital growth prediction
- Area investment scoring
- Comprehensive API documentation with Swagger

## Project Structure

```
realtex/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── admin.py        # Admin user management endpoints
│   │       ├── auth.py         # Authentication endpoints
│   │       └── predictions.py  # Real estate prediction endpoints
│   ├── models/
│   │   ├── area.py             # Area model
│   │   ├── prediction.py       # Prediction model
│   │   ├── property.py         # Property model
│   │   └── user.py             # User model with invitation functionality
│   ├── services/
│   │   └── email_service.py    # Email service for user invitations
│   ├── utils/
│   │   ├── env_setup.py        # Environment setup utilities
│   │   └── swagger_utils.py    # Swagger configuration utilities
│   ├── __init__.py             # Flask application factory
│   └── config.py               # Application configuration
├── migrations/                 # Database migrations
├── manage.py                   # Management script
├── run.py                      # Application entry point
├── test_api.py                 # API test script
└── requirements.txt            # Project dependencies
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the project root with the following variables:
     ```
     FLASK_APP=manage.py
     FLASK_ENV=development
     SECRET_KEY=your-secret-key
     JWT_SECRET_KEY=your-jwt-secret-key
     DATABASE_URL=postgresql://username:password@localhost/dbname
     MAIL_SERVER=smtp.example.com
     MAIL_PORT=587
     MAIL_USE_TLS=True
     MAIL_USERNAME=your-email@example.com
     MAIL_PASSWORD=your-email-password
     MAIL_DEFAULT_SENDER=noreply@realtex.ai
     ```

5. Initialize the database:
   ```
   flask init-db
   ```

6. Create an admin user:
   ```
   flask create-admin
   ```

## Running the Application

```
flask run
```

The application will be available at http://localhost:5000.

API documentation will be available at http://localhost:5000/api/docs/.

## Testing

Run the test script to validate all APIs:

```
python test_api.py
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/accept-invitation` - Accept user invitation
- `GET /api/v1/auth/me` - Get current user information

### Admin User Management

- `POST /api/v1/admin/users` - Create and invite a new user
- `GET /api/v1/admin/users` - Get all users
- `GET /api/v1/admin/users/{user_id}` - Get a specific user
- `PUT /api/v1/admin/users/{user_id}` - Update a user
- `DELETE /api/v1/admin/users/{user_id}` - Delete a user
- `POST /api/v1/admin/users/{user_id}/resend-invitation` - Resend invitation to a user

### Real Estate Predictions

- `POST /api/v1/predictions/price` - Predict property price
- `POST /api/v1/predictions/rent` - Predict property rental yield
- `POST /api/v1/predictions/capital-growth` - Predict property capital growth
- `GET /api/v1/predictions/area-score` - Get investment score for an area
