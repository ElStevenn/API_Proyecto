import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from configparser import ConfigParser
from pathlib import Path
from .security.enviroment import env_variable
import asyncio

class EmailSender:
    """
        Class to send emails with SMTP protocol
    
    """
    def __init__(self):
        self.password = "notificacioclient@gmail.com"
        self.email = env_variable["APP_PASSWORD"]

    def send_email(self, receiver_email, subject, message_body):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)

            msg = MIMEMultipart()
            msg.attach(MIMEText(message_body, 'html', 'utf-8'))  # Puesto en formato html, se puede cambiar también a txt
            msg["Subject"] = Header(subject, 'utf-8')
            msg["From"] = self.email
            msg["To"] = receiver_email

            server.sendmail(self.email, receiver_email, msg.as_string())
            print("Email has been sent successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            server.quit()


class MailHandle(EmailSender):
    logo_url = "http://apitravel360.homes/logo_app"

    def send_user_as_registered(self, user_name, user_email):
        # HTML structure for the email content
        html_content = f"""
        <html>
        <head>
            <style>
                .header {{
                    background-color: #4CAF50; /* Green background */
                    color: white;
                    text-align: center;
                    padding: 10px;
                }}
                .content {{
                    margin: 20px;
                    text-align: center;
                }}
                img {{
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Travel360</h1>
            </div>
            <div class="content">
                <img src="{self.logo_url}" alt="Travel360 Logo">
                <p>Dear {user_name},</p>
                <p>You have been successfully registered!</p>
            </div>
        </body>
        </html>
        """
        self.send_email(user_email, f"Successful Registration for {user_name}", html_content)

    


if __name__ == "__main__":
    email_handler = MailHandle()
    email_handler.send_user_as_registered("Pau Mateu", "paumat17@gmail.com")