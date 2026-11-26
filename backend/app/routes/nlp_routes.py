"""NLP Extraction, Normalization, and Clarification API Routes."""
from flask import Blueprint, jsonify, request
from backend.app.nlp.clarification import detect_missing_attributes, format_conversational_response
from backend.app.nlp.entity_extractor import extract_entities_from_text
from backend.app.nlp.hinglish_normalizer import normalize_text

nlp_bp = Blueprint("nlp_bp", __name__)


@nlp_bp.route("/api/nlp/extract", methods=["POST"])
@nlp_bp.route("/api/nlp/extract-profile", methods=["POST"])
def api_extract_profile():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"success": False, "error": "Text description is required."}), 400

    extracted = extract_entities_from_text(text)
    missing = detect_missing_attributes(extracted)
    return jsonify({
        "success": True,
        "extracted_profile": extracted,
        "missing_attributes": missing,
        "confidence_score": extracted.get("confidence_score", 0),
        "extraction_method": extracted.get("extraction_method")
    }), 200


@nlp_bp.route("/api/nlp/normalize", methods=["POST"])
def api_normalize_text():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    norm = normalize_text(text)
    return jsonify({"success": True, "original": text, "normalized": norm}), 200


@nlp_bp.route("/api/nlp/clarification", methods=["POST"])
def api_get_clarification():
    data = request.get_json(silent=True) or {}
    profile = data.get("profile", {})
    lang = data.get("language", "en")
    missing = detect_missing_attributes(profile)
    question, suggestions = format_conversational_response(profile, missing, lang=lang)
    return jsonify({
        "success": True,
        "has_missing": len(missing) > 0,
        "missing_count": len(missing),
        "missing_attributes": missing,
        "follow_up_question": question,
        "suggested_replies": suggestions
    }), 200
