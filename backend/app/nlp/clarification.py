"""Clarification detection and bilingual conversational follow-up question generation."""
from typing import Any, Dict, List, Tuple

CLARIFICATION_PROMPTS = {
    "state": {
        "question_en": "Which Indian State or Union Territory is your business located in?",
        "question_hi": "आपका व्यवसाय किस राज्य या केंद्र शासित प्रदेश में स्थित है?",
        "suggestions": ["Uttar Pradesh", "Bihar", "Maharashtra", "Rajasthan", "Delhi"]
    },
    "gender": {
        "question_en": "What is your gender? (Certain schemes like Stand-Up India and Mahila Samriddhi Yojana have dedicated mandates for women entrepreneurs).",
        "question_hi": "आपका लिंग क्या है? (कुछ योजनाएं जैसे स्टैंड-अप इंडिया और महिला समृद्धि योजना महिलाओं के लिए विशेष रूप से बनाई गई हैं)।",
        "suggestions": ["Female", "Male", "Transgender", "Prefer Not to Say"]
    },
    "social_category": {
        "question_en": "Which social category do you belong to (SC, ST, OBC, Minority, EWS, General)?",
        "question_hi": "आप किस सामाजिक श्रेणी (SC, ST, OBC, अल्पसंख्यक, EWS, सामान्य) से संबंधित हैं?",
        "suggestions": ["SC", "ST", "OBC", "Minority", "General", "EWS"]
    },
    "sector": {
        "question_en": "What is your business sector (e.g. Food Processing, Textiles, Handicrafts, Manufacturing, Retail, Technology)?",
        "question_hi": "आपका व्यवसाय किस क्षेत्र में है (जैसे खाद्य प्रसंस्करण, सिलाई/वस्त्र, हस्तशिल्प, निर्माण, दुकान, तकनीक)?",
        "suggestions": ["Food Processing", "Textiles", "Handicrafts", "Manufacturing", "Retail", "Services"]
    },
    "business_stage": {
        "question_en": "What stage is your business currently in?",
        "question_hi": "आपका व्यवसाय अभी किस चरण में है?",
        "suggestions": ["Ideation (नया विचार)", "Startup (हाल ही में शुरू किया)", "Existing MSME (स्थापित व्यवसाय)"]
    },
    "funding_requirement": {
        "question_en": "Approximately how much financial funding or loan (in INR) do you require?",
        "question_hi": "आपको लगभग कितने रुपये के ऋण या वित्तीय सहायता की आवश्यकता है?",
        "suggestions": ["₹50,000", "₹1,50,000", "₹5,00,000", "₹10,00,000", "₹25,00,000"]
    },
    "household_income": {
        "question_en": "What is your approximate annual household income? (Certain concessional schemes have income caps).",
        "question_hi": "आपकी अनुमानित वार्षिक पारिवारिक आय कितनी है? (कुछ रियायती योजनाओं में आय सीमा होती है)।",
        "suggestions": ["Under ₹1.5 Lakh", "₹1.5 Lakh - ₹3 Lakh", "₹3 Lakh - ₹6 Lakh", "Above ₹6 Lakh"]
    }
}


def detect_missing_attributes(extracted_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify missing eligibility attributes and return structured questions."""
    missing = []
    keys_to_check = [
        "state", "gender", "social_category", "sector",
        "business_stage", "funding_requirement", "household_income"
    ]
    for key in keys_to_check:
        val = extracted_profile.get(key)
        if val is None or val == "":
            q_info = CLARIFICATION_PROMPTS.get(key, {})
            missing.append({
                "field": key,
                "question_en": q_info.get("question_en", f"Please provide {key}."),
                "question_hi": q_info.get("question_hi", f"कृपया {key} बताएं।"),
                "suggestions": q_info.get("suggestions", [])
            })
    return missing


def format_conversational_response(extracted: Dict[str, Any], missing: List[Dict[str, Any]], lang: str = "en") -> Tuple[str, List[str]]:
    """Format a polite conversational reply with extracted summary and follow-up."""
    is_hi = (lang == "hi")

    # If all critical fields present
    if not missing:
        if is_hi:
            msg = (
                "बहुत बढ़िया! मुझे आपके व्यवसाय की मुख्य जानकारी प्राप्त हो गई है। "
                f"राज्य: {extracted.get('state')}, श्रेणी: {extracted.get('social_category')}, "
                f"क्षेत्र: {extracted.get('sector')}, आवश्यकता: ₹{extracted.get('funding_requirement', 0):,.0f}। "
                "अब मैं आपके लिए सबसे उपयुक्त सरकारी योजनाएं खोज रहा हूँ..."
            )
        else:
            msg = (
                "Excellent! I have extracted your core business eligibility details: "
                f"State: {extracted.get('state')}, Category: {extracted.get('social_category')}, "
                f"Sector: {extracted.get('sector')}, Funding Need: ₹{extracted.get('funding_requirement', 0):,.0f}. "
                "Evaluating qualifying government schemes for you now..."
            )
        return msg, ["Find Matching Schemes", "Edit Profile", "Ask a Question"]

    # Pick the next most critical missing item to ask
    next_item = missing[0]
    suggestions = next_item.get("suggestions", [])

    if is_hi:
        salutation = "धन्यवाद! "
        if extracted.get("sector") or extracted.get("state"):
            salutation += f"मैंने दर्ज कर लिया है: {extracted.get('sector') or ''} {extracted.get('state') or ''}। "
        question = salutation + next_item["question_hi"]
    else:
        salutation = "Thank you! "
        if extracted.get("sector") or extracted.get("state"):
            salutation += f"I have noted: {extracted.get('sector') or ''} in {extracted.get('state') or ''}. "
        question = salutation + next_item["question_en"]

    return question, suggestions
