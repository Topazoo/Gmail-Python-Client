# Clients
import os, smtplib

# Email utils
from email.message import EmailMessage
from email.headerregistry import Address

# Typing
from typing import Optional

class EmailClient:
    ''' Client to send emails via SMTP using raw credentials
        Note: This is not allowed for Gmail anymore
    '''

    DEFAULT_EMAIL_SERVER = "smtp.gmail.com"
    DEFAULT_EMAIL_SERVER_PORT = 587

    def __init__(self,
                 email_server:Optional[str]=None,
                 email_port:Optional[int]=None,
                 sender_email_address:Optional[str]=None,
                 sender_email_password:Optional[str]=None
            ) -> None:

        # Allow user specified email server to override the default
        if email_server:
            self.DEFAULT_EMAIL_SERVER = email_server

        # Allow user specified email server port to override the default
        if email_port:
            self.DEFAULT_EMAIL_SERVER_PORT = email_port

        # The default outgoing email address info
        self.sender_email_address = sender_email_address or os.environ.get('SENDER_EMAIL_ADDRESS')
        self.sender_email_password = sender_email_password or os.environ.get('SENDER_EMAIL_PASSWORD')


    def _templatize_text(self, text:str, template:Optional[str], template_values:Optional[dict]) -> str:
        ''' Validate arguments and apply template values to template if passed '''

        # Handle errors
        if not text and not template:
            raise ValueError('send_email() must be passed email body text or an HTML template')

        if text and template:
            raise ValueError('send_email() cannot be passed both email body text and an HTML template')

        if template:
            text = self._format_template(template, template_values or {})

        return text


    def _send_email(self, email:EmailMessage, recipient_email_address:str):
        ''' Internal method that invokes the actual client to send the message '''

        # Open client and connect
        client = smtplib.SMTP(self.DEFAULT_EMAIL_SERVER, self.DEFAULT_EMAIL_SERVER_PORT)
        client.ehlo()
        client.starttls()

        # Login and send email
        client.login(self.sender_email_address or '', self.sender_email_password or '')
        client.sendmail(self.sender_email_address or '', recipient_email_address, email.as_string())
        
        client.quit()


    def send_email(self, recipient_email_address:str, subject:str, text:Optional[str]=None, template:Optional[str]=None, template_values:Optional[dict]=None):
        ''' Send an email to a recipient with plain text or using an HTML template 
            
            A map of template values should be passed if a template is used to populate the template
        '''

        # Generate email from template and values if passed
        text = self._templatize_text(text or '', template, template_values)
            
        # Create the email object
        email = self._generate_email_object(recipient_email_address, subject, text, 'plain' if not template else 'html')

        # Use the client to send the email object
        self._send_email(email, recipient_email_address)


    def _generate_email_object(self, recipient_email_address:str, subject:str, text, type="plain") -> EmailMessage:
        ''' Create the email object to send '''

        email = EmailMessage()

        email['From'] = Address(domain=self.sender_email_address)
        email['To'] = Address(domain=recipient_email_address)
        email['Subject'] = subject

        # Add body content
        email.add_alternative(text, type)

        return email


    def _format_template(self, template:str, template_values:dict):
        ''' Format the template '''

        for key, value in template_values.items():
            template = template.replace("{" + key + "}", value)

        return template