# DriveSpotifyUpdater

1. You need to go here to sign up for access to the Google Drive api: https://console.developers.google.com/apis/dashboard
2. Create a project and then create an OAuth client ID for that project. Download the credentials file and rename it credentials.json
3. Put your Spotify API credentials into the spotify_credentials_sample.json and rename that to spotify_credentials.json
4. Create a virtual environment: virutalenv venv
5. Activate your virtual environment source venv/bin/activate
6. Install required packages: pip install -r requirements.txt
7. Run: python3 DriveSpotifyUpdater.py
