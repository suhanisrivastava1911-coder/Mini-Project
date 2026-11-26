"""Profile management with privacy-first consent enforcement and AES encryption."""
import json
from typing import Any, Dict, Optional, Tuple
from backend.app.database.crypto import decrypt_data, encrypt_data
from backend.app.database.db import execute_query, fetch_one
from backend.app.utils.validators import parse_amount, sanitize_text


def calculate_completion(profile: Dict[str, Any]) -> int:
    """Calculate profile completion percentage."""
    fields = [
        profile.get("business_name"),
        profile.get("business_sector"),
        profile.get("state"),
        profile.get("district"),
        profile.get("gender"),
        profile.get("social_category"),
        profile.get("business_stage"),
        profile.get("funding_requirement"),
        profile.get("household_income")
    ]
    completed = sum(1 for f in fields if f is not None and str(f).strip() != "")
    return int((completed / len(fields)) * 100)


def get_user_profile(user_id: int) -> Optional[Dict[str, Any]]:
    """Fetch user profile with sensitive data decryption."""
    prof = fetch_one(
        """
        SELECT up.*, u.full_name, u.email, u.phone, u.preferred_language, u.consent_given
        FROM user_profiles up
        JOIN users u ON u.id = up.user_id
        WHERE up.user_id = %s
        """,
        (user_id,)
    )
    if not prof:
        # Return basic user info even if profile table row not yet created
        u = fetch_one("SELECT id AS user_id, full_name, email, phone, preferred_language, consent_given FROM users WHERE id = %s", (user_id,))
        return u

    prof["annual_turnover"] = float(prof["annual_turnover"])
    prof["household_income"] = float(prof["household_income"])
    prof["funding_requirement"] = float(prof["funding_requirement"])
    prof["udyam_registered"] = bool(prof["udyam_registered"])
    if isinstance(prof.get("support_types"), str):
        try:
            prof["support_types"] = json.loads(prof["support_types"])
        except Exception:
            prof["support_types"] = []

    # Decrypt sensitive payload if present
    if prof.get("encrypted_sensitive_data"):
        try:
            decrypted = decrypt_data(prof["encrypted_sensitive_data"])
            prof["sensitive_data"] = json.loads(decrypted)
        except Exception:
            prof["sensitive_data"] = {}
    return prof


def save_user_profile(user_id: int, data: Dict[str, Any], in_memory_only: bool = False) -> Tuple[bool, Any]:
    """Save profile. If in_memory_only or consent is False, process in-memory without storing to MySQL."""
    b_name = sanitize_text(data.get("business_name"), 180)
    b_sector = sanitize_text(data.get("business_sector") or data.get("sector"), 80)
    b_type = sanitize_text(data.get("business_type") or "Proprietorship", 60)
    b_stage = sanitize_text(data.get("business_stage") or "Startup", 40)
    state = sanitize_text(data.get("state"), 80)
    district = sanitize_text(data.get("district"), 80)
    loc_type = sanitize_text(data.get("location_type") or "Urban", 20)
    gender = sanitize_text(data.get("gender"), 40)
    category = sanitize_text(data.get("social_category"), 40)
    age = int(data["age"]) if data.get("age") and str(data["age"]).isdigit() else None
    has_udyam = bool(str(data.get("udyam_registered") or data.get("has_udyam")).lower() in ("true", "1", "yes", "on"))

    funding_req = parse_amount(data.get("funding_requirement")) or 0.0
    household_inc = parse_amount(data.get("household_income") or data.get("annual_income")) or 0.0
    annual_turnover = parse_amount(data.get("annual_turnover")) or 0.0
    b_age_months = int(data.get("business_age_months") or 0)
    purpose = sanitize_text(data.get("funding_purpose") or data.get("specific_needs"), 1000)
    raw_desc = sanitize_text(data.get("raw_description") or data.get("raw_nlp_text"), 2000)

    support_types = data.get("support_types") or []
    if isinstance(support_types, str):
        try:
            support_types = json.loads(support_types)
        except Exception:
            support_types = [s.strip() for s in support_types.split(",") if s.strip()]

    profile_dict = {
        "user_id": user_id,
        "business_name": b_name,
        "business_sector": b_sector,
        "business_type": b_type,
        "business_stage": b_stage,
        "udyam_registered": has_udyam,
        "business_age_months": b_age_months,
        "annual_turnover": annual_turnover,
        "household_income": household_inc,
        "funding_requirement": funding_req,
        "funding_purpose": purpose,
        "support_types": support_types,
        "state": state,
        "district": district,
        "location_type": loc_type,
        "gender": gender,
        "social_category": category,
        "age": age,
        "raw_description": raw_desc,
        "profile_completion_percent": calculate_completion({
            "business_name": b_name, "business_sector": b_sector, "state": state,
            "district": district, "gender": gender, "social_category": category,
            "business_stage": b_stage, "funding_requirement": funding_req, "household_income": household_inc
        })
    }

    # If user opted out of persistence, return the in-memory dictionary
    user_row = fetch_one("SELECT consent_given FROM users WHERE id = %s", (user_id,))
    if in_memory_only or (user_row and not user_row.get("consent_given")):
        return True, profile_dict

    # Encrypt private notes / sensitive financial detail with AES
    sensitive_payload = json.dumps({"notes": purpose, "private_phone": data.get("phone")})
    encrypted_payload = encrypt_data(sensitive_payload)

    existing = fetch_one("SELECT id FROM user_profiles WHERE user_id = %s", (user_id,))
    if existing:
        execute_query(
            """
            UPDATE user_profiles
            SET business_name = %s, business_sector = %s, business_type = %s, business_stage = %s,
                udyam_registered = %s, business_age_months = %s, annual_turnover = %s, household_income = %s,
                funding_requirement = %s, funding_purpose = %s, support_types = %s, state = %s, district = %s,
                location_type = %s, gender = %s, social_category = %s, age = %s, encrypted_sensitive_data = %s,
                raw_description = %s, profile_completion_percent = %s
            WHERE user_id = %s
            """,
            (
                b_name, b_sector, b_type, b_stage, has_udyam, b_age_months, annual_turnover, household_inc,
                funding_req, purpose, json.dumps(support_types), state, district, loc_type, gender, category,
                age, encrypted_payload, raw_desc, profile_dict["profile_completion_percent"], user_id
            )
        )
    else:
        execute_query(
            """
            INSERT INTO user_profiles (
                user_id, business_name, business_sector, business_type, business_stage,
                udyam_registered, business_age_months, annual_turnover, household_income,
                funding_requirement, funding_purpose, support_types, state, district,
                location_type, gender, social_category, age, encrypted_sensitive_data,
                raw_description, profile_completion_percent
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id, b_name, b_sector, b_type, b_stage, has_udyam, b_age_months, annual_turnover, household_inc,
                funding_req, purpose, json.dumps(support_types), state, district, loc_type, gender, category,
                age, encrypted_payload, raw_desc, profile_dict["profile_completion_percent"]
            )
        )
    return True, get_user_profile(user_id)


def delete_user_and_profile(user_id: int) -> None:
    """Cascade delete user, profile, matches, checklists, and saved schemes."""
    execute_query("DELETE FROM users WHERE id = %s", (user_id,))
