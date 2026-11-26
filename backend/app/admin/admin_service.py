"""Administrative dashboard, scheme management, user administration, and audit trails."""
from typing import Any, Dict, List, Optional
from backend.app.database.db import execute_query, fetch_all, fetch_one
from backend.app.utils.validators import parse_amount, sanitize_text


def get_admin_dashboard_stats() -> Dict[str, Any]:
    """Retrieve high-level overview metrics."""
    total_users = fetch_one("SELECT COUNT(*) AS total FROM users WHERE role = 'user'")["total"]
    total_schemes = fetch_one("SELECT COUNT(*) AS total FROM scheme_master")["total"]
    active_schemes = fetch_one("SELECT COUNT(*) AS total FROM scheme_master WHERE scheme_status = 'Active'")["total"]
    expired_schemes = fetch_one("SELECT COUNT(*) AS total FROM scheme_master WHERE scheme_status = 'Expired'")["total"]
    total_matches = fetch_one("SELECT COUNT(*) AS total FROM match_result")["total"]

    # Category distribution
    cat_counts = fetch_all(
        "SELECT scheme_category, COUNT(*) AS count FROM scheme_master GROUP BY scheme_category ORDER BY count DESC LIMIT 6"
    )

    # Authority level distribution
    auth_counts = fetch_all(
        "SELECT authority_level, COUNT(*) AS count FROM scheme_master GROUP BY authority_level"
    )

    # Recent activity logs
    recent_audits = fetch_all(
        "SELECT al.*, au.username FROM audit_logs al LEFT JOIN admin_users au ON au.id = al.admin_id ORDER BY al.id DESC LIMIT 8"
    )

    return {
        "total_users": total_users,
        "total_schemes": total_schemes,
        "active_schemes": active_schemes,
        "expired_schemes": expired_schemes,
        "total_matches": total_matches,
        "category_distribution": cat_counts,
        "authority_distribution": auth_counts,
        "recent_audits": recent_audits
    }


def get_matching_analytics() -> Dict[str, Any]:
    """Retrieve deep analytics on popular sectors, state interest, and category distributions."""
    sector_interest = fetch_all(
        "SELECT business_sector, COUNT(*) AS count FROM user_profiles WHERE business_sector != '' GROUP BY business_sector ORDER BY count DESC LIMIT 8"
    )
    state_interest = fetch_all(
        "SELECT state, COUNT(*) AS count FROM user_profiles WHERE state != '' GROUP BY state ORDER BY count DESC LIMIT 8"
    )
    category_interest = fetch_all(
        "SELECT social_category, COUNT(*) AS count FROM user_profiles WHERE social_category != '' GROUP BY social_category ORDER BY count DESC"
    )
    gender_distribution = fetch_all(
        "SELECT gender, COUNT(*) AS count FROM user_profiles WHERE gender != '' GROUP BY gender ORDER BY count DESC"
    )
    most_matched_schemes = fetch_all(
        """
        SELECT sm.scheme_name, sm.scheme_code, COUNT(mr.id) AS matches_count,
               AVG(mr.match_score) AS avg_score
        FROM match_result mr
        JOIN scheme_master sm ON sm.id = mr.scheme_id
        WHERE mr.eligibility_status IN ('Eligible', 'Partially Eligible')
        GROUP BY sm.id, sm.scheme_name, sm.scheme_code
        ORDER BY matches_count DESC LIMIT 6
        """
    )
    return {
        "sector_interest": sector_interest,
        "state_interest": state_interest,
        "category_interest": category_interest,
        "gender_distribution": gender_distribution,
        "most_matched_schemes": most_matched_schemes
    }


def list_users(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """List registered users with profile snapshot."""
    return fetch_all(
        """
        SELECT u.id, u.user_uuid, u.full_name, u.email, u.phone, u.role, u.is_active,
               u.consent_given, u.created_at,
               up.business_name, up.business_sector, up.state, up.social_category
        FROM users u
        LEFT JOIN user_profiles up ON up.user_id = u.id
        WHERE u.role = 'user'
        ORDER BY u.id DESC
        LIMIT %s OFFSET %s
        """,
        (limit, offset)
    )


def log_audit(admin_id: Optional[int], action: str, target_type: str, target_id: Optional[int], details: str, ip: str = "127.0.0.1") -> None:
    """Record administrative audit log entry."""
    execute_query(
        "INSERT INTO audit_logs (admin_id, action, target_type, target_id, details, ip_address) VALUES (%s, %s, %s, %s, %s, %s)",
        (admin_id, action, target_type, target_id, details, ip)
    )


def save_scheme(data: Dict[str, Any], scheme_id: Optional[int] = None, admin_id: Optional[int] = None) -> int:
    """Create or update scheme with rule."""
    code = sanitize_text(data.get("scheme_code"), 50)
    name = sanitize_text(data.get("scheme_name"), 220)
    name_hi = sanitize_text(data.get("scheme_name_hi"), 255)
    desc = sanitize_text(data.get("scheme_description"), 3000)
    desc_hi = sanitize_text(data.get("scheme_description_hi"), 3000)
    cat = sanitize_text(data.get("scheme_category"), 80)
    auth = sanitize_text(data.get("authority_level") or "Central", 20)
    ministry = sanitize_text(data.get("ministry_or_org"), 200)
    states = sanitize_text(data.get("eligible_states") or "All India", 255)
    target = sanitize_text(data.get("target_beneficiary_groups"), 255)
    b_type = sanitize_text(data.get("benefit_type"), 100)
    max_amt = parse_amount(data.get("max_benefit_amount")) or 0.0
    sub_info = sanitize_text(data.get("subsidy_info"), 255)
    deadline = data.get("application_deadline") or None
    deadline_note = sanitize_text(data.get("deadline_note") or "Ongoing", 160)
    official_url = sanitize_text(data.get("official_url"), 255)
    source_url = sanitize_text(data.get("source_url") or official_url, 255)
    status = sanitize_text(data.get("scheme_status") or "Active", 20)
    verif = sanitize_text(data.get("verification_status") or "Verified", 30)

    if scheme_id:
        execute_query(
            """
            UPDATE scheme_master
            SET scheme_name = %s, scheme_name_hi = %s, scheme_description = %s, scheme_description_hi = %s,
                scheme_category = %s, authority_level = %s, ministry_or_org = %s, eligible_states = %s,
                target_beneficiary_groups = %s, benefit_type = %s, max_benefit_amount = %s, subsidy_info = %s,
                application_deadline = %s, deadline_note = %s, official_url = %s, source_url = %s,
                scheme_status = %s, verification_status = %s, last_verified_date = CURRENT_DATE
            WHERE id = %s
            """,
            (
                name, name_hi, desc, desc_hi, cat, auth, ministry, states, target, b_type, max_amt,
                sub_info, deadline, deadline_note, official_url, source_url, status, verif, scheme_id
            )
        )
        s_id = scheme_id
        log_audit(admin_id, "UPDATE_SCHEME", "SCHEME", s_id, f"Updated scheme {code} ({name})")
    else:
        s_id = execute_query(
            """
            INSERT INTO scheme_master (
                scheme_code, scheme_name, scheme_name_hi, scheme_description, scheme_description_hi,
                scheme_category, authority_level, ministry_or_org, eligible_states, target_beneficiary_groups,
                benefit_type, max_benefit_amount, subsidy_info, application_deadline, deadline_note,
                official_url, source_url, scheme_status, verification_status, last_verified_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
            """,
            (
                code, name, name_hi, desc, desc_hi, cat, auth, ministry, states, target, b_type,
                max_amt, sub_info, deadline, deadline_note, official_url, source_url, status, verif
            )
        )
        # Ensure default eligibility rule row exists
        execute_query(
            """
            INSERT INTO eligibility_rule (scheme_id, eligible_genders, eligible_categories, eligible_states, eligible_sectors, eligible_stages)
            VALUES (%s, 'All', 'All', %s, 'All', 'All')
            """,
            (s_id, states)
        )
        log_audit(admin_id, "CREATE_SCHEME", "SCHEME", s_id, f"Created new scheme {code} ({name})")

    # Record verification history
    execute_query(
        "INSERT INTO scheme_verification_history (scheme_id, verified_by, verification_status, notes) VALUES (%s, %s, %s, %s)",
        (s_id, admin_id, verif, f"Saved by admin ID {admin_id}")
    )
    return s_id


def delete_scheme(scheme_id: int, admin_id: Optional[int] = None) -> None:
    """Delete scheme and cascade related records."""
    scheme = fetch_one("SELECT scheme_code, scheme_name FROM scheme_master WHERE id = %s", (scheme_id,))
    name = scheme["scheme_name"] if scheme else str(scheme_id)
    execute_query("DELETE FROM scheme_master WHERE id = %s", (scheme_id,))
    log_audit(admin_id, "DELETE_SCHEME", "SCHEME", scheme_id, f"Deleted scheme: {name}")
