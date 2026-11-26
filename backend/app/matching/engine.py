"""Intelligent Scheme Matching Engine (4-Stage Hybrid Architecture)."""
from typing import Any, Dict, List
from backend.app.matching.hard_filter import evaluate_hard_gate
from backend.app.matching.weighted_scorer import calculate_weighted_score


def evaluate_single_scheme(profile: Dict[str, Any], scheme_with_rule: Dict[str, Any]) -> Dict[str, Any]:
    """Execute 4-stage evaluation on a scheme."""
    # Stage 1: Hard Eligibility Filtering
    passed_hard_gate, mandatory_failures, matched_mandatory, missing_mandatory = evaluate_hard_gate(
        profile, scheme_with_rule
    )

    # Stage 2: Weighted Scoring
    raw_score, matched_weighted, failed_weighted = calculate_weighted_score(
        profile, scheme_with_rule
    )

    all_matched = matched_mandatory + [m for m in matched_weighted if m["criterion"] not in [x["criterion"] for x in matched_mandatory]]
    all_failed = [{"criterion": "Mandatory Eligibility", "detail": f} for f in mandatory_failures] + failed_weighted
    all_missing = missing_mandatory

    # Determine Status and Explainability
    if not passed_hard_gate:
        status = "Not Eligible"
        # Never present as eligible; cap score so it never outranks qualifying schemes
        final_score = round(min(raw_score, 40.0), 2)
        summary = "Not Eligible: Mandatory condition not satisfied: " + "; ".join(mandatory_failures[:2])
    elif all_missing:
        status = "Partially Eligible"
        final_score = round(min(raw_score, 94.0), 2)
        summary = f"Potentially Eligible ({final_score:.0f}% match). Verification needed: {all_missing[0]['detail']}"
    else:
        status = "Eligible"
        final_score = round(raw_score, 2)
        top_reasons = [m["criterion"] for m in all_matched[:3]]
        summary = f"Eligible ({final_score:.0f}% match): Satisfies all mandatory criteria including {', '.join(top_reasons)}."

    return {
        "scheme_id": scheme_with_rule["id"],
        "scheme_code": scheme_with_rule.get("scheme_code"),
        "scheme_name": scheme_with_rule.get("scheme_name"),
        "scheme_name_hi": scheme_with_rule.get("scheme_name_hi"),
        "scheme_description": scheme_with_rule.get("scheme_description"),
        "scheme_description_hi": scheme_with_rule.get("scheme_description_hi"),
        "scheme_category": scheme_with_rule.get("scheme_category"),
        "authority_level": scheme_with_rule.get("authority_level"),
        "ministry_or_org": scheme_with_rule.get("ministry_or_org"),
        "benefit_type": scheme_with_rule.get("benefit_type"),
        "max_benefit_amount": float(scheme_with_rule.get("max_benefit_amount", 0.0)),
        "subsidy_info": scheme_with_rule.get("subsidy_info"),
        "application_deadline": str(scheme_with_rule["application_deadline"]) if scheme_with_rule.get("application_deadline") else None,
        "deadline_note": scheme_with_rule.get("deadline_note"),
        "official_url": scheme_with_rule.get("official_url"),
        "source_url": scheme_with_rule.get("source_url"),
        "verification_status": scheme_with_rule.get("verification_status"),
        "last_verified_date": str(scheme_with_rule.get("last_verified_date", "")),
        "match_score": final_score,
        "eligibility_status": status,
        "matched_criteria": all_matched,
        "failed_criteria": all_failed,
        "missing_criteria": all_missing,
        "explanation_summary": summary,
        "applicable_benefits": scheme_with_rule.get("benefit_type", "") + (" - " + scheme_with_rule.get("subsidy_info", "") if scheme_with_rule.get("subsidy_info") else "")
    }


def rank_and_match_schemes(profile: Dict[str, Any], schemes_with_rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Stage 3 & 4: Rank all evaluated schemes."""
    status_order = {"Eligible": 0, "Partially Eligible": 1, "Requires Clarification": 2, "Not Eligible": 3}
    evaluated = [evaluate_single_scheme(profile, s) for s in schemes_with_rules]
    evaluated.sort(
        key=lambda item: (
            status_order.get(item["eligibility_status"], 4),
            -item["match_score"],
            0 if item["verification_status"] == "Verified" else 1,
            item["scheme_name"]
        )
    )
    return evaluated
