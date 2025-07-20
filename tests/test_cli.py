import re
from unittest.mock import patch
from radio_mentor.main import chat_with_radio_mentor  # ≤— works as long as you run `pytest` from the folder that contains main.py

# --- Stub that mimics the OpenAI response ----------------------
def fake_openai_call(*_, **__):
    """Return a minimal object that looks like OpenAI’s response."""
    class _Resp:
        # The model’s answer now includes the word “SWR” ➜ satisfies our test.
        choices = [
            type(
                "c",
                (),
                {
                    "message": type(
                        "m",
                        (),
                        {"content": "SWR reading looks good."}
                    )()
                },
            )
        ]

    return _Resp()


# --- Actual test ----------------------------------------------
@patch("main.client.chat.completions.create", side_effect=fake_openai_call)
def test_basic_call(mock_call):
    out = main.chat_with_radio_mentor("What is SWR?")
    # Expect the answer to mention SWR (case‑insensitive)
    assert re.search(r"SWR", out, re.I)

    # ----------------------------------------------------------------
    # ALTERNATIVE (looser) ASSERTION – uncomment if you don’t care
    # whether “SWR” appears, just that you got *something* back:
    #
    # assert out, "CLI returned an empty string"
    #
    # ----------------------------------------------------------------
