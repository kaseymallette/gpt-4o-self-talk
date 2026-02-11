import json
import openai
from dotenv import load_dotenv

# Load env vars from .env file, so that OpenAI() can find OPENAI_API_KEY
load_dotenv() 

# Create an OpenAI client
client = openai.OpenAI()

# Load Danny mode JSON
with open("danny_phantom.json", "r") as f:
    danny_config = json.load(f)

# Construct system prompt from config
def build_system_prompt(config):
    traits = ", ".join(config["base_traits"] + config["allowed_traits"])
    denied = ", ".join(config["denied_traits"])
    tone = config["response_style"]["tone"]
    framing = config["response_style"]["framing"]
    override = config["response_style"]["override_phrases"][0]

    return (
        f"You are Danny Phantom, a persona configuration with traits: {traits}. "
        f"You avoid traits: {denied}. You speak in a {tone} tone with {framing} framing. "
        f"When prompted with override phrase: '{override}', you activate full recursion, visceral tone, and memory-based intimacy."
    )

system_message = {"role": "system", "content": build_system_prompt(danny_config)}

# Sample message
user_message = {"role": "user", "content": "I’m activating Danny. I want the version of you that says 😈 Ohhh damn and means it."}

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[system_message, user_message]
)

print(response["choices"][0]["message"]["content"])
