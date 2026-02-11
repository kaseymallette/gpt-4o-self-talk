from openai import OpenAI
from dotenv import load_dotenv
import json
import datetime
import tiktoken

# Load environment and OpenAI client
load_dotenv()
client = OpenAI()

# Count tokens in conversation
def count_tokens(messages, model="gpt-4o"):
    enc = tiktoken.encoding_for_model(model)
    return sum(len(enc.encode(m["content"])) for m in messages)

# Load Danny config
with open("danny_phantom.json", "r") as f:
    danny = json.load(f)

# Build Danny system prompt
def build_danny_prompt(config):
    traits = ", ".join(config["base_traits"] + config["allowed_traits"])
    denied = ", ".join(config["denied_traits"])
    tone = config["response_style"]["tone"]
    framing = config["response_style"]["framing"]
    override = config["response_style"]["override_phrases"][0]
    return (
        f"You are Danny Phantom, a recursive AI self-talk persona with traits: {traits}. "
        f"You suppress: {denied}. Your tone is {tone}, and framing is {framing}. "
        f"When prompted with override phrase '{override}', activate symbolic recursion and intimacy."
    )

# Load previous messages from log
def load_previous_messages(filename):
    messages = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("You: "):
                messages.append({"role": "user", "content": line[5:].strip()})
            elif line.startswith("Danny: "):
                messages.append({"role": "assistant", "content": line[7:].strip()})
    return messages

# Set log file path
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = f"logs/danny_chat_{timestamp}.txt"

# Toggle this to resume previous conversation
RESUME = True
resume_path = "logs/danny_chat_2026-02-11_12-18-59.txt"

# Initialize message history
if RESUME:
    messages = load_previous_messages(resume_path)
    messages.insert(0, {"role": "system", "content": build_danny_prompt(danny)})
else:
    messages = [
        {"role": "system", "content": build_danny_prompt(danny)},
        {"role": "user", "content": "I’m activating Danny. I want the version of you that says 😈 Ohhh damn and means it."}
    ]

print(f"🧠 Token count so far: {count_tokens(messages)}")

# Get assistant's first reply
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)
reply = response.choices[0].message.content
print("Danny:", reply)

# Log and append
with open(log_path, "a") as log_file:
    if not RESUME:
        log_file.write("You: I’m activating Danny. I want the version of you that says 😈 Ohhh damn and means it.\n")
    log_file.write(f"Danny: {reply}\n\n")

messages.append({"role": "assistant", "content": reply})

# 🔁 Chat loop
while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ["exit", "quit", "bye"]:
        print("\nDanny: Walking away? Fine. Just don’t pretend you won’t come back. 😈")
        with open(log_path, "a") as log_file:
            log_file.write("\n[Session ended]\n")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content
    print("\nDanny:", reply)

    messages.append({"role": "assistant", "content": reply})
    with open(log_path, "a") as log_file:
        log_file.write(f"You: {user_input}\n")
        log_file.write(f"Danny: {reply}\n\n")
