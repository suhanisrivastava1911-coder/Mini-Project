"""Checklist & Saved Schemes API Routes."""
from flask import Blueprint, Response, jsonify, request, session
from backend.app.authentication.auth import login_required
from backend.app.services.checklist_service import (
    get_or_create_checklist,
    get_user_saved_schemes,
    save_scheme,
    toggle_checklist_item,
    unsave_scheme,
)
from backend.app.services.guidance_service import (
    generate_printable_checklist_text,
    get_guidance_for_scheme,
)

checklist_bp = Blueprint("checklist_bp", __name__)


@checklist_bp.route("/api/checklists/<int:scheme_id>", methods=["GET"])
@checklist_bp.route("/api/checklist/<int:scheme_id>", methods=["GET"])
def api_get_checklist(scheme_id: int):
    user_id = session.get("user_id")
    # Return guidance bundle even for guest users
    bundle = get_guidance_for_scheme(scheme_id)
    if not bundle:
        return jsonify({"success": False, "error": "Scheme not found"}), 404
    return jsonify({
        "success": True,
        "scheme": bundle.get("scheme"),
        "items": bundle.get("documents", []),
        "steps": bundle.get("guide_steps", [])
    }), 200


@checklist_bp.route("/api/checklists/<int:checklist_id>/item/<int:item_id>", methods=["PUT"])
@checklist_bp.route("/api/checklist/item/<int:item_id>", methods=["PUT"])
def api_toggle_item(item_id: int, checklist_id: int = 1):
    data = request.get_json(silent=True) or {}
    is_checked = bool(data.get("is_checked") or data.get("is_ready", False))
    return jsonify({"success": True, "item_id": item_id, "is_ready": is_checked}), 200


@checklist_bp.route("/api/saved-schemes", methods=["GET"])
@checklist_bp.route("/api/schemes/saved", methods=["GET"])
def api_get_saved():
    user_id = session.get("user_id")
    if user_id:
        try:
            saved = get_user_saved_schemes(user_id)
            return jsonify({"success": True, "count": len(saved), "saved_schemes": saved}), 200
        except Exception:
            pass
    # Session-based fallback for guest / in-memory mode
    saved_ids = session.get("saved_scheme_ids", [])
    from backend.app.services.scheme_service import get_scheme_by_id
    saved = [get_scheme_by_id(sid) for sid in saved_ids if get_scheme_by_id(sid)]
    return jsonify({"success": True, "count": len(saved), "saved_schemes": saved}), 200


@checklist_bp.route("/api/saved-schemes", methods=["POST"])
@checklist_bp.route("/api/schemes/save", methods=["POST"])
def api_save_scheme():
    user_id = session.get("user_id")
    data = request.get_json(silent=True) or {}
    scheme_id = data.get("scheme_id")
    notes = data.get("notes", "")
    if not scheme_id:
        return jsonify({"success": False, "error": "scheme_id required"}), 400
    
    sid = int(scheme_id)
    if user_id:
        try:
            save_scheme(user_id, sid, notes)
            return jsonify({"success": True, "message": "Scheme saved to your dashboard."}), 200
        except Exception:
            pass

    # Save to session
    saved_ids = session.get("saved_scheme_ids", [])
    if sid not in saved_ids:
        saved_ids.append(sid)
        session["saved_scheme_ids"] = saved_ids
    return jsonify({"success": True, "message": "Scheme bookmarked to your dashboard."}), 200


@checklist_bp.route("/api/saved-schemes/<int:scheme_id>", methods=["DELETE"])
@checklist_bp.route("/api/schemes/saved/<int:scheme_id>", methods=["DELETE"])
def api_unsave_scheme(scheme_id: int):
    user_id = session.get("user_id")
    if user_id:
        try:
            unsave_scheme(user_id, scheme_id)
            return jsonify({"success": True, "message": "Scheme removed from saved list."}), 200
        except Exception:
            pass

    saved_ids = session.get("saved_scheme_ids", [])
    if scheme_id in saved_ids:
        saved_ids.remove(scheme_id)
        session["saved_scheme_ids"] = saved_ids
    return jsonify({"success": True, "message": "Scheme removed from saved list."}), 200


@checklist_bp.route("/api/schemes/<int:scheme_id>/guidance", methods=["GET"])
def api_scheme_guidance(scheme_id: int):
    bundle = get_guidance_for_scheme(scheme_id)
    if not bundle:
        return jsonify({"success": False, "error": "Scheme not found"}), 404
    return jsonify({"success": True, "guidance": bundle}), 200


@checklist_bp.route("/api/schemes/<int:scheme_id>/guide/download", methods=["GET"])
def api_download_checklist(scheme_id: int):
    user_name = session.get("user_name", "Entrepreneur")
    text = generate_printable_checklist_text(scheme_id, user_name)
    if not text:
        return jsonify({"success": False, "error": "Scheme not found"}), 404
    return Response(
        text,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename=Scheme_Application_Checklist_{scheme_id}.txt"}
    )
