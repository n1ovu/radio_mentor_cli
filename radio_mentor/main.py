# main.py – robust .env handling for OpenAI 1.x
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# 1️⃣  Always try to locate a .env anywhere upwards from CWD
load_dotenv(find_dotenv(), override=False)

# 2️⃣  If that fails, explicitly look next to this file (works even when cwd differs)
fallback_env = Path(__file__).with_name(".env")
if fallback_env.exists():
    load_dotenv(fallback_env, override=False)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is still missing.\n"
        "• Verify the .env file is present and formatted as OPENAI_API_KEY=sk-...\n"
        "• Or export the variable in your shell before running the script."
    )

client = OpenAI(api_key=api_key)

def chat_with_radio_mentor(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are Radio Mentor …"},
        {"role": "user", "content": prompt},
    ]
    resp = client.chat.completions.create(
        model="gpt-4.1-nano",  # or whichever model you want
        messages=messages,
        temperature=0.5,
    )
    return resp.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user = input("You: ")
        if user.lower() in {"exit", "quit"}:
            break
        print("Radio Mentor:", chat_with_radio_mentor(user))
