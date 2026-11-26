"""User and Admin authentication, password hashing, session management, and access control."""
import secrets
import uuid
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, List, Optional, Tuple
from flask import abort, jsonify, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from backend.app.database.db import execute_query, fetch_one
from backend.app.utils.validators import EMAIL_REGEX, sanitize_text


def hash_password(password: str) -> str:
    """PBKDF2-SHA256 salted hash."""
    return generate_password_hash(password, method="pbkdf2:sha256:600000")


def verify_password(pw_hash: str, password: str) -> bool:
    """Verify hash."""
    if not pw_hash or not password:
        return False
    return check_password_hash(pw_hash, password)


def register_user(payload: Dict[str, Any]) -> Tuple[bool, Any]:
    """Validate registration and insert new user record with explicit consent."""
    full_name = sanitize_text(payload.get("full_name"), 120)
    email = sanitize_text(payload.get("email"), 160).lower()
    phone = sanitize_text(payload.get("phone"), 20)
    password = str(payload.get("password") or "")
    confirm = str(payload.get("confirm_password") or "")
    lang = sanitize_text(payload.get("preferred_language") or "en", 10)
    consent = str(payload.get("consent_given") or "").lower() in ("true", "1", "yes", "on")

    errors: List[str] = []
    if len(full_name) < 2:
        errors.append("Full name must be at least 2 characters.")
    if not EMAIL_REGEX.match(email):
        errors.append("Please provide a valid email address.")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        errors.append("Password must contain both letters and digits.")
    if confirm and password != confirm:
        errors.append("Passwords do not match.")
    if not consent:
        errors.append("Explicit privacy consent is required before creating an account.")

    if errors:
        return False, errors

    existing = fetch_one("SELECT id FROM users WHERE email = %s", (email,))
    if existing:
        return False, ["An account with this email address already exists. Please log in."]

    user_uuid = str(uuid.uuid4())
    pw_hash = hash_password(password)

    user_id = execute_query(
        """
        INSERT INTO users (user_uuid, full_name, email, phone, password_hash, role, preferred_language, consent_given, consent_version, consent_timestamp)
        VALUES (%s, %s, %s, %s, %s, 'user', %s, TRUE, '1.0', CURRENT_TIMESTAMP)
        """,
        (user_uuid, full_name, email, phone, pw_hash, lang)
    )
    return True, {"user_id": user_id, "user_uuid": user_uuid, "full_name": full_name, "email": email}


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate regular entrepreneur."""
    email_clean = sanitize_text(email, 160).lower()
    if not email_clean or not password:
        return None
    user = fetch_one(
        "SELECT id, user_uuid, full_name, email, role, preferred_language, password_hash, is_active FROM users WHERE email = %s",
        (email_clean,)
    )
    if not user or not user["is_active"] or not verify_password(user["password_hash"], password):
        return None
    user.pop("password_hash", None)
    return user


def authenticate_admin(identifier: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate administrative user by username or email."""
    ident = sanitize_text(identifier, 160).lower()
    if not ident or not password:
        return None
    admin = fetch_one(
        "SELECT id, username, email, role, password_hash, is_active FROM admin_users WHERE username = %s OR email = %s",
        (ident, ident)
    )
    if not admin or not admin["is_active"] or not verify_password(admin["password_hash"], password):
        return None
    execute_query("UPDATE admin_users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", (admin["id"],))
    admin.pop("password_hash", None)
    return admin


def generate_password_reset_token(email: str) -> Tuple[bool, str]:
    """Create a temporary password reset token valid for 1 hour."""
    email_clean = sanitize_text(email, 160).lower()
    user = fetch_one("SELECT id FROM users WHERE email = %s", (email_clean,))
    if not user:
        return False, "If that email is registered, a password reset link has been generated."
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)
    execute_query(
        "UPDATE users SET reset_token = %s, reset_token_expiry = %s WHERE id = %s",
        (token, expiry, user["id"])
    )
    return True, token


def reset_password_with_token(token: str, new_password: str) -> Tuple[bool, str]:
    """Reset password using valid unexpired token."""
    if not token or len(new_password) < 8:
        return False, "Invalid token or password does not meet requirements."
    user = fetch_one(
        "SELECT id, reset_token_expiry FROM users WHERE reset_token = %s",
        (token,)
    )
    if not user or not user.get("reset_token_expiry") or user["reset_token_expiry"] < datetime.utcnow():
        return False, "Reset token is invalid or has expired."
    pw_hash = hash_password(new_password)
    execute_query(
        "UPDATE users SET password_hash = %s, reset_token = NULL, reset_token_expiry = NULL WHERE id = %s",
        (pw_hash, user["id"])
    )
    return True, "Password has been successfully reset. You can now log in."


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            if request.path.startswith("/api/"):
                return jsonify({"error": "Authentication required", "login_url": "/pages/login.html"}), 401
            return redirect("/pages/login.html?next=" + request.path)
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_id"):
            if request.path.startswith("/api/"):
                return jsonify({"error": "Admin access required"}), 403
            return redirect("/pages/admin_login.html?next=" + request.path)
        return f(*args, **kwargs)
    return decorated
