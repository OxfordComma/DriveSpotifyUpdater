from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import spotipy
import spotipy.util as util
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']



def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    # 0B7wQpwvNx4sTUVZKMFFIVFByakE is the Drive id for the 'Guitar' folder
    # pageSize 1000 to get all of the documents
    drive_args = json.load(open('drive_arguments.json'))['arguments']
    query = drive_args['query']
    playlist_uri = drive_args['playlist_uri']

    results = service.files().list(q=query, pageSize=1000, orderBy='modifiedTime desc').execute()
    items = results.get('files', [])

    songs = [i['name'] for i in items]
    filter_out = ['HOLIDAY', 'TEMPLATE', 'Copy']
    songs = list(filter(lambda x: not any(f in x for f in filter_out), songs))
    song_uris = []

    spotify_creds = json.load(open('spotify_credentials.json'))['credentials']
    username = spotify_creds['username']
    client_id = spotify_creds['client_id']
    client_secret = spotify_creds['client_secret']
    redirect_uri = spotify_creds['redirect_uri']
    scope = 'playlist-modify-private'
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False

        current_tracks_in_playlist = [i['track']['uri'] for i in sp.user_playlist_tracks(username, playlist_uri)['items'] if i]

        for song in songs:
            search_result = sp.search(song.replace(' -', '').replace('[DRAFT]', ''))
            if len(search_result['tracks']['items']) == 0:
                print(song + ' not found in Spotify search.')

            else:
                song_uri = search_result['tracks']['items'][0]['uri']
                if song_uri not in current_tracks_in_playlist:
                    song_uris.append(song_uri)
            print(song)

        counter = 0
        while counter < len(song_uris):
            spotify_results = sp.user_playlist_add_tracks(username, playlist_uri, song_uris[counter:counter+100])
            counter += 100
    else:
        print("Can't get token for", username)

    if not songs:
        print('No files found.')
    else:
        print('Songs:')
        for song in songs:
            print(song)

if __name__ == '__main__':
    main()