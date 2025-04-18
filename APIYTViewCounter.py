from googleapiclient.discovery import build
from google.oauth2 import service_account
import time
import os
service_account_file = #'path/to/your/service_account.json'  # Update this path
print("os.path.exists(service_account_file):", os.path.exists(service_account_file))
with open(service_account_file, 'r') as f:
    print("file readable")

    # secutity check
    if os.path.exists(''): # Check if the file exists
        print("Service account file exists")
try:
    from google.oauth2 import service_account
except ImportError:
    # Fallback for some environments
    from google.auth import service_account

# Set up the YouTube API client
def initialize_youtube_client():
    try:
        service_account_file = 'null'  # Update this path
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
        )
        return build('youtube', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Error initializing YouTube client: {e}")
        return None

# Alternative method using API key (if you don't have service account)
def initialize_youtube_client_with_key():
    API_KEY = "null"  # Your API key
    return build('youtube', 'v3', developerKey=API_KEY)

youtube = initialize_youtube_client() or initialize_youtube_client_with_key()

def update_video_title(video_id, new_title):
    try:
        request = youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": new_title,
                    "categoryId": "22",
                    "description": "Updated description",
                    "tags": ["tag1", "tag2"],
                    "defaultLanguage": "en",
                }
            }
        )
        response = request.execute()
        print(f"Title updated successfully: {new_title}")
        return response
    except Exception as e:
        print(f"Error updating title: {e}")
        return None

def get_views(video_id):
    try:
        request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        response = request.execute()
        return int(response['items'][0]['statistics']['viewCount'])
    except Exception as e:
        print(f"Error getting view count: {e}")
        return 0

# Main loop
def main():
    VIDEO_ID = "your_video_id"  # Replace with your video ID
    last_views = 0
    
    while True:
        try:
            current_views = get_views(VIDEO_ID)
            if current_views > last_views:
                new_title = f"My Video - {current_views} views!"
                update_video_title(VIDEO_ID, new_title)
                last_views = current_views
            time.sleep(60)  # Wait for 1 minute before checking again
        except KeyboardInterrupt:
            print("Script stopped by user")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()