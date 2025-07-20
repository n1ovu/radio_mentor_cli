# =============================
# Radio Mentor CLI project
# Minimal, single‑folder layout:
#   radio_mentor_cli/
#     main.py
#     tests/
#         test_cli.py
#         test_cli_more.py
# =============================

# ------------ main.py -----------------
"""Radio Mentor – concise RF diagnostics via OpenAI CLI."""

import os
import time
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load .env (search upward first, then next to this file)
load_dotenv(find_dotenv(), override=False)
fallback_env = Path(__file__).with_name(".env")
if fallback_env.exists():
    load_dotenv(fallback_env, override=False)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY missing; put it in a .env file or export it.")

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = (
    "You are Radio Mentor, an RF‑diagnostics expert. "
    "Respond in \u22643 short sentences, plain English, no fluff."
)

def chat_with_radio_mentor(prompt: str) -> str:
    """Send *prompt* to the model and return a terse answer."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    start = time.time()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=120,
    )
    latency = time.time() - start  # noqa: F841  # placeholder for future logging
    return resp.choices[0].message.content.strip()

if __name__ == "__main__":
    print("Radio Mentor CLI (type 'exit' to quit)")
    while True:
        user_in = input("You: ").strip()
        if user_in.lower() in {"exit", "quit"}:
            break
        print("Radio Mentor:", chat_with_radio_mentor(user_in))


# ------------ tests/test_cli.py -----------------
"""Basic smoke test for Radio Mentor CLI."""

import sys, pathlib, re
from unittest.mock import patch

# Make project root importable when tests run from any location
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import main  # noqa: E402 – after path tweak


def fake_openai_call(*_, **__):
    class _Resp:
        choices = [
            type(
                "Choice",
                (),
                {
                    "message": type(
                        "Msg", (), {"content": "SWR reading looks good."}
                    )()
                },
            )
        ]

    return _Resp()


@patch("main.client.chat.completions.create", side_effect=fake_openai_call)
def test_basic_call(mock_call):
    out = main.chat_with_radio_mentor("What is SWR?")
    assert re.search(r"SWR", out, re.I)


# ------------ tests/test_cli_more.py -----------------
"""Additional contract tests for Radio Mentor CLI."""

import sys, pathlib, re
from unittest.mock import patch

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import main  # noqa: E402


# Utility to stub responses --------------------------------------

def _stub_response(text: str):
    return type(
        "Resp",
        (),
        {
            "choices": [
                type(
                    "Choice",
                    (),
                    {"message": type("Msg", (), {"content": text})()},
                )
            ]
        },
    )()


# 1. Sentence‑limit check ---------------------------------------
@patch(
    "main.client.chat.completions.create",
    side_effect=lambda *_, **__: _stub_response(
        "Good match on your coax. SWR looks 1.2:1. All set."
    ),
)
def test_reply_max_three_sentences(_):
    out = main.chat_with_radio_mentor("Check my SWR")
    sentences = [s for s in re.split(r"[.!?](?:\\s+|$)", out) if s.strip()]
    assert len(sentences) <= 3


# 2. Whitespace trimming ----------------------------------------
@patch(
    "main.client.chat.completions.create",
    side_effect=lambda *_, **__: _stub_response("  Trim me  "),
)
def test_reply_is_stripped(_):
    out = main.chat_with_radio_mentor("Ping")
    assert out == "Trim me"


# 3. Keyword sanity check ---------------------------------------
@patch(
    "main.client.chat.completions.create",
    side_effect=lambda *_, **__: _stub_response("SWR reading is nominal."),
)
def test_reply_mentions_swr(_):
    out = main.chat_with_radio_mentor("What is SWR?")
    assert re.search(r"\bSWR\b", out, re.I)
