---
name: streamlit-ui
description: Use when editing Streamlit UI, page layout, chat interactions, sidebar controls, CSS theming, or app.py interface code.
---

# Streamlit UI

Use this skill for DocVision AI interface changes in `app.py`, including chat navigation, upload forms, source lists, prompt inputs, and custom CSS.

## Project Context

- The application entry point is `app.py`.
- The app uses `st.query_params` to track the active `chat_id`.
- Custom styling is defined in the `THEME_CSS` string.
- Chat/session data comes from `db.py`; retrieval and ingestion come from `vector_functions.py`.

## Working Rules

- Preserve existing Streamlit patterns unless there is a clear reason to restructure.
- Keep UI state transitions explicit with `set_chat_query()` and `st.rerun()`.
- Validate user inputs before creating chats, adding URLs, or sending questions.
- Avoid leaking raw exceptions to the UI except where existing behavior already displays a user-facing error.
- Keep desktop and narrow-screen layouts usable when adding columns or custom HTML.

## Verification

- Run `streamlit run app.py` when feasible.
- Check the app starts without `GOOGLE_API_KEY` and shows the configured error.
- Check creating, opening, and deleting chats still updates the URL state correctly.
