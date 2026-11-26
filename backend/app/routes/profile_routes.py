"""Profile API Routes."""
import json
from flask import Blueprint, Response, jsonify, request, session
from backend.app.authentication.auth import login_required
from backend.app.database.db import execute_query, fetch_all, fetch_one
from backend.app.services.profile_service import delete_user_and_profile, get_user_profile, save_user_profile

profile_bp = Blueprint("profile_bp", __name__)


@profile_bp.route("/api/profile", methods=["GET"])
@login_required
def api_get_profile():
    user_id = session["user_id"]
    prof = get_user_profile(user_id)
    return jsonify({"success": True, "profile": prof}), 200


@profile_bp.route("/api/profile", methods=["POST", "PUT"])
@login_required
def api_save_profile():
    user_id = session["user_id"]
    data = request.get_json(silent=True) or request.form.to_dict()
    in_memory = data.get("in_memory", False)
    ok, res = save_user_profile(user_id, data, in_memory_only=in_memory)
    return jsonify({"success": ok, "profile": res}), (200 if ok else 400)


@profile_bp.route("/api/profile", methods=["DELETE"])
@login_required
def api_delete_profile():
    user_id = session["user_id"]
    delete_user_and_profile(user_id)
    session.clear()
    return jsonify({"success": True, "message": "Your profile and personal records have been permanently removed."}), 200


@profile_bp.route("/api/profile/export", methods=["GET"])
@login_required
def api_export_user_data():
    user_id = session["user_id"]
    u = fetch_one("SELECT id, user_uuid, full_name, email, phone, role, preferred_language, consent_given, consent_timestamp, created_at FROM users WHERE id = %s", (user_id,))
    p = get_user_profile(user_id)
    matches = fetch_all("SELECT mr.*, sm.scheme_name, sm.scheme_code FROM match_result mr JOIN scheme_master sm ON sm.id = mr.scheme_id WHERE mr.user_id = %s", (user_id,))
    saved = fetch_all("SELECT ss.*, sm.scheme_name FROM saved_schemes ss JOIN scheme_master sm ON sm.id = ss.scheme_id WHERE ss.user_id = %s", (user_id,))

    export_payload = {
        "user_account": u,
        "entrepreneur_profile": p,
        "match_history": matches,
        "saved_schemes": saved,
        "exported_at": "2026-11-26"
    }
    return Response(
        json.dumps(export_payload, indent=2, default=str),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=my_scheme_sahayak_data.json"}
    )
