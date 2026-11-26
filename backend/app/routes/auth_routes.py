"""Authentication and Password Management API Routes."""
from flask import Blueprint, jsonify, request, session
from backend.app.authentication.auth import (
    authenticate_admin,
    authenticate_user,
    generate_password_reset_token,
    login_required,
    register_user,
    reset_password_with_token,
)
from backend.app.database.db import fetch_one

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/api/auth/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or request.form.to_dict()
    # Normalize field name variations from frontend forms
    if "full_name" not in data and "name" in data:
        data["full_name"] = data["name"]
    if "consent_given" not in data and "consent_data_collection" in data:
        data["consent_given"] = data["consent_data_collection"]
    if "confirm_password" not in data and "password_confirm" in data:
        data["confirm_password"] = data["password_confirm"]

    ok, res = register_user(data)
    if not ok:
        return jsonify({"success": False, "errors": res, "error": res[0] if res else "Registration failed"}), 400

    session.permanent = True
    session["user_id"] = res["user_id"]
    session["user_uuid"] = res["user_uuid"]
    session["user_name"] = res["full_name"]
    session["role"] = "user"
    session["lang"] = data.get("preferred_language", "en")

    return jsonify({
        "success": True,
        "message": "Account created successfully.",
        "user": res,
        "redirect_url": "/pages/schemes.html"
    }), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or request.form.to_dict()
    email = data.get("email", "")
    password = data.get("password", "")
    user = authenticate_user(email, password)
    if not user:
        return jsonify({"success": False, "error": "Invalid email or password. Please verify your credentials."}), 401

    session.permanent = True
    session["user_id"] = user["id"]
    session["user_uuid"] = user["user_uuid"]
    session["user_name"] = user["full_name"]
    session["role"] = user["role"]
    session["lang"] = user.get("preferred_language", "en")

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "user": user,
        "redirect_url": "/pages/schemes.html"
    }), 200


@auth_bp.route("/api/auth/admin-login", methods=["POST"])
def api_admin_login():
    data = request.get_json(silent=True) or request.form.to_dict()
    ident = data.get("username", "") or data.get("email", "")
    password = data.get("password", "")
    admin = authenticate_admin(ident, password)
    if not admin:
        return jsonify({"success": False, "error": "Invalid administrative credentials."}), 401

    session["admin_id"] = admin["id"]
    session["admin_user"] = admin["username"]
    session["admin_role"] = admin["role"]

    return jsonify({"success": True, "message": "Admin login successful.", "admin": admin}), 200


@auth_bp.route("/api/auth/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."}), 200


@auth_bp.route("/api/auth/forgot-password", methods=["POST"])
def api_forgot_password():
    data = request.get_json(silent=True) or request.form.to_dict()
    email = data.get("email", "")
    ok, token_or_msg = generate_password_reset_token(email)
    return jsonify({"success": ok, "message": "If this email is registered, a password reset token has been generated.", "reset_token": token_or_msg if ok else None}), 200


@auth_bp.route("/api/auth/reset-password", methods=["POST"])
def api_reset_password():
    data = request.get_json(silent=True) or request.form.to_dict()
    token = data.get("token", "")
    new_pw = data.get("new_password", "")
    ok, msg = reset_password_with_token(token, new_pw)
    return jsonify({"success": ok, "message": msg}), (200 if ok else 400)


@auth_bp.route("/api/auth/me", methods=["GET"])
def api_me():
    user_id = session.get("user_id")
    admin_id = session.get("admin_id")
    if user_id:
        u = fetch_one("SELECT id, user_uuid, full_name, email, phone, role, preferred_language, consent_given FROM users WHERE id = %s", (user_id,))
        return jsonify({"authenticated": True, "role": "user", "user": u})
    if admin_id:
        a = fetch_one("SELECT id, username, email, role FROM admin_users WHERE id = %s", (admin_id,))
        return jsonify({"authenticated": True, "role": "admin", "admin": a})
    return jsonify({"authenticated": False}), 200
