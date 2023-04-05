import os
# from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Set up OAuth2 credentials
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube.force-ssl'])
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube.force-ssl']
        )
        # ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube.force-ssl']
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Create a YouTube API client
# youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
youtube = build('youtube', 'v3', credentials=creds)

# Use the client to retrieve video details
# video_id = 'USRokXSLT0s'
# video_response = youtube.videos().list(
#     part='snippet',
#     id=video_id
# ).execute()

# # Print the video title
# video_title = video_response['items'][0]['snippet']['title']
# print(f'Title: {video_title}')

# Use the client to retrieve the watch later playlist ID
playlists_response = youtube.playlists().list(
    part='snippet',
    mine=True,
    maxResults=50
).execute()
print(f'playlists_response: {playlists_response}')
watch_later_id = None
for playlist in playlists_response['items']:
    if playlist['snippet']['title'] == 'Watch later':
        watch_later_id = playlist['id']
        break

print(f'Watch later id: {watch_later_id}')

# Use the client to retrieve the videos in the watch later playlist
videos = []
next_page_token = None
while True:
    playlist_items_response = youtube.playlistItems().list(
        part='snippet',
        playlistId=watch_later_id,
        maxResults=50,
        pageToken=next_page_token
    ).execute()
    videos.extend(playlist_items_response['items'])
    next_page_token = playlist_items_response.get('nextPageToken')
    if not next_page_token:
        break

# Print the video titles
for video in videos:
    title = video['snippet']['title']
    print(title)
