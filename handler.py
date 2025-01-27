import os
import smtplib
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# If modifying or sending emails, use the correct Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Load credentials from token file
def authenticate_gmail_api():
    """Handles OAuth2 authentication for Gmail API"""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def send_email(receiver_email, subject, body_text):
    try:
        sender_email = "aastha.banaotech@gmail.com"
        password = "lrde mafc mnxo dzig"  # App password should be set here

        # Prepare the email content
        message = f"Subject: {subject}\n\n{body_text}"

        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully!"})
        }

    except smtplib.SMTPAuthenticationError:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Authentication failed. Check your credentials."})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error sending email: {str(e)}"})
        }

def handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event['body'])

        receiver_email = body['receiver_email']
        subject = body['subject']
        body_text = body['body_text']

        # Call the send_email function to send the email
        return send_email(receiver_email, subject, body_text)

    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Missing required field: {str(e)}"})
        }
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON format"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"An unexpected error occurred: {str(e)}"})
        }

def serve_frontend(event, context):
    file_path = os.path.join(os.path.dirname(__file__), 'index.html')
    
    with open(file_path, 'r') as file:
        html_content = file.read()

    print("Serving frontend...")  # Debug log to confirm this function is being hit

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html_content,
    }