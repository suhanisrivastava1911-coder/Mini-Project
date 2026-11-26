"""Intelligent Scheme Matching API Routes."""
import json
from flask import Blueprint, jsonify, request, session
from backend.app.database.db import execute_query, fetch_all, fetch_one
from backend.app.matching.engine import rank_and_match_schemes
from backend.app.services.profile_service import get_user_profile
from backend.app.services.scheme_service import get_all_schemes, get_scheme_by_id

matching_bp = Blueprint("matching_bp", __name__)


@matching_bp.route("/api/matching/match", methods=["POST"])
@matching_bp.route("/api/matching/find-schemes", methods=["POST"])
def api_find_schemes():
    data = request.get_json(silent=True) or {}
    user_id = session.get("user_id")

    # Prefer profile passed in body, fallback to saved profile if authenticated
    profile = data.get("profile") or data.get("profile_data")
    if not profile and user_id:
        profile = get_user_profile(user_id)

    if not profile:
        return jsonify({"success": False, "error": "Profile details required for matching."}), 400

    schemes_with_rules = get_all_schemes(active_only=True)
    ranked = rank_and_match_schemes(profile, schemes_with_rules)

    # Persist match results if user is authenticated and has given consent
    if user_id:
        u = fetch_one("SELECT consent_given FROM users WHERE id = %s", (user_id,))
        if u and u.get("consent_given"):
            execute_query("DELETE FROM match_result WHERE user_id = %s", (user_id,))
            for item in ranked:
                execute_query(
                    """
                    INSERT INTO match_result (
                        user_id, scheme_id, match_score, eligibility_status,
                        matched_criteria_json, failed_criteria_json, missing_criteria_json,
                        explanation_summary
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        user_id, item["scheme_id"], item["match_score"], item["eligibility_status"],
                        json.dumps(item["matched_criteria"]), json.dumps(item["failed_criteria"]),
                        json.dumps(item["missing_criteria"]), item["explanation_summary"]
                    )
                )

    eligible = [r for r in ranked if r["eligibility_status"] == "Eligible"]
    partially_eligible = [r for r in ranked if r["eligibility_status"] == "Partially Eligible"]
    not_eligible = [r for r in ranked if r["eligibility_status"] == "Not Eligible"]

    return jsonify({
        "success": True,
        "total_evaluated": len(ranked),
        "total_qualifying": len(eligible) + len(partially_eligible),
        "eligible_count": len(eligible),
        "partially_eligible_count": len(partially_eligible),
        "not_eligible_count": len(not_eligible),
        "results": ranked
    }), 200


@matching_bp.route("/api/matching/results", methods=["GET"])
def api_get_saved_results():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "error": "Authentication required"}), 401

    rows = fetch_all(
        """
        SELECT mr.*, sm.scheme_code, sm.scheme_name, sm.scheme_name_hi,
               sm.scheme_description, sm.scheme_description_hi, sm.scheme_category,
               sm.authority_level, sm.ministry_or_org, sm.benefit_type,
               sm.max_benefit_amount, sm.subsidy_info, sm.application_deadline,
               sm.deadline_note, sm.official_url, sm.source_url, sm.verification_status,
               (SELECT COUNT(*) FROM saved_schemes ss WHERE ss.user_id = mr.user_id AND ss.scheme_id = mr.scheme_id) AS is_saved
        FROM match_result mr
        JOIN scheme_master sm ON sm.id = mr.scheme_id
        WHERE mr.user_id = %s
        ORDER BY FIELD(mr.eligibility_status, 'Eligible', 'Partially Eligible', 'Requires Clarification', 'Not Eligible'),
                 mr.match_score DESC
        """,
        (user_id,)
    )
    for r in rows:
        r["match_score"] = float(r["match_score"])
        r["max_benefit_amount"] = float(r["max_benefit_amount"])
        r["is_saved"] = bool(r["is_saved"])
        if isinstance(r.get("matched_criteria_json"), str):
            r["matched_criteria"] = json.loads(r["matched_criteria_json"])
        if isinstance(r.get("failed_criteria_json"), str):
            r["failed_criteria"] = json.loads(r["failed_criteria_json"])
        if isinstance(r.get("missing_criteria_json"), str):
            r["missing_criteria"] = json.loads(r["missing_criteria_json"])

    return jsonify({"success": True, "count": len(rows), "results": rows}), 200


@matching_bp.route("/api/matching/results/<int:scheme_id>", methods=["GET"])
def api_get_single_result(scheme_id: int):
    user_id = session.get("user_id")
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        return jsonify({"success": False, "error": "Scheme not found"}), 404

    match_record = None
    if user_id:
        match_record = fetch_one(
            "SELECT * FROM match_result WHERE user_id = %s AND scheme_id = %s",
            (user_id, scheme_id)
        )
        if match_record:
            match_record["match_score"] = float(match_record["match_score"])
            if isinstance(match_record.get("matched_criteria_json"), str):
                match_record["matched_criteria"] = json.loads(match_record["matched_criteria_json"])
            if isinstance(match_record.get("failed_criteria_json"), str):
                match_record["failed_criteria"] = json.loads(match_record["failed_criteria_json"])

    return jsonify({"success": True, "scheme": scheme, "match_evaluation": match_record}), 200
