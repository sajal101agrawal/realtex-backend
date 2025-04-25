from flask import Flask
from flask_mail import Message
from app import mail

def send_invitation_email(recipient_email, invitation_token):
    """
    Send invitation email to a new user
    
    Args:
        recipient_email (str): Email address of the recipient
        invitation_token (str): Invitation token for account activation
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        invitation_link = f"http://localhost:5000/accept-invitation?token={invitation_token}"
        
        msg = Message(
            subject="Welcome to Realtex AI - Invitation to Join",
            recipients=[recipient_email],
            html=f"""
            <h2>Welcome to Realtex AI</h2>
            <p>You have been invited to join the Realtex AI platform.</p>
            <p>Please click the link below to set your password and activate your account:</p>
            <p><a href="{invitation_link}">Accept Invitation</a></p>
            <p>This link will expire in 7 days.</p>
            <p>If you did not request this invitation, please ignore this email.</p>
            <p>Thank you,<br>The Realtex AI Team</p>
            """
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending invitation email: {str(e)}")
        return False
