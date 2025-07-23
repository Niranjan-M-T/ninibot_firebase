import requests
import os
import time
from config import PUBLER_API_KEY, PUBLER_WORKSPACE_ID

def upload_media(video_path):
    """
    Uploads a video to Publer and returns the media ID.
    """
    try:
        url = "https://app.publer.com/api/v1/media"
        headers = {
            "Authorization": f"Bearer {PUBLER_API_KEY}",
            "Publer-Workspace-Id": PUBLER_WORKSPACE_ID,
        }
        with open(video_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                return response.json()['data']['id']
            else:
                print(f"Error uploading media to Publer: {response.text}")
                return None
    except Exception as e:
        print(f"An error occurred during media upload: {e}")
        return None

def upload_to_instagram(video_path="output/video.mp4", description=""):
    """
    Uploads a video to Instagram Reels using the Publer API.
    """
    try:
        media_id = upload_media(video_path)
        if not media_id:
            return

        url = "https://app.publer.com/api/v1/posts/schedule/publish"
        headers = {
            "Authorization": f"Bearer {PUBLER_API_KEY}",
            "Publer-Workspace-Id": PUBLER_WORKSPACE_ID,
            "Content-Type": "application/json",
        }
        data = {
            "bulk": {
                "state": "scheduled",
                "posts": [
                    {
                        "networks": {
                            "instagram": {
                                "type": "video",
                                "text": description,
                                "media": [{"id": media_id, "type": "video"}]
                            }
                        },
                        "accounts": [
                            {
                                "id": "72165006158" # Replace with your Instagram account ID in Publer
                            }
                        ]
                    }
                ]
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            job_id = response.json()['data']['job_id']
            print(f"Post creation job initiated with ID: {job_id}")
            # Poll for job status
            while True:
                status_url = f"https://app.publer.com/api/v1/job_status/{job_id}"
                status_response = requests.get(status_url, headers=headers)
                if status_response.status_code == 200:
                    status = status_response.json()['data']['status']
                    if status == 'completed':
                        print("Successfully uploaded the video to Instagram Reels using Publer.")
                        break
                    elif status == 'failed':
                        print(f"Error uploading to Instagram via Publer: {status_response.json()['data']['result']['payload']}")
                        break
                    else:
                        print("Waiting for post to be published...")
                        time.sleep(10)
                else:
                    print(f"Error checking job status: {status_response.text}")
                    break
        else:
            print(f"Error creating post with Publer: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    with open("reel_prompt.txt", "r") as f:
        prompt = f.read().strip()
    description = f"{prompt} #food #asmr #reel #ai"
    upload_to_instagram(description=description)
