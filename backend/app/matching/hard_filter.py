"""Stage 1: Hard Eligibility Filtering (Mandatory Eligibility Gate)."""
from typing import Any, Dict, List, Optional, Tuple


def _split_csv(val: Optional[str]) -> List[str]:
    if not val:
        return []
    return [item.strip() for item in str(val).split(",") if item.strip()]


def evaluate_hard_gate(profile: Dict[str, Any], rule: Dict[str, Any]) -> Tuple[bool, List[str], List[Dict[str, str]], List[Dict[str, str]]]:
    """Evaluate mandatory constraints.
    Returns:
        (passed, mandatory_failures, matched_mandatory, missing_mandatory)
    """
    mandatory_failures: List[str] = []
    matched_mandatory: List[Dict[str, str]] = []
    missing_mandatory: List[Dict[str, str]] = []

    gender = (profile.get("gender") or "").strip()
    category = (profile.get("social_category") or "").strip()
    state = (profile.get("state") or "").strip()
    sector = (profile.get("business_sector") or profile.get("sector") or "").strip()
    stage = (profile.get("business_stage") or "").strip()
    age = profile.get("age")
    income = profile.get("household_income") or profile.get("annual_income")
    funding = profile.get("funding_requirement")
    has_udyam = bool(profile.get("udyam_registered") or profile.get("has_udyam"))

    scheme_code = rule.get("scheme_code", "")

    # Special Mandate for Stand-Up India (Must be SC/ST OR Woman, Greenfield)
    if scheme_code == "STANDUP-INDIA":
        is_sc_st = category in ("SC", "ST")
        is_woman = gender == "Female"
        if not gender and not category:
            missing_mandatory.append({"criterion": "Beneficiary Mandate (SC/ST or Woman)", "detail": "Specify gender and social category to confirm eligibility."})
        elif is_sc_st or is_woman:
            reasons = []
            if is_woman:
                reasons.append("Woman founder")
            if is_sc_st:
                reasons.append(f"{category} category founder")
            matched_mandatory.append({"criterion": "Beneficiary Mandate", "detail": "Eligible under: " + " & ".join(reasons)})
        else:
            msg = "Stand-Up India strictly requires applicant to be either a Woman OR belong to SC/ST category."
            mandatory_failures.append(msg)
    else:
        # Standard Gender Mandatory Check
        elig_genders = _split_csv(rule.get("eligible_genders", "All"))
        if rule.get("gender_mandatory") and "All" not in elig_genders:
            if not gender or gender == "Prefer Not to Say":
                missing_mandatory.append({"criterion": "Mandatory Gender", "detail": f"Scheme requires one of: {', '.join(elig_genders)}."})
            elif gender in elig_genders:
                matched_mandatory.append({"criterion": "Mandatory Gender", "detail": f"Gender ({gender}) matches scheme criteria."})
            else:
                mandatory_failures.append(f"Scheme restricted to {', '.join(elig_genders)} (Your profile: {gender}).")

        # Standard Category Mandatory Check
        elig_cats = _split_csv(rule.get("eligible_categories", "All"))
        if rule.get("category_mandatory") and "All" not in elig_cats:
            if not category:
                missing_mandatory.append({"criterion": "Mandatory Category", "detail": f"Scheme requires one of: {', '.join(elig_cats)}."})
            elif category in elig_cats:
                matched_mandatory.append({"criterion": "Mandatory Category", "detail": f"Category ({category}) is eligible."})
            else:
                mandatory_failures.append(f"Scheme restricted to {', '.join(elig_cats)} (Your profile: {category}).")

    # State Domicile Mandatory Check
    elig_states = _split_csv(rule.get("applicable_states") or rule.get("eligible_states", "All India"))
    state_is_mandatory = rule.get("state_mandatory", True if ("All India" not in elig_states and "All" not in elig_states) else False)
    if state_is_mandatory and "All India" not in elig_states and "All" not in elig_states:
        if not state:
            missing_mandatory.append({"criterion": "Mandatory State Domicile", "detail": f"Restricted to: {', '.join(elig_states)}."})
        elif state in elig_states:
            matched_mandatory.append({"criterion": "Mandatory State Domicile", "detail": f"State ({state}) is covered."})
        else:
            mandatory_failures.append(f"Restricted to entrepreneurs located in: {', '.join(elig_states)} (Your state: {state}).")

    # Income Ceiling Mandatory Check
    max_income = rule.get("max_household_income")
    if rule.get("income_mandatory") and max_income is not None:
        if income is None:
            missing_mandatory.append({"criterion": "Mandatory Income Limit", "detail": f"Annual household income must be <= ₹{float(max_income):,.0f}."})
        elif float(income) <= float(max_income):
            matched_mandatory.append({"criterion": "Mandatory Income Limit", "detail": f"Income (₹{float(income):,.0f}) is within limit (<= ₹{float(max_income):,.0f})."})
        else:
            mandatory_failures.append(f"Income (₹{float(income):,.0f}) exceeds scheme ceiling of ₹{float(max_income):,.0f}.")

    # Business Sector Mandatory Check
    elig_sectors = _split_csv(rule.get("eligible_sectors", "All"))
    if rule.get("sector_mandatory") and "All" not in elig_sectors:
        if not sector:
            missing_mandatory.append({"criterion": "Mandatory Sector", "detail": f"Eligible sectors: {', '.join(elig_sectors)}."})
        elif sector in elig_sectors:
            matched_mandatory.append({"criterion": "Mandatory Sector", "detail": f"Sector ({sector}) is supported."})
        else:
            mandatory_failures.append(f"Sector '{sector}' is not covered by this scheme (Eligible: {', '.join(elig_sectors)}).")

    # Business Stage Mandatory Check
    elig_stages = _split_csv(rule.get("eligible_stages", "All"))
    if rule.get("stage_mandatory") and "All" not in elig_stages:
        if not stage:
            missing_mandatory.append({"criterion": "Mandatory Stage", "detail": f"Supported stages: {', '.join(elig_stages)}."})
        elif stage in elig_stages:
            matched_mandatory.append({"criterion": "Mandatory Stage", "detail": f"Stage ({stage}) matches scheme target."})
        else:
            mandatory_failures.append(f"Scheme restricted to {', '.join(elig_stages)} (Your stage: {stage}).")

    # Age Limit Check
    min_age = rule.get("min_age")
    max_age = rule.get("max_age")
    if (min_age is not None or max_age is not None) and age is not None:
        try:
            a = int(age)
            if min_age is not None and a < int(min_age):
                mandatory_failures.append(f"Minimum applicant age is {min_age} years (Current age: {a}).")
            elif max_age is not None and a > int(max_age):
                mandatory_failures.append(f"Maximum applicant age is {max_age} years (Current age: {a}).")
            else:
                matched_mandatory.append({"criterion": "Age Requirement", "detail": f"Age ({a} yrs) is within range."})
        except ValueError:
            pass

    # Udyam Requirement Check
    if rule.get("requires_udyam") and not has_udyam:
        missing_mandatory.append({"criterion": "Udyam Registration", "detail": "Valid Udyam Registration Certificate is required before bank sanction."})

    passed = (len(mandatory_failures) == 0)
    return passed, mandatory_failures, matched_mandatory, missing_mandatory
