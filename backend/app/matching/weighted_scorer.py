"""Stage 2: Transparent Weighted Relevance Scoring."""
from typing import Any, Dict, List, Optional, Tuple


def _split_csv(val: Optional[str]) -> List[str]:
    if not val:
        return []
    return [item.strip() for item in str(val).split(",") if item.strip()]


def calculate_weighted_score(profile: Dict[str, Any], rule: Dict[str, Any]) -> Tuple[float, List[Dict[str, str]], List[Dict[str, str]]]:
    """Calculate match score using exact formula:
    Match Score = (Sum of matched applicable weights / Sum of applicable weights) * 100
    """
    matched_criteria: List[Dict[str, str]] = []
    failed_criteria: List[Dict[str, str]] = []

    sum_matched = 0.0
    sum_applicable = 0.0

    gender = (profile.get("gender") or "").strip()
    category = (profile.get("social_category") or "").strip()
    state = (profile.get("state") or "").strip()
    sector = (profile.get("business_sector") or profile.get("sector") or "").strip()
    stage = (profile.get("business_stage") or "").strip()
    income = profile.get("household_income") or profile.get("annual_income")
    funding = profile.get("funding_requirement")
    loc_type = (profile.get("location_type") or "").strip()

    # 1. Social Category Weight
    w_cat = float(rule.get("weight_category", 20.0))
    if w_cat > 0:
        sum_applicable += w_cat
        elig_cats = _split_csv(rule.get("eligible_categories", "All"))
        if "All" in elig_cats or (category and category in elig_cats):
            sum_matched += w_cat
            matched_criteria.append({"criterion": "Social Category Alignment", "detail": f"Category ({category or 'All'}) aligns with scheme target."})
        elif category:
            failed_criteria.append({"criterion": "Social Category", "detail": f"Category ({category}) is not explicitly targeted."})

    # 2. Gender Weight
    w_gen = float(rule.get("weight_gender", 15.0))
    if w_gen > 0:
        sum_applicable += w_gen
        elig_genders = _split_csv(rule.get("eligible_genders", "All"))
        if "All" in elig_genders or (gender and gender in elig_genders):
            sum_matched += w_gen
            matched_criteria.append({"criterion": "Gender Alignment", "detail": f"Gender ({gender or 'All'}) aligns with scheme."})
        elif gender:
            failed_criteria.append({"criterion": "Gender", "detail": f"Scheme focuses on {', '.join(elig_genders)}."})

    # 3. State Weight
    w_state = float(rule.get("weight_state", 15.0))
    if w_state > 0:
        sum_applicable += w_state
        elig_states = _split_csv(rule.get("eligible_states", "All India"))
        if "All India" in elig_states or "All" in elig_states or (state and state in elig_states):
            sum_matched += w_state
            matched_criteria.append({"criterion": "Geographic Alignment", "detail": f"State ({state or 'All India'}) is fully eligible."})
        elif state:
            failed_criteria.append({"criterion": "Geographic Domicile", "detail": f"Scheme operates in: {', '.join(elig_states)}."})

    # 4. Sector Weight
    w_sec = float(rule.get("weight_sector", 15.0))
    if w_sec > 0:
        sum_applicable += w_sec
        elig_sectors = _split_csv(rule.get("eligible_sectors", "All"))
        if "All" in elig_sectors or (sector and sector in elig_sectors):
            sum_matched += w_sec
            matched_criteria.append({"criterion": "Sector Alignment", "detail": f"Sector ({sector or 'General'}) is eligible."})
        elif sector:
            failed_criteria.append({"criterion": "Sector Target", "detail": f"Focused on {', '.join(elig_sectors)}."})

    # 5. Business Stage Weight
    w_stg = float(rule.get("weight_stage", 10.0))
    if w_stg > 0:
        sum_applicable += w_stg
        elig_stages = _split_csv(rule.get("eligible_stages", "All"))
        if "All" in elig_stages or (stage and stage in elig_stages):
            sum_matched += w_stg
            matched_criteria.append({"criterion": "Business Stage", "detail": f"Stage ({stage or 'General'}) fits scheme focus."})
        elif stage:
            failed_criteria.append({"criterion": "Business Stage", "detail": f"Scheme targets: {', '.join(elig_stages)}."})

    # 6. Income Alignment Weight
    w_inc = float(rule.get("weight_income", 15.0))
    if w_inc > 0:
        sum_applicable += w_inc
        max_inc = rule.get("max_household_income")
        if max_inc is None:
            sum_matched += w_inc
            matched_criteria.append({"criterion": "Income Criteria", "detail": "No upper income ceiling."})
        elif income is not None and float(income) <= float(max_inc):
            sum_matched += w_inc
            matched_criteria.append({"criterion": "Income Criteria", "detail": f"Income (₹{float(income):,.0f}) is within limit."})
        elif income is not None:
            failed_criteria.append({"criterion": "Income Ceiling", "detail": f"Income exceeds ₹{float(max_inc):,.0f}."})

    # 7. Funding Range Weight
    w_fund = float(rule.get("weight_funding", 10.0))
    if w_fund > 0:
        sum_applicable += w_fund
        min_f = float(rule.get("min_funding", 0.0))
        max_f = float(rule.get("max_funding")) if rule.get("max_funding") is not None else None
        if funding is not None:
            f_val = float(funding)
            if f_val >= min_f and (max_f is None or f_val <= max_f):
                sum_matched += w_fund
                matched_criteria.append({"criterion": "Funding Requirement", "detail": f"Requested ₹{f_val:,.0f} fits scheme range."})
            elif f_val < min_f:
                # Partial weight if request is close
                sum_matched += w_fund * 0.4
                failed_criteria.append({"criterion": "Funding Range", "detail": f"Requested amount is lower than scheme minimum (₹{min_f:,.0f})."})
            else:
                sum_matched += w_fund * 0.5
                failed_criteria.append({"criterion": "Funding Range", "detail": f"Requested amount exceeds standard cap (₹{max_f:,.0f})."})
        else:
            sum_matched += w_fund * 0.5

    # 8. Location (Rural/Urban) Alignment if configured
    w_loc = float(rule.get("weight_location", 0.0))
    if w_loc > 0:
        sum_applicable += w_loc
        pref = rule.get("location_preference", "All")
        if pref == "All" or (loc_type and loc_type == pref):
            sum_matched += w_loc
            matched_criteria.append({"criterion": "Location Preference", "detail": f"Fits {pref} focus."})
        else:
            failed_criteria.append({"criterion": "Location Preference", "detail": f"Preferred {pref} units."})

    final_score = (sum_matched / sum_applicable * 100.0) if sum_applicable > 0 else 0.0
    return round(min(100.0, max(0.0, final_score)), 2), matched_criteria, failed_criteria
