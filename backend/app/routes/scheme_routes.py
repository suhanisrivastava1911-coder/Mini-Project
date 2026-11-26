"""Public Scheme Exploration, Search, and Filtering API Routes."""
import re
from flask import Blueprint, jsonify, request
from backend.app.services.scheme_service import get_all_schemes, get_scheme_by_id, get_scheme_categories
from backend.app.utils.validators import sanitize_text

scheme_bp = Blueprint("scheme_bp", __name__)


@scheme_bp.route("/api/schemes", methods=["GET"])
@scheme_bp.route("/api/schemes/search", methods=["GET"])
def api_list_schemes():
    """Comprehensive multi-parameter search and filtering across all verified schemes."""
    q = sanitize_text(request.args.get("q", "") or request.args.get("search", ""), 120).lower().strip()
    auth = sanitize_text(request.args.get("authority", "") or request.args.get("level", ""), 40).strip()
    category = sanitize_text(request.args.get("category", "") or request.args.get("sector", ""), 80).strip()
    state = sanitize_text(request.args.get("state", ""), 80).strip()
    gender = sanitize_text(request.args.get("gender", ""), 40).strip()
    social_cat = sanitize_text(request.args.get("social_category", ""), 40).strip()
    funding = request.args.get("funding", None)
    benefit = sanitize_text(request.args.get("benefit_type", ""), 80).lower().strip()

    schemes = get_all_schemes(active_only=True)
    filtered = []

    for s in schemes:
        # 1. Authority level filter (Central, State, Private_CSR)
        if auth and auth.lower() != "all" and auth.lower() != "all authorities":
            s_auth = (s.get("authority_level") or "").lower()
            if auth.lower() not in s_auth:
                continue

        # 2. Sector / Category filter
        if category and category.lower() != "all" and category.lower() != "all sectors":
            s_sectors = (s.get("eligible_sectors") or s.get("scheme_category") or "").lower()
            if category.lower() not in s_sectors and "all" not in s_sectors:
                continue

        # 3. State domicile filter
        if state and state.lower() != "all" and state.lower() != "all india":
            s_states = (s.get("eligible_states") or "all india").lower()
            if "all india" not in s_states and state.lower() not in s_states:
                continue

        # 4. Gender filter
        if gender and gender.lower() != "all":
            s_genders = (s.get("eligible_genders") or "all").lower()
            if "all" not in s_genders and gender.lower() not in s_genders:
                continue

        # 5. Social Category filter
        if social_cat and social_cat.lower() != "all":
            s_cats = (s.get("eligible_categories") or "all").lower()
            if "all" not in s_cats and social_cat.lower() not in s_cats:
                continue

        # 6. Benefit type filter
        if benefit and benefit not in (s.get("benefit_type") or "").lower():
            continue

        # 7. Funding ceiling filter
        if funding:
            try:
                fund_val = float(funding)
                if s.get("max_benefit_amount") and float(s["max_benefit_amount"]) < fund_val:
                    continue
            except (ValueError, TypeError):
                pass

        # 8. Full-Text Search across name, hindi name, description, keywords, ministry, sector, and beneficiaries
        if q:
            # Tokenize search query to support multi-word search in any order
            tokens = [t for t in re.split(r"\s+", q) if t]
            searchable_corpus = (
                f"{s.get('scheme_name', '')} {s.get('scheme_name_hi', '')} "
                f"{s.get('scheme_code', '')} {s.get('scheme_description', '')} "
                f"{s.get('scheme_description_hi', '')} {s.get('ministry_or_org', '')} "
                f"{s.get('keywords', '')} {s.get('eligible_sectors', '')} "
                f"{s.get('eligible_states', '')} {s.get('target_beneficiary_groups', '')} "
                f"{s.get('benefit_type', '')}"
            ).lower()

            # Every token must match somewhere in the scheme record (case-insensitive & whitespace trimmed)
            match_all = True
            for token in tokens:
                if token not in searchable_corpus:
                    match_all = False
                    break
            if not match_all:
                continue

        filtered.append(s)

    return jsonify({
        "success": True,
        "count": len(filtered),
        "total_catalog": len(schemes),
        "schemes": filtered
    }), 200


@scheme_bp.route("/api/schemes/<int:scheme_id>", methods=["GET"])
def api_get_scheme(scheme_id: int):
    """Retrieve full details, required documents, and step-by-step guidance for a specific scheme."""
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        return jsonify({"success": False, "error": f"Scheme with ID {scheme_id} was not found."}), 404
    return jsonify({
        "success": True,
        "scheme": scheme,
        "documents": scheme.get("documents", []),
        "steps": scheme.get("guide_steps", [])
    }), 200


@scheme_bp.route("/api/schemes/filters", methods=["GET"])
def api_get_filters():
    """Return available filter options dynamically computed from verified catalog."""
    schemes = get_all_schemes(active_only=True)
    authorities = sorted(list({s.get("authority_level") for s in schemes if s.get("authority_level")}))
    states = sorted(list({state.strip() for s in schemes for state in (s.get("eligible_states") or "").split(",") if state.strip() and state.strip() != "All India"}))
    categories = get_scheme_categories()
    return jsonify({
        "success": True,
        "authorities": ["All Authorities"] + authorities,
        "states": ["All India"] + states,
        "categories": ["All Sectors"] + categories
    }), 200


@scheme_bp.route("/api/schemes/categories", methods=["GET"])
def api_get_categories():
    categories = get_scheme_categories()
    return jsonify({"success": True, "categories": categories}), 200
