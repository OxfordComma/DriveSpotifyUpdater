# DriveSpotifyUpdater

- You need to go here to sign up for access to the Google Drive api: https://console.developers.google.com/apis/dashboard
- Create a project and then create an OAuth client ID for that project. Download the credentials file and rename it credentials.json
- Put your Spotify API credentials into the spotify_credentials_sample.json and rename that to spotify_credentials.json
- Rename drive_arguments_sample.json to drive_arguments.json and update the fields inside.
-- Query for me was "'<Drive Folder ID> in parents'" to only search the folder where the one pages are
-- Playlist URI is the playlist to be updated
- Create a virtual environment: virutalenv venv
- Activate your virtual environment source venv/bin/activate
- Install required packages: pip install -r requirements.txt
- Run: python3 DriveSpotifyUpdater.py
