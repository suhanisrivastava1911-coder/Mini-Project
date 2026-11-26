"""Application guidance service and export generator."""
from typing import Any, Dict, Optional
from backend.app.database.db import fetch_all, fetch_one


OFFICIAL_SAFEGUARDS = [
    {
        "title_en": "Official Portal Submission Only",
        "title_hi": "केवल आधिकारिक पोर्टल पर आवेदन करें",
        "detail_en": "AI Scheme Sahayak prepares your documentation and eligibility. Final submission must always take place on the designated official government portal.",
        "detail_hi": "यह प्लेटफॉर्म आपकी पात्रता और दस्तावेज़ तैयार कराता है। अंतिम आवेदन हमेशा सरकारी पोर्टल पर ही करें।"
    },
    {
        "title_en": "Beware of Fraudulent Middlemen",
        "title_hi": "फर्जी बिचौलियों से सावधान रहें",
        "detail_en": "Government portals like JanSamarth, PMEGP, Stand-Up Mitra, and Udyam never charge private commissions or request bank OTPs over the phone.",
        "detail_hi": "जनसमर्थ, PMEGP, स्टैंड-अप इंडिया और उद्यम पोर्टल कभी भी निजी कमीशन नहीं मांगते और न ही फोन पर OTP मांगते हैं।"
    },
    {
        "title_en": "Verify Certificate Validity Windows",
        "title_hi": "प्रमाण पत्रों की समय सीमा जांचें",
        "detail_en": "Ensure Income, Caste, and Domicile certificates are issued within your state's mandated validity timeframe before submission.",
        "detail_hi": "आवेदन से पहले सुनिश्चित करें कि आय, जाति और निवास प्रमाण पत्र वैध समयावधि के अंदर जारी किए गए हों।"
    }
]


def get_guidance_for_scheme(scheme_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve all guidance details, documents, and procedure steps."""
    scheme = fetch_one("SELECT * FROM scheme_master WHERE id = %s", (scheme_id,))
    if not scheme:
        return None
    docs = fetch_all("SELECT * FROM scheme_document WHERE scheme_id = %s ORDER BY sort_order ASC", (scheme_id,))
    steps = fetch_all("SELECT * FROM guide_step WHERE scheme_id = %s ORDER BY step_number ASC", (scheme_id,))

    return {
        "scheme": scheme,
        "documents": docs,
        "steps": steps,
        "safeguards": OFFICIAL_SAFEGUARDS
    }


def generate_printable_checklist_text(scheme_id: int, user_name: str = "Entrepreneur") -> str:
    """Generate plaintext / printable document checklist."""
    bundle = get_guidance_for_scheme(scheme_id)
    if not bundle:
        return ""
    scheme = bundle["scheme"]
    lines = [
        "=" * 70,
        "AI SCHEME SAHAYAK - OFFICIAL APPLICATION READINESS CHECKLIST",
        "=" * 70,
        f"Applicant Name: {user_name}",
        f"Scheme: {scheme['scheme_name']}",
        f"Ministry / Provider: {scheme['ministry_or_org']}",
        f"Official Portal: {scheme['official_url']}",
        f"Deadline: {scheme['application_deadline'] or scheme['deadline_note']}",
        "-" * 70,
        "REQUIRED DOCUMENTS CHECKLIST:",
    ]
    for idx, doc in enumerate(bundle["documents"], 1):
        mand = "[MANDATORY]" if doc["is_mandatory"] else "[OPTIONAL / AS APPLICABLE]"
        lines.append(f"  [ ] {idx}. {doc['document_name']} {mand}")
        if doc.get("description"):
            lines.append(f"       Note: {doc['description']}")
    lines.extend([
        "-" * 70,
        "APPLICATION PROCEDURE SUMMARY:",
    ])
    for step in bundle["steps"]:
        lines.append(f"  Step {step['step_number']}: {step['step_title']}")
        lines.append(f"    {step['step_description']}")
        if step.get("tips"):
            lines.append(f"    Tip: {step['tips']}")
    lines.extend([
        "-" * 70,
        "SAFEGUARDS & DISCLAIMER:",
        "- This platform does not directly disburse funds or claim automatic government approval.",
        "- Application submission occurs strictly on the official website listed above.",
        "=" * 70
    ])
    return "\n".join(lines)
