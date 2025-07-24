import vertexai
from vertexai.preview.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
from config import GEMINI_API_KEY, PROJECT_ID


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

        # Initialize Vertex AI
        vertexai.init(project=PROJECT_ID, location="us-central1")

        # Load the model
        model = GenerativeModel("veo-3.0-fast-generate-preview")

        # Generate video
        response = model.generate_content(
            [prompt],
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.4,
                "top_p": 1,
                "top_k": 32
            },
            safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False,
        )

        # Save the video to a file
        with open(output_file, "wb") as f:
            f.write(response.content)

        print("Video generation complete!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_video_from_prompt()
