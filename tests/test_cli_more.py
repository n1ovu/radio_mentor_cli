"""
Extra scenarios for Radio Mentor CLI.

Put this file next to test_cli.py →  tests/test_cli_more.py
"""

import re
from unittest.mock import patch
from radio_mentor.main import chat_with_radio_mentor


# ---------- Re‑usable stub --------------------------------------
def _stub_response(text: str):
    """Return a fake OpenAI response object with custom text."""
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


# ---------- 1. Sentence‑count check -----------------------------
@patch(
    "main.client.chat.completions.create",
    side_effect=lambda *_, **__: _stub_response(
        "Good match on your coax. SWR looks 1.2:1. All set."
    ),
)
def test_reply_max_three_sentences(_):
    """Model must stay within ≤ 3 sentences (per system prompt)."""
    out = main.chat_with_radio_mentor("Check my SWR")
    # in tests/test_cli_more.py
    sentences = [s for s in re.split(r"[.!?](?:\s+|$)", out) if s.strip()]
    assert len(sentences) <= 3


# ---------- 2. Trimmed output check -----------------------------
@patch(
    "main.client.chat.completions.create",
    side_effect=lambda *_, **__: _stub_response("  Trim me  "),
)
def test_reply_is_stripped(_):
    out = main.chat_with_radio_mentor("Ping")
    assert out == "Trim me", "chat_with_radio_mentor() should strip whitespace"


# ---------- 3. Keyword presence check ---------------------------
@patch(
    "main.client.chat.completions.create",
    side_effect=lambda *_, **__: _stub_response("SWR reading is nominal."),
)
def test_reply_mentions_swr(_):
    out = main.chat_with_radio_mentor("What is SWR?")
    assert re.search(r"\bSWR\b", out, re.I)
