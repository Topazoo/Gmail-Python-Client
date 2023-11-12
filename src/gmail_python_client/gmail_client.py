# Clients
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from .email_client import EmailClient
from email.message import EmailMessage

# Utils
from googleapiclient.discovery import build as build_creds
import os, base64

# Typing
from typing import Optional


class GmailClient(EmailClient):
    ''' Client to send emails via the GMail API 
    
        Requires the following environmental variables or arguments:
        sender_email_address (env: `GMAIL_SENDER_EMAIL_ADDRESS`) - The email address being used to send emails
        access_token (env: `GMAIL_OAUTH_ACCESS_TOKEN`) - A Google OAuth Access Token
        refresh_token (env: `GMAIL_OAUTH_REFRESH_TOKEN`) - A Google OAuth Refresh Token
        client_id (env: `GMAIL_OAUTH_CLIENT_ID`) - A Google OAuth Client ID
        client_secret (env: `GMAIL_OAUTH_CLIENT_SECRET`) - A Google OAuth Client Secret Key
    '''

    def __init__(self,
            sender_email_address:Optional[str]=None,
            access_token:Optional[str]=None,
            refresh_token:Optional[str]=None,
            client_id:Optional[str]=None,
            client_secret:Optional[str]=None,
        ) -> None:
    
        super().__init__(sender_email_address=sender_email_address or os.environ.get('GMAIL_SENDER_EMAIL_ADDRESS'))
        # Store credentials if passed or read from env
        self.access_token = access_token or os.environ.get('GMAIL_OAUTH_ACCESS_TOKEN')
        self.refresh_token = refresh_token or os.environ.get('GMAIL_OAUTH_REFRESH_TOKEN')
        self.client_id = client_id or os.environ.get('GMAIL_OAUTH_CLIENT_ID')
        self.client_secret = client_secret or os.environ.get('GMAIL_OAUTH_CLIENT_SECRET')

        # Login to GMail
        self.service = self._login()


    def _login(self):
        credentials = Credentials(
            self.access_token,
            refresh_token=self.refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=['https://www.googleapis.com/auth/gmail.send']
        )

        if self.refresh_token and self.client_id and self.client_secret:
            credentials.refresh(Request())

        service = build_creds('gmail', 'v1', credentials=credentials)

        return service


    def _generate_email_object(self, recipient_email_address:str, subject:str, text, type="plain") -> EmailMessage:
        ''' Create the email object to send '''

        email = EmailMessage()

        email['From'] = self.sender_email_address
        email['To'] = recipient_email_address
        email['Subject'] = subject

        # Add body content
        email.add_alternative(text, type)

        return email


    def _send_email(self, email:EmailMessage, _):
        ''' Internal method that invokes the actual client to send the message '''

        self.service.users().messages().send(userId='me', body={'raw': base64.urlsafe_b64encode(email.as_bytes()).decode()}).execute()