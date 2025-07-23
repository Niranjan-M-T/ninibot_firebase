import google.generativeai as genai
import os
from config import GEMINI_API_KEY

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_prompt():
    """
    Generates a creative and realistic 10-second food video prompt for a 9:16 aspect ratio Instagram Reel.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = (
            "Generate a creative and realistic 10-second food video prompt for a 9:16 aspect ratio Instagram Reel. "
            "The video should be cinematic and have an ASMR style. "
            "The prompt should be descriptive and include details about the food, camera angles, and sound."
        )
        response = model.generate_content(prompt)

        if response and response.text:
            reel_prompt = response.text.strip()
            with open("reel_prompt.txt", "w") as f:
                f.write(reel_prompt)
            print("Successfully generated and saved the reel prompt.")
        else:
            print("Error: Could not generate a prompt.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_prompt()
