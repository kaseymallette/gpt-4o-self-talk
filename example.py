from dotenv import load_dotenv
from openai import OpenAI

# Load env vars from .env file, so that OpenAI() can find OPENAI_API_KEY
load_dotenv() 

# Create an OpenAI client
client = OpenAI() 

# Create a response with the gpt-4o model, and print the output text
response = client.responses.create(
    model="gpt-4o",
    input="Write a one-sentence bedtime story about a unicorn."
)

# Print the output text
print(response.output_text)