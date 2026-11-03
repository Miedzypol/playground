import json
import time
from pathlib import Path

from config import _base_system_prompt

SESSION_FILE = Path("data/sessions.json")
messages = []
current_session_id = None


def _load_sessions():
    if not SESSION_FILE.exists():
        return []
    with open(SESSION_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    if isinstance(data, list):
        return data
    return [data]


def _new_messages():
    return [{"role": "system", "content": _base_system_prompt}]


def startsession(session_id=None):
    global current_session_id
    sessions = _load_sessions()
    if not sessions:
        newsession()
        return
    if session_id is None:
        session = sessions[-1]
    else:
        session = next(
            (item for item in sessions if item["session_id"] == session_id),
            sessions[-1],
        )
    current_session_id = session["session_id"]
    messages[:] = session.get("messages", [])

    if not messages or messages[0].get("role") != "system":
        messages.insert(0, {"role": "system", "content": _base_system_prompt})
    else:
        model_instructions_marker = "\n\nModel-Specific Instructions:\n"
        model_instructions = messages[0]["content"].partition(
            model_instructions_marker
        )[2]
        messages[0]["content"] = _base_system_prompt
        if model_instructions:
            messages[0]["content"] += (
                f"{model_instructions_marker}{model_instructions}"
            )

def newsession():
    global current_session_id
    sessions = _load_sessions()
    current_session_id = max(
        (session["session_id"] for session in sessions),
        default=-1, ) + 1
    messages[:] = _new_messages()
    savesession()

def addmessage(role, content):
    messages.append({"role": role, "content": content})

def savesession():
    global current_session_id
    sessions = _load_sessions()
    if current_session_id is None:
        current_session_id = max(
            (session["session_id"] for session in sessions),
            default=-1,
        ) + 1
    current_session = {
        "session_id": current_session_id,
        "messages": messages,
        "created_at": int(time.time()),
    }
    for index, session in enumerate(sessions):
        if session["session_id"] == current_session_id:
            sessions[index] = current_session
            break
    else:
        sessions.append(current_session)
    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_FILE, "w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=4, ensure_ascii=False)