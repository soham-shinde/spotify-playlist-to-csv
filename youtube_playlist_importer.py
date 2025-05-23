import pandas as pd
import os
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load CSV file
df = pd.read_csv("spotify_playlist_songs.csv")

# Setup OAuth
SCOPES = ["https://www.googleapis.com/auth/youtube"]
flow = InstalledAppFlow.from_client_secrets_file("key3.json", SCOPES)
creds = flow.run_local_server(port=0)

youtube = build("youtube", "v3", credentials=creds)

# Create a playlist
request = youtube.playlists().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Imported Spotify Playlist",
            "description": "Playlist created from Spotify CSV",
        },
        "status": {"privacyStatus": "private"},
    },
)
response = request.execute()
playlist_id = response["id"]
print(f"✅ Created YouTube Playlist: {response['snippet']['title']}")


count = 0
# Search and add each song
for index, row in df.iterrows():
    query = f"{row['Title']} {row['Artist']} official video song"
    if count ==50 : break
    try:
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=1,
            type="video"
        ).execute()

        if search_response["items"]:
            video_id = search_response["items"][0]["id"]["videoId"]
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id,
                        },
                    }
                }
            ).execute()
            print(f"🎵 Added: {query}")
        else:
            print(f"⚠️ Not found: {query}")

        time.sleep(1) 
        count+=1# Respect rate limits
    except HttpError as e:
        print(f"❌ API error for: {query}\n{e}")
        continue

print("✅ All done!")
