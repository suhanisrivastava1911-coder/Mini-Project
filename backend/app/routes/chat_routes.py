"""Conversational Chat Assistant API Routes."""
from flask import Blueprint, jsonify, request, session
from backend.app.services.chat_service import (
    clear_chat_history,
    get_chat_history,
    get_or_create_session,
    process_user_message,
)
from backend.app.services.profile_service import get_user_profile

chat_bp = Blueprint("chat_bp", __name__)


@chat_bp.route("/api/chat/message", methods=["POST"])
def api_chat_message():
    data = request.get_json(silent=True) or {}
    message_text = data.get("message", "").strip()
    session_uuid = data.get("session_uuid")
    lang = data.get("language") or session.get("lang", "en")
    user_id = session.get("user_id")

    if not message_text:
        return jsonify({"success": False, "error": "Message text is required."}), 400

    # Retrieve or create session
    chat_sess = get_or_create_session(user_id, language=lang)
    existing_prof = data.get("current_profile")
    if not existing_prof and user_id:
        existing_prof = get_user_profile(user_id) or {}

    response_payload = process_user_message(
        session_id=chat_sess["id"],
        message_text=message_text,
        existing_profile=existing_prof,
        language=lang
    )
    response_payload["session_uuid"] = chat_sess["session_uuid"]
    response_payload["success"] = True
    return jsonify(response_payload), 200


@chat_bp.route("/api/chat/history", methods=["GET"])
def api_chat_history():
    user_id = session.get("user_id")
    chat_sess = get_or_create_session(user_id)
    history = get_chat_history(chat_sess["id"])
    return jsonify({"success": True, "session_uuid": chat_sess["session_uuid"], "history": history}), 200


@chat_bp.route("/api/chat/clear", methods=["POST"])
def api_clear_chat():
    user_id = session.get("user_id")
    chat_sess = get_or_create_session(user_id)
    clear_chat_history(chat_sess["id"])
    return jsonify({"success": True, "message": "Conversation history cleared."}), 200
