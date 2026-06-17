import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "docvision.sqlite"


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source_text TEXT,
            type TEXT DEFAULT 'document',
            chat_id INTEGER,
            FOREIGN KEY (chat_id) REFERENCES chat(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chat(id)
        )
        """
    )

    conn.commit()
    conn.close()


init_db()


def create_chat(title):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat (title) VALUES (?)", (title,))
    chat_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return chat_id


def list_chats():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat ORDER BY created_at DESC")
    chats = cursor.fetchall()
    conn.close()
    return chats


def read_chat(chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat WHERE id = ?", (chat_id,))
    chat = cursor.fetchone()
    conn.close()
    return chat


def delete_chat(chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat WHERE id = ?", (chat_id,))
    cursor.execute("DELETE FROM sources WHERE chat_id = ?", (chat_id,))
    cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

    persist_path = BASE_DIR / "persist" / f"chat_{chat_id}"
    if persist_path.exists():
        import shutil
        shutil.rmtree(persist_path)


def create_source(name, source_text, chat_id, source_type="document"):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sources (name, source_text, chat_id, type) VALUES (?, ?, ?, ?)",
        (name, source_text, chat_id, source_type),
    )
    source_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return source_id


def list_sources(chat_id, source_type=None):
    conn = connect_db()
    cursor = conn.cursor()
    if source_type:
        cursor.execute(
            "SELECT * FROM sources WHERE chat_id = ? AND type = ? ORDER BY id DESC",
            (chat_id, source_type),
        )
    else:
        cursor.execute("SELECT * FROM sources WHERE chat_id = ? ORDER BY id DESC", (chat_id,))
    sources = cursor.fetchall()
    conn.close()
    return sources


def delete_source(source_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sources WHERE id = ?", (source_id,))
    conn.commit()
    conn.close()


def create_message(chat_id, sender, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (chat_id, sender, content) VALUES (?, ?, ?)",
        (chat_id, sender, content),
    )
    conn.commit()
    conn.close()


def get_messages(chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, content FROM messages WHERE chat_id = ? ORDER BY timestamp ASC",
        (chat_id,),
    )
    messages = cursor.fetchall()
    conn.close()
    return messages
