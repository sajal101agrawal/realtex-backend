from flask import Flask
from flask_migrate import Migrate

# Import db and create_app directly
from app import db, create_app

app = create_app('development')
migrate = Migrate(app, db)

@app.cli.command('init-db')
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    print('Database initialized successfully')

@app.cli.command('create-admin')
def create_admin():
    """Create an admin user"""
    from app.models.user import User
    
    admin_email = 'admin@realtex.ai'
    admin = User.query.filter_by(email=admin_email).first()
    
    if admin:
        print(f'Admin user {admin_email} already exists')
        return
    
    admin = User(
        email=admin_email,
        password='admin123',  # This would be a secure password in production
        is_admin=True
    )
    admin.is_active = True
    admin.first_name = 'Admin'
    admin.last_name = 'User'
    
    db.session.add(admin)
    db.session.commit()
    
    print(f'Admin user {admin_email} created successfully')

if __name__ == '__main__':
    app.run(debug=True)
