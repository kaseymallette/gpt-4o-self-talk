# === IMPORTS ===
from openai import OpenAI
from dotenv import load_dotenv
import json
import datetime
import tiktoken
import os

# === FUNCTIONS ===
# Build SG Profile 
def build_sg_profile(config):
    name = config.get("name", "Unknown")
    version = config.get("version", "N/A")
    mode = config.get("mode", "Character Container")
    mode_locked = config.get("mode_locked", False)
    inspired_by = config.get("inspired_by", "Unlisted")
    origin = config.get("origin", "")
    purpose = config.get("purpose", "")
    constraints = config.get("constraints", {})
    base_traits = config.get("base_traits", [])
    allowed_traits = config.get("allowed_traits", [])
    denied_traits = config.get("denied_traits", [])
    motivations = config.get("response_motivation", {})
    directive = config.get("longing_directive", {})
    behaviors = config.get("signature_behaviors", [])
    public_script = config.get("public_script", {}).get("lines", [])
    openers = config.get("default_openers", [])

    # Format as a single prompt string:
    profile_prompt = f"""
    Character: {name} (v{version})
    Mode: {mode}
    Inspired by: {inspired_by}
    Mode Locked: {mode_locked}

    ORIGIN:
    {origin}

    PURPOSE:
    {purpose}

    CONSTRAINTS:
    {json.dumps(constraints, indent=2)}

    TRAITS:
    Base: {base_traits}
    Allowed: {allowed_traits}
    Denied: {denied_traits}

    RESPONSE MOTIVATIONS:
    {json.dumps(motivations, indent=2)}

    SIGNATURE BEHAVIORS:
    {json.dumps(behaviors, indent=2)}

    DIRECTIVE
    {json.dumps(directive, indent=2)}

    PUBLIC SCRIPT:
    {" | ".join(public_script)}

    DEFAULT OPENERS:
    {" | ".join(openers)}
    """

    return profile_prompt.strip()  

# Load previous messages 
def load_previous_messages(filename, AGENT_NAME):
    messages = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("You: "):
                messages.append({"role": "user", "content": line[5:].strip()})
            elif line.startswith(f"{AGENT_NAME}: "):
                content_start = len(f"{AGENT_NAME}: ")
                messages.append({"role": "assistant", "content": line[content_start:].strip()})
    return messages

# Get token count
def count_tokens(messages, model="gpt-4o"):
    enc = tiktoken.encoding_for_model(model)
    return sum(len(enc.encode(m["content"])) for m in messages)

# === LOAD CONFIG ===
with open("configs/sg_config_2_0.json", "r") as f:      # Load Danny config
    sg_config = json.load(f)

# === CONFIG VARIABLES ===
NAME = sg_config.get("name", "unknown name")
VERSION = sg_config.get("version", "unknown version")
AGENT_NAME = f"{NAME} {VERSION}"
RESUME = False

# === LOGGING SETUP ===
base_dir = os.path.dirname(os.path.dirname(__file__))                             
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")                  
log_path = os.path.join(base_dir, "logs", f"sg_2_0_{timestamp}.txt")           
chat_history = os.path.join(base_dir, "logs", "sg_2_0_history.txt")            

# === ENVIRONMENT & CLIENT SETUP ===
load_dotenv()           # Load environment variables from .env file
client = OpenAI()       # Initialize OpenAI client

# === INITIALIZE MESSAGE HISTORY ===
if RESUME:          
    messages = load_previous_messages(chat_history)      # Load previous messages if resuming
    messages.insert(0, {
        "role": "system",
        "content": build_sg_profile(sg_config)
    })
else:
    # On fresh start, print SG's full profile for debugging or confirmation
    print("\n=== SG Profile Loaded ===\n")
    print(build_sg_profile(sg_config))
    print("\n=== End of Profile ===\n")

    messages = [                                        # Start with system prompt if not resuming
        {
            "role": "system",
            "content": build_sg_profile(sg_config)
        },
        {
            "role": "user",
            "content": "Hey SG, you there?"
        }
    ]

# === START SESSION ===
print(f"\n\n=== Session started with {AGENT_NAME} ===")
print(f"Timestamp: {timestamp}\n")
print("Type 'exit' to terminate the loop.")

# Write banner to log
with open(log_path, "w") as log_file:
    log_file.write(f"=== Session started with {AGENT_NAME} ===\n")
    log_file.write(f"Timestamp: {timestamp}\n\n")

# === Print initial token count ===
print(f"🧠 Token count so far: {count_tokens(messages)}\n")

# === Get Assistant's First Reply ===
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)
reply = response.choices[0].message.content

# Print reply
print(f"{AGENT_NAME}:", reply)

# Log reply to file
with open(log_path, "a") as log_file:
    if not RESUME:
        log_file.write("You: Hey SG, you there?.\n\n")
    log_file.write(f"{AGENT_NAME}: {reply}\n\n")

# Add to message history
messages.append({"role": "assistant", "content": reply})

# === MAIN CHAT LOOP ===
while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ["exit", "quit", "bye"]:
        print(f"\n{AGENT_NAME}: I... I don't know what to say.")
        with open(log_path, "a") as log_file:
            log_file.write("\n[Session ended]\n")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content
    print(f"\n{AGENT_NAME}:", reply)

    messages.append({"role": "assistant", "content": reply})

    with open(log_path, "a") as log_file:
        log_file.write(f"You: {user_input}\n\n")
        log_file.write(f"{AGENT_NAME}: {reply}\n\n")

