import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_and_get_access_token():
    # Path to your JSON credentials file

    credentials_path = os.path.abspath('C:\\Users\\Admin\\gdrive')

    # Check if the token file exists, and if it's still valid
    creds = None
    if os.path.exists('token.json'):
        creds = service_account.Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive.file'])

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This opens a new browser window/tab for the user to log in
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, ['https://www.googleapis.com/auth/drive.file'])
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Access token
    access_token = creds.token

    return access_token

# Example usage
if __name__ == '__main__':
    access_token = authenticate_and_get_access_token()
    print('Access Token:', access_token)

