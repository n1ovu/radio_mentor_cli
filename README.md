# Radio Mentor CLI  
![Python CI](https://github.com/<user>/radio_mentor_cli/actions/workflows/python-ci.yml/badge.svg)


Command‑line tool that delivers concise RF‑diagnostics answers
using OpenAI’s GPT‑4o‑mini model.

• Intent‑first system prompt
• Hard caps on sentence count / tokens
• Low‑temperature for determinism

PyTest suite with mocked completions, sentence limit check, Keyword validation.

Note choice of gpt‑4o‑mini, small max_tokens, and placeholder latency logging.

Advanced Prompt Engineer – Built Radio Mentor CLI
• Authored system prompt that enforces ≤ 3‑sentence RF advice (plain English).
• Designed evaluation harness (pytest + mocked OpenAI) achieving 100 % pass rate across smoke and contract tests.
• Optimised runtime cost by capping max_tokens at 120 and selecting gpt‑4o‑mini tier.
• Resolved import‑path & coverage pitfalls, demonstrating deep Python tooling expertise.

## Running locally
```bash
pip install python-dotenv openai pytest
python main.py
