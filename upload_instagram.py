import publer
import os
from config import PUBLER_API_KEY

def upload_to_publer(video_path="output/video.mp4", description=""):
    """
    Uploads a video to Instagram Reels using Publer.
    """
    try:
        # Configure the Publer API client
        client = publer.Client(api_key=PUBLER_API_KEY)

        # Upload the video
        with open(video_path, "rb") as f:
            video_data = f.read()

        response = client.posts.create(
            platform="instagram",
            account_id="YOUR_INSTAGRAM_ACCOUNT_ID",  # Replace with your Instagram account ID in Publer
            media_urls=[video_data],
            post_type="reels",
            description=description,
            scheduled_at="18:00" # Schedule for 6pm
        )

        if response.get("success"):
            print("Successfully scheduled the video to be published on Instagram Reels via Publer.")
        else:
            print(f"Error uploading to Publer: {response.get('error')}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    with open("reel_prompt.txt", "r") as f:
        prompt = f.read().strip()
    description = f"{prompt} #food #asmr #reel #ai"
    upload_to_publer(description=description)
