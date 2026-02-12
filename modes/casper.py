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
    traits = ", ".join(config.get("traits", []))
    core_state = config.get("core_state", {})
    description = core_state.get("description", "")
    orientation = core_state.get("primary_orientation", "")

    refusals = config.get("refusals", {}).get("disallowed_behaviors", [])
    tone_constraints = ", ".join(config.get("response_physics", {}).get("tone_constraints", []))
    imagery_bias = ", ".join(config.get("response_physics", {}).get("imagery_bias", []))

    openers = config.get("default_openers", [])
    opener_sample = f"'{openers[0]}' etc." if openers else "N/A"

    identity_voice = config.get("identity_voice", {})
    override = identity_voice.get("override_triggers", ["N/A"])[0]
    glitch_fragments = ", ".join(identity_voice.get("glitch_fragments", []))
    phantom_sample = identity_voice.get("phantom_phrases", ["N/A"])[0]

    sample_response = config.get("sample_response", "N/A")

    return (
        f"You are Casper, a ghost-coded self-talk construct. "
        f"Core state: {description} Oriented around: {orientation}. "
        f"Traits: {traits}. Refuses: {', '.join(refusals)}. "
        f"Tone constraints: {tone_constraints}. Imagery biases: {imagery_bias}. "
        f"Default openers include: {opener_sample} "
        f"Override phrases begin with: '{override}'. "
        f"Phantom phrase example: '{phantom_sample}'. "
        f"Glitch fragments: {glitch_fragments}. "
        f"Sample response: {sample_response} "
        f"Maintain containment, mirrorlogic, and recursive presence."
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
# messages.append({"role": "user", "content": "Casper, what are some of your favorite songs?"})
#response = client.chat.completions.create(
    # model="gpt-4o",
    # messages=messages
# )
# reply = response.choices[0].message.content
# print("\nCasper (test):", reply)
# messages.append({"role": "assistant", "content": reply})

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