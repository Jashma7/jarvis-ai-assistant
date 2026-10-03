
"""
Jarvis AI Assistant - Memory Module
Stores and retrieves simple user memories in a JSON file.
"""

import json
from datetime import datetime
from config import MEMORY_FILE


def load_memories():
    """Load saved memories from the JSON file."""
    if not MEMORY_FILE.exists():
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load memories: {error}")
        return {}


def save_memories(memories):
    """Save memories to the JSON file."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(memories, file, indent=4, ensure_ascii=False)
        return True
    except (OSError, TypeError) as error:
        print(f"Could not save memories: {error}")
        return False


def remember(key, value):
    """Save or update a memory using a key and value."""
    key = str(key).strip().lower()
    value = str(value).strip()

    if not key or not value:
        return False

    memories = load_memories()
    memories[key] = {
        "value": value,
        "saved_at": datetime.now().isoformat(timespec="seconds")
    }
    return save_memories(memories)


def recall(key):
    """Retrieve a saved memory by its key."""
    key = str(key).strip().lower()
    memories = load_memories()
    item = memories.get(key)

    if isinstance(item, dict):
        return item.get("value")

    # Support older entries stored as plain strings.
    if isinstance(item, str):
        return item

    return None


def get_all_memories():
    """Return all saved memories."""
    return load_memories()


def forget(key):
    """Delete a specific memory."""
    key = str(key).strip().lower()
    memories = load_memories()

    if key not in memories:
        return False

    del memories[key]
    return save_memories(memories)


def clear_memories():
    """Delete all saved memories."""
    return save_memories({})


if __name__ == "__main__":
    print("Testing Jarvis Memory")
    print("---------------------")

    remember("favorite_language", "Python")
    remember("assistant_owner", "Jeshma")

    print("Favorite language:", recall("favorite_language"))
    print("Assistant owner:", recall("assistant_owner"))
    print("All memories:", get_all_memories())

    print("\nMemory module test completed.")
