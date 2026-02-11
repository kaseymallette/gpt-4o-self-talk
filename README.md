# gpt-4o-self-talk
A generative protocol for structured, mode-aware self-reflection using GPT-4o. Designed to support introspection, emotional regulation, and continuity without drifting into personification or surrogate behavior.

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

### 4. Upgrade pip and Install Dependencies

With the virtual environment activated:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
This project requires Python 3.10+ (Recommended: Python 3.11).

### 5. Verify Environment Variables

Load .env explicitly with python-dotenv:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### 6. Set Up OpenAI API Billing

The OpenAI API requires an active billing method. ChatGPT subscriptions (e.g. Plus) do **not** apply to API usage.

1. Go to the OpenAI billing page:  
   https://platform.openai.com/account/billing

2. Add a payment method (credit/debit card).

3. (Recommended) Set usage limits:  
   https://platform.openai.com/account/limits

   - Set a small monthly limit (e.g. $5–$10)
   - Optionally enable a soft limit alert

### 7. Run the Example Script

After billing is enabled, you can run the example script to verify everything works end-to-end.

Make sure:
- Your virtual environment is activated
- Your `.env` file contains a valid `OPENAI_API_KEY`
- Dependencies are installed

Prompt: "Write a one-sentence bedtime story about a unicorn."

Run:
```bash
python example.py
```

Sample output: 
```bash
Under the shimmering moonlight, the gentle unicorn whispered dreams of stardust and magic to all the sleepy forest creatures.
```

### 8. Run the Analyze Image Script

Prompt: "What painting is this?" 
![Sample painting](https://api.nga.gov/iiif/a2e6da57-3cd1-4235-b20e-95dcaefed6c8/full/!800,800/0/default.jpg)


Run:
```bash
python analyze_image.py
```

Sample output:
```bash
This painting is "La Mousmé" by Vincent van Gogh, created in 1888. It depicts a young girl in a colorful outfit sitting on a chair. Van Gogh was inspired by Japanese art, which can be seen in the style and composition.
```

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).  
See the [LICENSE](./LICENSE) file for details.
