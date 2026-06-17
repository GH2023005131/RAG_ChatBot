---
name: gemini-prompting
description: Use when working on Gemini API calls, GOOGLE_API_KEY, answer generation, prompt construction, context grounding, or conversation history in app.py.
---

# Gemini Prompting

Use this skill for LLM integration and answer-generation changes in DocVision AI.

## Project Context

- Gemini is initialized in `app.py` with `google.genai.Client(api_key=API_KEY)`.
- The API key comes from `.env` as `GOOGLE_API_KEY`.
- `generate_answer()` retrieves context, builds a prompt, calls `gemini-2.5-flash`, and stores chat messages through the UI flow.
- `build_prompt()` instructs the model to answer only from provided context.
- `build_conversation_history()` includes prior user and assistant messages.

## Working Rules

- Keep answers grounded in retrieved context; do not weaken the context-only instruction without a product reason.
- Do not log, print, or commit API keys or `.env` contents.
- Handle empty context before calling Gemini.
- Keep model response parsing robust for both `response.text` and candidate parts.
- Be careful when adding conversation history so stale messages do not override retrieved source context.

## Verification

- Check missing `GOOGLE_API_KEY` stops the app with a user-facing error.
- Check no-context questions return the existing no-context message.
- Check Gemini exceptions are caught and returned as user-facing errors.
