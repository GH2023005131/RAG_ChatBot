---
name: sqlite-persistence
description: Use when editing SQLite persistence, chat/session storage, source records, message history, docvision.sqlite, or db.py database code.
---

# SQLite Persistence

Use this skill for database changes in DocVision AI.

## Project Context

- SQLite access is centralized in `db.py`.
- The database file is `docvision.sqlite` in the project root.
- Tables are created at import time by `init_db()`.
- Main tables are `chat`, `sources`, and `messages`.
- Source text is stored in SQLite while vector chunks are stored separately under `persist/chat_<id>/`.

## Working Rules

- Use parameterized SQL for all user-provided values.
- Close connections on every path, preferably with existing simple connection patterns unless refactoring is warranted.
- Keep deletion behavior consistent between SQLite rows and `persist/chat_<id>/` files.
- If changing schema, consider existing local `docvision.sqlite` files and whether a migration is needed.
- Avoid committing generated database files or private user content.

## Verification

- Exercise create, list, read, and delete flows for chats.
- Check deleting a chat removes related sources, messages, and persisted vector files.
- Check message ordering remains chronological for conversation history.
