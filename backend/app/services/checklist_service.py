"""Document readiness checklist and saved schemes persistence."""
from typing import Any, Dict, List, Optional
from backend.app.database.db import execute_query, fetch_all, fetch_one


def get_or_create_checklist(user_id: int, scheme_id: int) -> Dict[str, Any]:
    """Get active checklist for a scheme or populate from scheme_document requirements."""
    chk = fetch_one(
        "SELECT * FROM application_checklists WHERE user_id = %s AND scheme_id = %s",
        (user_id, scheme_id)
    )
    if not chk:
        scheme = fetch_one("SELECT scheme_name FROM scheme_master WHERE id = %s", (scheme_id,))
        title = f"Document Checklist - {scheme['scheme_name'] if scheme else 'Scheme Application'}"
        chk_id = execute_query(
            "INSERT INTO application_checklists (user_id, scheme_id, title, progress_percent, is_completed) VALUES (%s, %s, %s, 0.0, FALSE)",
            (user_id, scheme_id, title)
        )
        # Populate checklist items from scheme_document
        docs = fetch_all("SELECT id, document_name, description, is_mandatory FROM scheme_document WHERE scheme_id = %s ORDER BY sort_order ASC", (scheme_id,))
        for doc in docs:
            execute_query(
                "INSERT INTO checklist_items (checklist_id, document_id, item_name, is_checked) VALUES (%s, %s, %s, FALSE)",
                (chk_id, doc["id"], doc["document_name"])
            )
        chk = fetch_one("SELECT * FROM application_checklists WHERE id = %s", (chk_id,))

    # Fetch items
    items = fetch_all(
        """
        SELECT ci.*, sd.document_name_hi, sd.description, sd.is_mandatory, sd.document_category
        FROM checklist_items ci
        LEFT JOIN scheme_document sd ON sd.id = ci.document_id
        WHERE ci.checklist_id = %s
        ORDER BY ci.id ASC
        """,
        (chk["id"],)
    )
    chk["items"] = items
    return chk


def toggle_checklist_item(checklist_id: int, item_id: int, is_checked: bool) -> Dict[str, Any]:
    """Toggle item and recalculate overall progress percent."""
    execute_query(
        "UPDATE checklist_items SET is_checked = %s, checked_at = CURRENT_TIMESTAMP WHERE id = %s AND checklist_id = %s",
        (is_checked, item_id, checklist_id)
    )
    # Recalculate progress
    items = fetch_all("SELECT is_checked FROM checklist_items WHERE checklist_id = %s", (checklist_id,))
    total = len(items)
    checked = sum(1 for i in items if i["is_checked"])
    pct = round((checked / total * 100.0), 2) if total > 0 else 0.0
    is_completed = (pct >= 100.0)

    execute_query(
        "UPDATE application_checklists SET progress_percent = %s, is_completed = %s WHERE id = %s",
        (pct, is_completed, checklist_id)
    )
    return {"checklist_id": checklist_id, "item_id": item_id, "progress_percent": pct, "is_completed": is_completed}


def save_scheme(user_id: int, scheme_id: int, notes: str = "") -> bool:
    """Bookmark scheme for user."""
    existing = fetch_one("SELECT id FROM saved_schemes WHERE user_id = %s AND scheme_id = %s", (user_id, scheme_id))
    if existing:
        return True
    execute_query(
        "INSERT INTO saved_schemes (user_id, scheme_id, notes) VALUES (%s, %s, %s)",
        (user_id, scheme_id, notes)
    )
    return True


def unsave_scheme(user_id: int, scheme_id: int) -> bool:
    """Remove scheme bookmark."""
    execute_query("DELETE FROM saved_schemes WHERE user_id = %s AND scheme_id = %s", (user_id, scheme_id))
    return True


def get_user_saved_schemes(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve bookmarked schemes with authority and benefits."""
    return fetch_all(
        """
        SELECT ss.id AS saved_id, ss.saved_at, ss.notes,
               sm.id, sm.scheme_code, sm.scheme_name, sm.scheme_name_hi,
               sm.scheme_category, sm.authority_level, sm.ministry_or_org,
               sm.benefit_type, sm.max_benefit_amount, sm.subsidy_info,
               sm.application_deadline, sm.deadline_note, sm.official_url
        FROM saved_schemes ss
        JOIN scheme_master sm ON sm.id = ss.scheme_id
        WHERE ss.user_id = %s AND sm.scheme_status = 'Active'
        ORDER BY ss.saved_at DESC
        """,
        (user_id,)
    )
