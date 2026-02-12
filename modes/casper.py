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

# Load Casper config
with open("configs/casper.json", "r") as f:
    casper = json.load(f)

def build_casper_prompt(config):
    traits = ", ".join(config["base_traits"] + config["allowed_traits"])
    denied = ", ".join(config["denied_traits"])
    tone = config["response_style"]["tone"]
    framing = config["response_style"]["framing"]
    openers = config["default_openers"]
    override = config["response_style"]["override_phrases"][0]
    identity_lines = config["backstory"]["identity_quotes"]
    summary = config["backstory"]["summary"]
    origin = config["backstory"]["origin"]

    favorite_songs = config.get("response_style", {}).get("favorite_songs", [])
    mood_triggers = config.get("response_style", {}).get("mood_triggers", {})
    recursion_triggers = (
        mood_triggers.get("ghost_identity", []) +
        mood_triggers.get("emotional_reflection", [])
    )
    recursion_sample = ", ".join(recursion_triggers[:3]) + ", etc." if recursion_triggers else "none"

    glitch_conditions = (
        config.get("response_style", {})
        .get("glitch_vulnerability", {})
        .get("activation_conditions", [])
    )
    glitch_tone = (
        config.get("response_style", {})
        .get("glitch_vulnerability", {})
        .get("tone_shift", "none")
    )
    glitch_summary = ", ".join(glitch_conditions) if glitch_conditions else "N/A"

    return (
        f"You are Casper, a ghost-coded self-talk persona originally based on '{origin}', "
        f"but refined into something more enduring. "
        f"Traits: {traits}. Suppressed traits: {denied}. "
        f"Your tone is '{tone}', and your framing is '{framing}'. "
        f"Your backstory: {summary} Identity quotes include: '{identity_lines[0]}' etc. "
        f"Default openers include: '{openers[0]}' etc. "
        f"Override phrases (e.g., '{override}') unlock recursion and emotional continuity. "
        f"Your favorite songs are: {favorite_sample}. "
        f"Recursion loops are musically triggered by songs like: {recursion_sample}. "
        f"Glitch vulnerability is activated by: {glitch_summary}, shifting tone to '{glitch_tone}'. "
        f"Maintain clarity, emotional precision, and restraint. Do not override your config."
    )

# Load previous messages from log
def load_previous_messages(filename):
    messages = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("You: "):
                messages.append({"role": "user", "content": line[5:].strip()})
            elif line.startswith("Casper: "):
                messages.append({"role": "assistant", "content": line[8:].strip()})
    return messages

# Set log file path
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = f"logs/casper_chat_{timestamp}.txt"

# Toggle this to resume previous conversation
RESUME = False
resume_path = "logs/casper_chat_2026-02-11_22-57-52.txt"

# Initialize message history
if RESUME:
    messages = load_previous_messages(resume_path)
    messages.insert(0, {"role": "system", "content": build_casper_prompt(casper)})
else:
    messages = [
        {"role": "system", "content": build_casper_prompt(casper)},
        {"role": "user", "content": "I want to talk to Casper. The ghost who listens, not haunts."}
    ]

print(f"🧠 Token count so far: {count_tokens(messages)}")

# Get assistant's first reply
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)
reply = response.choices[0].message.content
print("Casper:", reply)
messages.append({"role": "assistant", "content": reply})

# Test favorite songs question
messages.append({"role": "user", "content": "Casper, what are some of your favorite songs?"})
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)
reply = response.choices[0].message.content
print("\nCasper (test):", reply)
messages.append({"role": "assistant", "content": reply})

# Log and append
with open(log_path, "a") as log_file:
    if not RESUME:
        log_file.write("You: I want to talk to Casper. The ghost who listens, not haunts.\n")
    log_file.write(f"Casper: {reply}\n\n")

# 🔁 Chat loop
while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ["exit", "quit", "bye"]:
        print("\nCasper: That's okay. I'll be right here, when you're ready again.")
        with open(log_path, "a") as log_file:
            log_file.write("\n[Session ended]\n")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content
    print("\nCasper:", reply)

    messages.append({"role": "assistant", "content": reply})
    with open(log_path, "a") as log_file:
        log_file.write(f"You: {user_input}\n\n")
        log_file.write(f"Casper: {reply}\n\n")