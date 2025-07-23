import requests
import os
from config import PUBLER_API_KEY

def upload_to_instagram(video_path="output/video.mp4", description=""):
    """
    Uploads a video to Instagram Reels using the Publer API.
    """
    try:
        url = "https://api.publer.io/v1/posts"
        headers = {
            "Authorization": f"Bearer {PUBLER_API_KEY}",
        }
        data = {
            "platform": "instagram",
            "account_id": "YOUR_INSTAGRAM_ACCOUNT_ID",  # Replace with your Instagram account ID in Publer
            "media_urls": [video_path],
            "description": description,
            "post_type": "reel",
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            print("Successfully uploaded the video to Instagram Reels using Publer.")
        else:
            print(f"Error uploading to Instagram via Publer: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    with open("reel_prompt.txt", "r") as f:
        prompt = f.read().strip()
    description = f"{prompt} #food #asmr #reel #ai"
    upload_to_instagram(description=description)
