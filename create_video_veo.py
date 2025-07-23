import time
import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

# Configure your API key
genai.configure(api_key=GEMINI_API_KEY)

def create_video_from_prompt(prompt_file="reel_prompt.txt", output_file="output/video.mp4"):
    """
    Generates a video from a prompt using the Veo 3.0 Fast Generate Preview model.
    """
    try:
        # Read the prompt from the file
        with open(prompt_file, "r") as f:
            prompt = f.read().strip()

        if not prompt:
            print("Error: Prompt file is empty.")
            return

        client = genai.Client()

        # Generate video with Veo 3
        operation = client.models.generate_videos(
            model="veo-3.0-fast-generate-preview", # Use the preview model for Veo 3
            prompt=prompt,
            config=types.GenerateVideosConfig(
                negative_prompt="cartoon, drawing, low quality",
            ),
        )

        # Poll the operation status until the video is ready
        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10) # Adjust sleep duration as needed

        operation = client.operations.get(operation)
        generated_video = operation.result.generated_videos[0]

        # Download the generated video file
        video_file = client.files.get(file=generated_video.video)
        with open(output_file, "wb") as f:
            f.write(video_file.read())

        print("Video generation complete!")
        print(f"Generated video details: {generated_video.video}")


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_video_from_prompt()
