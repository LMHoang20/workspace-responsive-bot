from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import json
import os
import base64

from app.utility import SingletonMeta
from app.config import *

def cipher_from_passphrase(passphrase: str):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(passphrase.encode())
    key = base64.urlsafe_b64encode(digest.finalize())
    return Fernet(key)

class CredentialStore(metaclass=SingletonMeta):
    def __init__(self):
        self.service_account = None
        self.client_secrets = None

    def get_service_account(self):
        if not self.service_account:
            self.service_account = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=SCOPES,
            )
        return self.service_account

    def get_client_secrets(self):
        if not self.client_secrets:
            self.client_secrets = user_authenticate()
        return self.client_secrets
    
    def get_project_id(self):
        return self.get_service_account().project_id

# Function to store tokens in a JSON file
def store_tokens(credentials):
    with open(TOKEN_FILE, 'w') as token_file:
        PASSPHRASE = os.getenv('PASSPHRASE')
        if PASSPHRASE is not None and PASSPHRASE != "":
            cipher = cipher_from_passphrase(PASSPHRASE)
            encrypted = cipher.encrypt(credentials.encode())
            token_file.write(encrypted.decode())
        else:
            token_file.write(credentials)

# Function to load tokens from the JSON file
def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, 'r') as token_file:
            PASSPHRASE = os.getenv('PASSPHRASE')
            data = token_file.read()
            if PASSPHRASE is not None and PASSPHRASE != "":
                cipher = cipher_from_passphrase(PASSPHRASE)
                plain_text = cipher.decrypt(data.encode()).decode()
                return json.loads(plain_text)
            else:
                return json.loads(data)
    except Exception as e:
        # delete the file if it is corrupted
        print("Deleting corrupted token file:", e)
        os.remove(TOKEN_FILE)
        return None

# Function to create OAuth2 flow and authenticate the user
def user_authenticate():
    credentials = None

    # Load existing tokens if they exist
    token = load_tokens()
    if token and token.get('scopes') == SCOPES:
        credentials = Credentials.from_authorized_user_info(
            token, 
            scopes=SCOPES,
        )

        # If the token is expired, refresh it
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            store_tokens(credentials.to_json())

    # If no valid credentials, initiate the OAuth2 flow
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())  # Refresh if expired
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)  # Open browser to authorize

        # Store the credentials in the file
        store_tokens(credentials.to_json())

    return credentials

