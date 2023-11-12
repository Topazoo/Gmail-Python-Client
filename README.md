# Gmail-Python-Client

Client for Sending Emails via GMail using OAuth2.0 for Python
https://developers.google.com/identity/protocols/oauth2

## Configuring a new project

### Installing

```sh
pip install gmail-python-client
```

### Google Cloud Configuration

1. Visit: https://console.cloud.google.com/apis/credentials while logged in to your Gmail Account
1. Create a new project for your application that is to send emails
1. Visit: https://console.developers.google.com/start/api?id=gmail to enable Gmail
1. Configure the OAuth consent screen: https://console.cloud.google.com/projectselector2/apis/credentials/consent?supportedpurview=project
1. Ensure the `https://www.googleapis.com/auth/gmail.send` scope is enabled
1. Create OAuth 2.0 credentials (select "Web application" as the application type) and save the JSON data
1. Make sure that the redirect URI (https://developers.google.com/oauthplayground) is added to the list of authorized redirect URIs in your project's OAuth 2.0 Client ID settings in Google Cloud Console.
1. Get a refresh token using the OAuth 2.0 Playground: https://developers.google.com/oauthplayground/
1. Click on the gear icon in the upper right corner of the OAuth 2.0 Playground to open the OAuth 2.0 Configuration.
1. Ensure that "Use your own OAuth credentials" is checked and fill in the "OAuth Client ID" and "OAuth Client secret" that you obtained from the Google Cloud Console.
1. Select the `https://www.googleapis.com/auth/gmail.send` scope.
1. Also, make sure the checkbox "Auto-refresh the token before it expires" is unchecked, because you need the refresh token to be able to generate new access tokens in your application.
1. Click "Exchange authorization code for tokens" to get your access token and refresh token.
1. (Note:) You can use the API Playground to generate an access token without creating an OAuth2.0 client ID directly, but it will only last 24 hours

### Application Configuration

Once you have a 24hour access token from the API Playground or a more permanenent combination of a Client ID, Client Secret and Refresh Token, you can use this library like so:

```python
from gmail_python_client import GmailClient

# Configure with Access Token
# Looks like:
# ya29.a0AfB_byDzLjqCbsdb_RMnguTrB8fmdSEsOSMkvWH6zjcm-1UIi3cdNpfvhZUjYZLVB7NrnNGJIEEatntXjBpc5Bk_cIGKgnjqtesO-HLT0H2Yiz-lZFviz3_UfaaoR8HLjmrKmm7VCkBZvdI0ABb4ADnY9fEKxcLMhR4daCgYKAQcSARASFQGOcNnCvZ0k13Q_KYFObZFjh5umXQ0171
if __name__ == '__main__':
    c = GmailClient(
        "my_sender_email@gmail.com",
        access_token="<access_token>",
    )

    # Send the email to pswanson@ucdavis.edu
    c.send_email("pswanson@ucdavis.edu", "Test", "Hello World!")
```

```python
from gmail_python_client import GmailClient

# Configure with Refresh Token
# Looks like:
# 1//04mDFqbnpQnGTCgYIARAAGAQSNwF-L9IruAAqiKvHXfHzZnMt6UqTzDOZGg4TJha3oCGa9utu_PwxfrmG-su47Qytt8m2eWDDwZo
if __name__ == '__main__':
    c = GmailClient(
        "my_sender_email@gmail.com",
        client_id="<client_id>",
        client_secret="<client_secret>",
        refresh_token="<refresh_token>",
    )

    # Send the email to pswanson@ucdavis.edu
    c.send_email("pswanson@ucdavis.edu", "Test", "Hello World!")
```

### Configuring via the Environment

You can configure the client using environmental variables rather than passing the configuration to the constructor:

```sh
# Configure with Access Token
export GMAIL_SENDER_EMAIL_ADDRESS="my_sender_email@gmail.com"
export GMAIL_OAUTH_ACCESS_TOKEN="ya29.a0AfB_byDzLjqCbsdb_RMnguTrB8fmdSEsOSMkvWH6zjcm-1UIi3cdNpfvhZUjYZLVB7NrnNGJIEEatntXjBpc5Bk_cIGKgnjqtesO-HLT0H2Yiz-lZFviz3_UfaaoR8HLjmrKmm7VCkBZvdI0ABb4ADnY9fEKxcLMhR4daCgYKAQcSARASFQGOcNnCvZ0k13Q_KYFObZFjh5umXQ0171"
```

```python
from gmail_python_client import GmailClient

if __name__ == '__main__':
    # Send the email to pswanson@ucdavis.edu
    GmailClient().send_email("pswanson@ucdavis.edu", "Test", "Hello World!")
```

```sh
# Configure with Refresh Token
export GMAIL_SENDER_EMAIL_ADDRESS="my_sender_email@gmail.com"
export GMAIL_OAUTH_REFRESH_TOKEN="1//04mDFqbnpQnGTCgYIARAAGAQSNwF-L9IruAAqiKvHXfHzZnMt6UqTzDOZGg4TJha3oCGa9utu_PwxfrmG-su47Qytt8m2eWDDwZo"
export GMAIL_OAUTH_CLIENT_ID="MyClientID.apps.googleusercontent.com"
export GMAIL_OAUTH_CLIENT_SECRET="GOCYYW-J2krl75t71RhZdZmmB-bSRX52lhJ"
```

```python
from gmail_python_client import GmailClient

if __name__ == '__main__':
    # Send the email to pswanson@ucdavis.edu
    GmailClient().send_email("pswanson@ucdavis.edu", "Test", "Hello World!")
```
