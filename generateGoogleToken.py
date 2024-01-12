import pickle
import base64
from google_auth_oauthlib.flow import InstalledAppFlow

# Replace this with the path to your 'credentials.json'
credentials_file = "docker_google_secret.json"

# Scopes for Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def main():
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)

    # Check if the credentials include a refresh token
    if not creds.refresh_token:
        print("No refresh token found. Re-authenticate to obtain a new refresh token.")
        return

    # Serialize the credentials to a base64 string
    serialized_creds = base64.b64encode(pickle.dumps(creds)).decode("utf-8")

    # Print the serialized credentials
    print("Serialized credentials:")
    print(serialized_creds)

if __name__ == "__main__":
    main()
