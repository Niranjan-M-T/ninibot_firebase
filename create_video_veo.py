import os
from config import VEO_API_KEY
from google.cloud import videointelligence_v1p3beta1 as videointelligence

def create_video_from_prompt(prompt_file="reel_prompt.txt", output_file="output/video.mp4"):
    """
    Generates a video from a prompt using the Veo API.
    """
    try:
        # Read the prompt from the file
        with open(prompt_file, "r") as f:
            prompt = f.read().strip()

        if not prompt:
            print("Error: Prompt file is empty.")
            return

        # Configure the Veo API client
        client = videointelligence.VideoIntelligenceServiceClient.from_service_account_json(VEO_API_KEY)

        # Construct the request
        request = videointelligence.AnnotateVideoRequest(
            features=[videointelligence.Feature.TEXT_DETECTION],
            input_content=prompt.encode("utf-8"),
        )

        # Make the API call
        print("Generating video... This may take a few minutes.")
        operation = client.annotate_video(request=request)
        result = operation.result(timeout=300)

        # Save the video
        with open(output_file, "wb") as f:
            f.write(result.annotation_results[0].text_annotations[0].text.encode("utf-8"))

        print(f"Successfully generated and saved the video to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_video_from_prompt()
