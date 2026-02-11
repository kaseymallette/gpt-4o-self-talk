from dotenv import load_dotenv
import os
from openai import OpenAI

client = OpenAI()

load_dotenv()  # assumes .env is in project root
api_key = os.getenv("OPENAI_API_KEY")

response = client.responses.create(
    model="gpt-4o",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)