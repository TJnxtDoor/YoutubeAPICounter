import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE = 'youtube'
API_VERSION = 'v3'

def authenticate_youtube():
    """Handles the OAuth flow to get permission to access YouTube"""
    print(" Authenticating with YouTube...")
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json', 
            SCOPES
        )
        credentials = flow.run_local_server(port=0)
        return build(API_SERVICE, API_VERSION, credentials=credentials)
    except Exception as e:
        print(f" Authentication failed: {e}")
        return None

def get_video_details(youtube, video_id):
    """Gets the current view count and title of a video"""
    print(f" Getting stats for video {video_id}...")
    try:
        response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()
        
        if not response['items']:
            print(" Video not found - check your video ID")
            return None
            
        video = response['items'][0]
        views = int(video['statistics']['viewCount'])
        title = video['snippet']['title']
        
        print(f" Found video: '{title}' with {views:,} views")
        return {'views': views, 'title': title}
    
    except HttpError as error:
        print(f" YouTube API error: {error}")
        return None

def update_video_title(youtube, video_id, new_title):
    """Updates the video title on YouTube"""
    print(f" Attempting to update title to: '{new_title}'")
    try:
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        video = video_response['items'][0]
        video['snippet']['title'] = new_title
        
        youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': video['snippet']
            }
        ).execute()
        
        print(" Title updated successfully!")
        return True
        
    except HttpError as error:
        print(f" Failed to update title: {error}")
        return False

def format_view_count(views):
    """Formats the view count with commas"""
    if views < 1000:
        return str(views)
    return f"{views:,}"

def main():
    VIDEO_ID = "YOUR_VIDEO_ID_HERE"
    
    youtube = authenticate_youtube()
    if not youtube:
        return
    
    video_info = get_video_details(youtube, VIDEO_ID)
    if not video_info:
        return
    
    views_formatted = format_view_count(video_info['views'])
    new_title = f"{video_info['title']} 👀 {views_formatted} views"
    
    update_video_title(youtube, VIDEO_ID, new_title)

if __name__ == "__main__":
    print(" Starting YouTube View Counter Updater")
    main()
    print(" Done!")
