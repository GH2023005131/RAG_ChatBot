import os
from pathlib import Path

import google.genai as genai
import streamlit as st
from dotenv import load_dotenv

from db import (
    create_chat,
    create_message,
    create_source,
    delete_chat,
    delete_source,
    get_messages,
    list_chats,
    list_sources,
    read_chat,
)
from vector_functions import (
    SUPPORTED_EXTENSIONS,
    add_documents_to_chat,
    create_vector_store,
    extract_text,
    extract_text_from_url,
    retrieve_chat,
)

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
POPPLER_PATH = os.getenv("POPPLER_PATH")

st.set_page_config(
    page_title="DocVision AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not API_KEY:
    st.title("📄 DocVision AI")
    st.error("Missing GOOGLE_API_KEY. Create a .env file with GOOGLE_API_KEY=your_api_key")
    st.stop()


def load_language_model():
    return genai.Client(api_key=API_KEY)

MODEL = load_language_model()

THEME_CSS = """
<style>
body {
    background: #08101f;
    color: #e9eef8;
}
section.main {
    padding-top: 1.25rem;
}
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.98) !important;
    color: #f8fafc;
}
.stButton>button {
    border-radius: 14px;
    background: linear-gradient(135deg, #4f46e5, #06b6d4);
    color: white;
    border: none;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.18);
}
.stButton>button:hover {
    background: linear-gradient(135deg, #4338ca, #0891b2);
}
.stTextArea>div>div>textarea,
.stTextInput>div>div>input,
.stSelectbox>div>div>div {
    border-radius: 16px;
    background: #111827;
    color: #f8fafc;
    border: 1px solid rgba(148, 163, 184, 0.2);
}
.reportview-container .main .block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 2rem;
}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


def format_source(source):
    icon = "🌐" if source["type"] == "web" else "📄"
    return f"{icon} {source['name']}"


def get_chat_id_from_query():
    params = st.query_params
    chat_id = params.get("chat_id", [None])[0]
    if chat_id is not None and str(chat_id).isdigit():
        return int(chat_id)
    return None


def set_chat_query(chat_id=None):
    if chat_id is None:
        st.query_params = {}
    else:
        st.query_params = {"chat_id": [str(chat_id)]}


def build_prompt(question, context_chunks):
    context_text = "\n\n".join(context_chunks)
    return f"""
You are a professional AI assistant. Answer directly using only the context provided below.

Context:
{context_text}

Question:
{question}
"""


def build_conversation_history(chat_id):
    messages = get_messages(chat_id)
    history_lines = []
    for message in messages:
        role = "User" if message["sender"] == "user" else "Assistant"
        history_lines.append(f"{role}: {message['content']}")
    return "\n".join(history_lines)


def generate_answer(chat_id, question):
    context_chunks = retrieve_chat(chat_id, question, top_k=8)
    if not context_chunks:
        return "No relevant context found. Upload documents or add web sources.", []

    conversation_history = build_conversation_history(chat_id)
    prompt = build_prompt(question, context_chunks)
    if conversation_history:
        prompt = (
            "You are a professional AI assistant. Use the conversation history and the context below to answer the latest question."
            "\n\nConversation history:\n"
            + conversation_history
            + "\n\n" + prompt
        )

    try:
        response = MODEL.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        answer_text = response.text if getattr(response, "text", None) else ""
        if not answer_text and response.candidates:
            candidate = response.candidates[0]
            if getattr(candidate, "content", None) and getattr(candidate.content, "parts", None):
                answer_text = candidate.content.parts[0].text or ""
        return answer_text.strip(), context_chunks
    except Exception as error:
        return f"Error generating answer: {error}", context_chunks


def rebuild_chat_index(chat_id):
    sources = list_sources(chat_id)
    texts = [source["source_text"] for source in sources if source["source_text"]]
    if texts:
        return create_vector_store(texts, chat_id)
    return False


def build_dashboard():
    st.markdown(
        "<div class='hero-card'><div><h1>📄 DocVision AI</h1>"
        "<p>Build a smart RAG app with persistent chats, document sources, and web page ingestion.</p></div></div>",
        unsafe_allow_html=True,
    )

    with st.container():
        chats = list_chats()
        chat_count = len(chats)
        docs_count = sum(len(list_sources(chat['id'], source_type='document')) for chat in chats)
        web_count = sum(len(list_sources(chat['id'], source_type='web')) for chat in chats)
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        stats_col1.markdown(
            f"<div class='metric-card'><h3>Chats</h3><p>{chat_count}</p></div>",
            unsafe_allow_html=True,
        )
        stats_col2.markdown(
            f"<div class='metric-card'><h3>Documents</h3><p>{docs_count}</p></div>",
            unsafe_allow_html=True,
        )
        stats_col3.markdown(
            f"<div class='metric-card'><h3>Web sources</h3><p>{web_count}</p></div>",
            unsafe_allow_html=True,
        )


def chats_home():
    build_dashboard()

    st.markdown("## Your chat sessions")
    st.markdown("Create a chat and store related PDF, DOCX, text, image, or web sources per session.")

    with st.form("create_chat_form", clear_on_submit=True):
        chat_title = st.text_input("Chat title", placeholder="Enter chat title")
        create_button = st.form_submit_button("Create chat")
        if create_button:
            if chat_title.strip():
                new_chat_id = create_chat(chat_title.strip())
                set_chat_query(new_chat_id)
                st.rerun()
            else:
                st.warning("Please enter a chat title.")

    st.markdown("---")
    chats = list_chats()
    if not chats:
        st.info("No chats created yet. Add a chat to start indexing sources.")
        return

    for chat in chats:
        with st.container():
            cols = st.columns([0.65, 0.15, 0.2])
            cols[0].markdown(f"**{chat['title']}**")
            if cols[1].button("Open", key=f"open_{chat['id']}"):
                set_chat_query(chat['id'])
                st.rerun()
            if cols[2].button("Delete", key=f"delete_{chat['id']}"):
                delete_chat(chat['id'])
                st.success(f"Deleted chat: {chat['title']}")
                st.rerun()


def chat_page(chat_id):
    chat = read_chat(chat_id)
    if chat is None:
        st.error("Chat not found.")
        if st.button("Back to chats"):
            set_chat_query(None)
            st.rerun()
        return

    st.markdown(
        "<div class='hero-card'><div><h1>📄 DocVision AI</h1>"
        f"<p>Chat: {chat['title']} — upload documents, add web sources, and ask smart questions.</p></div></div>",
        unsafe_allow_html=True,
    )
    sources_count = len(list_sources(chat_id))
    st.caption(f"📚 {sources_count} sources indexed")

    with st.sidebar:
        if st.button("Back to chats"):
            set_chat_query(None)
            st.rerun()

        st.markdown(f"## {chat['title']}")
        st.markdown("### Upload documents")
        uploaded_files = st.file_uploader(
            "Drop files here or click to browse",
            type=[ext.strip('.') for ext in sorted(SUPPORTED_EXTENSIONS)],
            accept_multiple_files=True,
            help="Supported: PDF, DOCX, TXT, CSV, MD, PNG, JPG, JPEG, BMP, TIFF",
            key=f"upload_{chat_id}",
        )
        process_docs = st.button("Add documents", key=f"process_docs_{chat_id}")

        st.markdown("---")
        st.markdown("### Add web source")
        link_url = st.text_input(
            "Web page URL",
            value="",
            key=f"link_url_{chat_id}",
            help="Paste a public webpage URL to index its content.",
        )
        add_link = st.button("Add web source", key=f"add_link_{chat_id}")

        st.markdown("---")
        st.markdown("### Sources")
        sources = list_sources(chat_id)
        if sources:
            for source in sources:
                cols = st.columns([0.8, 0.2])
                cols[0].markdown(format_source(source))
                if cols[1].button("❌", key=f"delete_source_{source['id']}"):
                    delete_source(source['id'])
                    remaining = list_sources(chat_id)
                    if remaining:
                        rebuild_chat_index(chat_id)
                    else:
                        index_file = Path("persist") / f"chat_{chat_id}" / "faiss_index.bin"
                        chunks_file = Path("persist") / f"chat_{chat_id}" / "chunks.pkl"
                        if index_file.exists():
                            index_file.unlink()
                        if chunks_file.exists():
                            chunks_file.unlink()
                    st.rerun()
        else:
            st.markdown("No sources added yet.")

        st.markdown("---")
        st.markdown("### Notes")
        st.markdown(
            "- Add documents or web sources to build the RAG index.\n"
            "- Delete source items to rebuild the chat index automatically.\n"
            "- Ask specific questions for better results."
        )

    if process_docs:
        if not uploaded_files:
            st.warning("Upload at least one file to add documents.")
        else:
            with st.spinner("Processing uploaded documents..."):
                added = 0
                failed = []
                for uploaded_file in uploaded_files:
                    text = extract_text(uploaded_file.getvalue(), uploaded_file.name, poppler_path=POPPLER_PATH)
                    if text:
                        create_source(uploaded_file.name, text, chat_id, source_type="document")
                        add_documents_to_chat(chat_id, [text])
                        added += 1
                    else:
                        failed.append(uploaded_file.name)
            if added:
                st.success(f"Added {added} document{'' if added == 1 else 's'}.")
            if failed:
                st.error("Failed to read: " + ", ".join(failed))
            st.rerun()

    if add_link:
        if not link_url.strip():
            st.warning("Enter a webpage URL before adding a source.")
        else:
            with st.spinner("Fetching webpage content..."):
                page_text = extract_text_from_url(link_url.strip())
                if page_text:
                    create_source(link_url.strip(), page_text, chat_id, source_type="web")
                    add_documents_to_chat(chat_id, [page_text])
                    st.success("Web source added successfully.")
                else:
                    st.error("Unable to extract text from the provided URL.")
            st.rerun()
            
    st.markdown("### 💬 Conversation")

    messages = get_messages(chat_id)

    for message in messages:
        role = "user" if message["sender"] == "user" else "assistant"

        with st.chat_message(role):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about your documents...")

    if question:
        create_message(chat_id, "user", question)

        with st.spinner("Generating answer..."):
            answer, _ = generate_answer(chat_id, question)

        if answer.startswith("Error generating answer:"):
            st.error(answer)
        elif answer.strip():
            create_message(chat_id, "ai", answer)

        st.rerun()

def main():
    current_chat_id = get_chat_id_from_query()
    if current_chat_id is None:
        chats_home()
    else:
        chat_page(current_chat_id)


if __name__ == "__main__":
    main()