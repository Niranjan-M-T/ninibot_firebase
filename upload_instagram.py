import requests
import os
from config import INSTAGRAM_USER_ID, INSTAGRAM_ACCESS_TOKEN, CDN_HOSTING_LINK

def upload_to_instagram(video_path="output/video.mp4", description=""):
    """
    Uploads a video to Instagram Reels.
    """
    try:
        # Step 1: Create a media container
        create_container_url = f"https://graph.facebook.com/v13.0/{INSTAGRAM_USER_ID}/media"
        create_container_payload = {
            "media_type": "REELS",
            "video_url": f"{CDN_HOSTING_LINK}/{os.path.basename(video_path)}",
            "caption": description,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
        create_container_response = requests.post(create_container_url, data=create_container_payload)
        creation_id = create_container_response.json()["id"]

        # Step 2: Publish the media container
        publish_container_url = f"https://graph.facebook.com/v13.0/{INSTAGRAM_USER_ID}/media_publish"
        publish_container_payload = {
            "creation_id": creation_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
        publish_container_response = requests.post(publish_container_url, data=publish_container_payload)

        if publish_container_response.status_code == 200:
            print("Successfully uploaded the video to Instagram Reels.")
        else:
            print(f"Error uploading to Instagram: {publish_container_response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    with open("reel_prompt.txt", "r") as f:
        prompt = f.read().strip()
    description = f"{prompt} #food #asmr #reel #ai"
    upload_to_instagram(description=description)
