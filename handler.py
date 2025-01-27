import os
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receiver_email, subject, body_text):
    try:
        # Use your Gmail address and app-specific password
        sender_email = "" #add your email
        password = ""  # Replace this with your app-specific password

        # Prepare the email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body_text, 'plain'))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

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
