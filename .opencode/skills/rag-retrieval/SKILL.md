---
name: rag-retrieval
description: Use when working on RAG retrieval, FAISS indexes, embeddings, chunking, context ranking, or files named vector_functions.py and persist/chat_*.
---

# RAG Retrieval

Use this skill for changes to retrieval quality, embedding generation, chunking, FAISS persistence, or answer context selection in DocVision AI.

## Project Context

- Retrieval code lives in `vector_functions.py`.
- Per-chat vector data is stored under `persist/chat_<id>/` as `faiss_index.bin` and `chunks.pkl`.
- The embedding model is `sentence-transformers/all-MiniLM-L6-v2` loaded lazily by `load_embedding_model()`.
- `retrieve_chat(chat_id, query, top_k=8)` returns raw text chunks used by `app.py` to build the Gemini prompt.

## Working Rules

- Keep FAISS index vectors and saved chunks in the same order.
- When changing chunking, consider both newly indexed sources and existing persisted indexes.
- Do not silently delete or rebuild persisted chat indexes unless the user asks or the code path is already an explicit rebuild.
- Preserve `float32` vectors for FAISS compatibility.
- Prefer small, measurable retrieval changes before adding new dependencies.

## Verification

- Run or reason through upload/add-source flows that call `add_documents_to_chat()`.
- Check empty-document behavior returns `False` rather than creating invalid indexes.
- Check no-index behavior returns an empty context list.
