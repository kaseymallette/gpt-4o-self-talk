from dotenv import load_dotenv
from openai import OpenAI

# Load env vars from .env file, so that OpenAI() can find OPENAI_API_KEY
load_dotenv()

# Create an OpenAI client
client = OpenAI()

# Create a response with the gpt-4o model to analyze the image
response = client.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Describe this image in 1-2 sentences.",
                },
                {
                    "type": "input_image",
                    "image_url": "https://api.nga.gov/iiif/a2e6da57-3cd1-4235-b20e-95dcaefed6c8/full/!800,800/0/default.jpg"
                }
            ]
        }
    ]
)

# Print the output text
print(response.output_text)