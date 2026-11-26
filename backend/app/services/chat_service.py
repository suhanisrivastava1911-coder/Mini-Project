"""Conversational AI Assistant service for natural multilingual intake."""
import json
import uuid
from typing import Any, Dict, List, Optional
from backend.app.database.db import execute_query, fetch_all, fetch_one
from backend.app.nlp.clarification import detect_missing_attributes, format_conversational_response
from backend.app.nlp.entity_extractor import extract_entities_from_text


def get_or_create_session(user_id: Optional[int], language: str = "en") -> Dict[str, Any]:
    """Get active session or spawn a new session UUID."""
    if user_id:
        existing = fetch_one(
            "SELECT id, session_uuid, user_id, language, is_active FROM chat_sessions WHERE user_id = %s AND is_active = TRUE ORDER BY id DESC LIMIT 1",
            (user_id,)
        )
        if existing:
            return existing

    sess_uuid = str(uuid.uuid4())
    s_id = execute_query(
        "INSERT INTO chat_sessions (session_uuid, user_id, language, is_active) VALUES (%s, %s, %s, TRUE)",
        (sess_uuid, user_id, language)
    )
    return {"id": s_id, "session_uuid": sess_uuid, "user_id": user_id, "language": language}


def process_user_message(session_id: int, message_text: str, existing_profile: Optional[Dict[str, Any]] = None, language: str = "en") -> Dict[str, Any]:
    """Process incoming message via NLP pipeline, record history, and return assistant response."""
    existing = existing_profile or {}

    # Extract entities
    newly_extracted = extract_entities_from_text(message_text)

    # Merge extracted entities into profile without overwriting existing valid values with None
    merged_profile = dict(existing)
    for k, v in newly_extracted.items():
        if v is not None and v != "" and v != []:
            merged_profile[k] = v

    # Save user message to database
    execute_query(
        "INSERT INTO chat_messages (session_id, sender, message_text, extracted_entities_json) VALUES (%s, 'user', %s, %s)",
        (session_id, message_text, json.dumps(newly_extracted))
    )

    # Detect missing attributes
    missing = detect_missing_attributes(merged_profile)

    # Generate natural response and suggestions
    reply_text, suggestions = format_conversational_response(merged_profile, missing, lang=language)

    # Save assistant response
    execute_query(
        "INSERT INTO chat_messages (session_id, sender, message_text) VALUES (%s, 'assistant', %s)",
        (session_id, reply_text)
    )

    ready_to_match = (len(missing) <= 1 and merged_profile.get("state") and merged_profile.get("sector"))

    return {
        "reply": reply_text,
        "suggestions": suggestions,
        "extracted_profile": merged_profile,
        "newly_detected": newly_extracted,
        "missing_attributes": missing,
        "ready_to_match": ready_to_match
    }


def get_chat_history(session_id: int) -> List[Dict[str, Any]]:
    """Fetch chronological chat history."""
    return fetch_all(
        "SELECT id, sender, message_text, created_at FROM chat_messages WHERE session_id = %s ORDER BY id ASC",
        (session_id,)
    )


def clear_chat_history(session_id: int) -> None:
    """Clear chat messages for a session."""
    execute_query("DELETE FROM chat_messages WHERE session_id = %s", (session_id,))
