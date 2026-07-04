import json
import os
from datetime import datetime


HISTORY_FILE = "history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_to_history(product_name, verdict, category):
    history = load_history()

    entry = {
        "product_name": product_name,
        "category": category,
        "badge": verdict.get("badge", "UNKNOWN"),
        "rating": verdict.get("rating", 0),
        "summary": verdict.get("summary", ""),
        "pros": verdict.get("pros", []),
        "cons": verdict.get("cons", []),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    # avoid duplicates — update if same product analyzed again
    history = [h for h in history if h["product_name"].lower() != product_name.lower()]
    history.insert(0, entry)

    # keep only last 20
    history = history[:20]

    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"History save error: {e}")


def clear_history():
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
    except Exception as e:
        print(f"History clear error: {e}")