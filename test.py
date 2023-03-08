import os
from googleapiclient.discovery import build

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

# Use the client to retrieve video details
video_id = 'VIDEO_ID'
video_response = youtube.videos().list(
    part='snippet',
    id=video_id
).execute()

# Print the video title
video_title = video_response['items'][0]['snippet']['title']
print(f'Title: {video_title}')
