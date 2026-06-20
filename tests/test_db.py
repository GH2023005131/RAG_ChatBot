import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def test_import_db():
    from db import connect_db, create_chat, list_chats, read_chat

    assert callable(connect_db)
    assert callable(create_chat)
    assert callable(list_chats)
    assert callable(read_chat)
