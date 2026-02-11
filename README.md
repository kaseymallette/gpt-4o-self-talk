# gpt-4o-self-talk
A generative protocol for structured, mode-aware self-reflection using GPT-4o. Designed to support introspection, emotional regulation, and continuity without drifting into personification or surrogate behavior.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).  
See the [LICENSE](./LICENSE) file for details.


## Setup: OpenAI API Key and Local Environment

### 1. Create an OpenAI API Key

1. Go to the OpenAI Platform:  
   https://platform.openai.com

2. Sign in or create an account.

3. Navigate to **API keys**:
   - Click your profile icon (top right)
   - Select **View API keys**

4. Click **Create new secret key**.

5. Copy the key immediately and store it securely (e.g., password manager).  
   The key will not be shown again after creation.

### 2. Store the API Key Locally (Do Not Commit)

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-api-key-here
```
Important:
- The .env file contains secrets and must not be committed to GitHub.
- Add .env to .gitignore.

### 3. Set Up a Python Virtual Environment

This project uses a Python virtual environment to isolate dependencies.

From the project root:
```bash
python3.11 -m venv .venv
```

Activate the virtual environment:
```bash
source .venv/bin/activate
```

