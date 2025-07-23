import time
import os
import google.generativeai as genai
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

        # Create the model
        model = genai.GenerativeModel('models/veo-3.0-fast-generate-preview')

        # Generate video
        video = model.generate_content(prompt)

        # Save the video to a file
        with open(output_file, "wb") as f:
            f.write(video.content)

        print("Video generation complete!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_video_from_prompt()
