"""Administrative API Routes."""
from flask import Blueprint, jsonify, request, session
from backend.app.admin.admin_service import (
    delete_scheme,
    get_admin_dashboard_stats,
    get_matching_analytics,
    list_users,
    save_scheme,
)
from backend.app.authentication.auth import admin_required
from backend.app.services.profile_service import delete_user_and_profile

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/api/admin/dashboard", methods=["GET"])
@admin_required
def api_admin_dashboard():
    stats = get_admin_dashboard_stats()
    return jsonify({"success": True, "stats": stats}), 200


@admin_bp.route("/api/admin/analytics", methods=["GET"])
@admin_required
def api_admin_analytics():
    analytics = get_matching_analytics()
    return jsonify({"success": True, "analytics": analytics}), 200


@admin_bp.route("/api/admin/users", methods=["GET"])
@admin_required
def api_admin_users():
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))
    users = list_users(limit, offset)
    return jsonify({"success": True, "count": len(users), "users": users}), 200


@admin_bp.route("/api/admin/users/<int:user_id>", methods=["DELETE"])
@admin_required
def api_admin_delete_user(user_id: int):
    delete_user_and_profile(user_id)
    return jsonify({"success": True, "message": "User deleted successfully."}), 200


@admin_bp.route("/api/admin/schemes", methods=["POST"])
@admin_required
def api_admin_create_scheme():
    data = request.get_json(silent=True) or request.form.to_dict()
    admin_id = session.get("admin_id")
    s_id = save_scheme(data, scheme_id=None, admin_id=admin_id)
    return jsonify({"success": True, "message": "Scheme created.", "scheme_id": s_id}), 201


@admin_bp.route("/api/admin/schemes/<int:scheme_id>", methods=["PUT"])
@admin_required
def api_admin_update_scheme(scheme_id: int):
    data = request.get_json(silent=True) or request.form.to_dict()
    admin_id = session.get("admin_id")
    s_id = save_scheme(data, scheme_id=scheme_id, admin_id=admin_id)
    return jsonify({"success": True, "message": "Scheme updated.", "scheme_id": s_id}), 200


@admin_bp.route("/api/admin/schemes/<int:scheme_id>", methods=["DELETE"])
@admin_required
def api_admin_delete_scheme(scheme_id: int):
    admin_id = session.get("admin_id")
    delete_scheme(scheme_id, admin_id=admin_id)
    return jsonify({"success": True, "message": "Scheme deleted."}), 200
