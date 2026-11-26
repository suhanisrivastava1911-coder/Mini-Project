"""Rule-based Named Entity Recognition & Profile Extraction for Indian Entrepreneurs."""
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib import error as url_error, request as url_request

from backend.app.config import Config
from backend.app.nlp.hinglish_normalizer import normalize_text


INDIAN_STATES = {
    "Andhra Pradesh": ("andhra pradesh", "andhra", "vizag", "vijayawada", "आंध्र प्रदेश"),
    "Arunachal Pradesh": ("arunachal pradesh", "itanagar", "अरुणाचल प्रदेश"),
    "Assam": ("assam", "guwahati", "silchar", "असम"),
    "Bihar": ("bihar", "patna", "gaya", "muzaffarpur", "bhagalpur", "बिहार", "पटना"),
    "Chhattisgarh": ("chhattisgarh", "raipur", "bilaspur", "छत्तीसगढ़"),
    "Delhi": ("delhi", "new delhi", "ncr", "दिल्ली", "नई दिल्ली"),
    "Goa": ("goa", "panaji", "गोवा"),
    "Gujarat": ("gujarat", "ahmedabad", "surat", "vadodara", "rajkot", "गुजरात"),
    "Haryana": ("haryana", "gurugram", "gurgaon", "faridabad", "panipat", "हरियाणा"),
    "Himachal Pradesh": ("himachal pradesh", "shimla", "dharamshala", "हिमाचल प्रदेश"),
    "Jammu and Kashmir": ("jammu", "kashmir", "srinagar", "जम्मू", "कश्मीर"),
    "Jharkhand": ("jharkhand", "ranchi", "jamshedpur", "dhanbad", "झारखंड"),
    "Karnataka": ("karnataka", "bengaluru", "bangalore", "mysuru", "कर्नाटक"),
    "Kerala": ("kerala", "kochi", "thiruvananthapuram", "kozhikode", "केरल"),
    "Madhya Pradesh": ("madhya pradesh", "bhopal", "indore", "gwalior", "jabalpur", "mp", "मध्य प्रदेश"),
    "Maharashtra": ("maharashtra", "mumbai", "pune", "nagpur", "nashik", "aurangabad", "महाराष्ट्र"),
    "Manipur": ("manipur", "imphal", "मणिपुर"),
    "Meghalaya": ("meghalaya", "shillong", "मेघालय"),
    "Mizoram": ("mizoram", "aizawl", "मिजोरम"),
    "Nagaland": ("nagaland", "kohima", "नागालैंड"),
    "Odisha": ("odisha", "orissa", "bhubaneswar", "cuttack", "ओडिशा"),
    "Punjab": ("punjab", "ludhiana", "amritsar", "jalandhar", "पंजाब"),
    "Rajasthan": ("rajasthan", "jaipur", "jodhpur", "udaipur", "kota", "राजस्थान"),
    "Sikkim": ("sikkim", "gangtok", "सिक्किम"),
    "Tamil Nadu": ("tamil nadu", "chennai", "coimbatore", "madurai", "तमिलनाडु"),
    "Telangana": ("telangana", "hyderabad", "warangal", "तेलंगाना"),
    "Tripura": ("tripura", "agartala", "त्रिपुरा"),
    "Uttar Pradesh": (
        "uttar pradesh", "lucknow", "kanpur", "varanasi", "banaras", "kashi",
        "agra", "prayagraj", "allahabad", "meerut", "noida", "ghaziabad", "gorakhpur", "bareilly", "up",
        "उत्तर प्रदेश", "लखनऊ", "वाराणसी"
    ),
    "Uttarakhand": ("uttarakhand", "dehradun", "haridwar", "उत्तराखंड"),
    "West Bengal": ("west bengal", "kolkata", "howrah", "siliguri", "पश्चिम बंगाल")
}

DISTRICT_HINTS = {
    "Varanasi": ("varanasi", "banaras", "kashi", "वाराणसी"),
    "Lucknow": ("lucknow", "लखनऊ"),
    "Kanpur": ("kanpur", "कानपुर"),
    "Patna": ("patna", "पटना"),
    "Jaipur": ("jaipur", "जयपुर"),
    "Bhopal": ("bhopal", "भोपाल"),
    "Indore": ("indore", "इंदौर"),
    "Pune": ("pune", "पुणे"),
    "Mumbai": ("mumbai", "मुंबई"),
    "Gorakhpur": ("gorakhpur", "गोरखपुर"),
    "Prayagraj": ("prayagraj", "allahabad", "प्रयागराज"),
    "Agra": ("agra", "आगरा"),
    "Meerut": ("meerut", "मेरठ"),
}

SECTOR_KEYWORDS = {
    "Food Processing": (
        "food processing", "food", "bakery", "pickle", "achaar", "papad", "spice",
        "masala", "flour mill", "atta chakki", "tiffin", "sweet shop", "mithai",
        "dairy", "snack", "catering", "खाद्य", "अचार", "पापड़", "मसाला", "बेकरी"
    ),
    "Textiles": (
        "textile", "tailor", "tailoring", "stitching", "sewing", "boutique", "handloom",
        "weaving", "weaver", "embroidery", "garment", "saree", "chikankari", "silai",
        "सिलाई", "बुनाई", "हथकरघा", "कपड़ा", "वस्त्र"
    ),
    "Handicrafts": (
        "handicraft", "artisan", "pottery", "potter", "carpenter", "woodwork",
        "blacksmith", "bamboo", "craft", "cobbler", "goldsmith", "sculpture", "brassware",
        "हस्तशिल्प", "कारीगर", "शिल्प", "बढ़ई", "कुम्हार", "लोहार", "मोची"
    ),
    "Manufacturing": (
        "manufacturing", "factory", "unit", "production", "machinery", "soap",
        "candle", "agarbatti", "paper plate", "furniture", "plastic", "workshop",
        "विनिर्माण", "कारखाना", "उत्पादन", "मोमबत्ती", "अगरबत्ती"
    ),
    "Retail": (
        "retail", "shop", "kirana", "grocery", "dukaan", "store", "stationery",
        "medical store", "general store", "दुकान", "किराना"
    ),
    "Trading": (
        "trading", "wholesale", "distributor", "supplier", "dealer", "vendor",
        "street vendor", "hawker", "thela", "व्यापार", "थोक", "रेहड़ी", "ठेला"
    ),
    "Services": (
        "service", "coaching", "laundry", "dhobi", "cleaning", "transport",
        "cyber cafe", "csc", "printing", "delivery", "clinic", "सेवा", "धोबी"
    ),
    "Repair & Maintenance": (
        "repair", "mechanic", "garage", "welding", "electrician", "plumber",
        "mobile repair", "salon", "barber", "beauty parlour", "मरम्मत", "नाई", "सैलून"
    ),
    "Agri-Allied": (
        "poultry", "fishery", "beekeeping", "dairy farming", "goat farming",
        "mushroom", "murgi palan", "matsya palan", "pashupalan", "मधुमक्खी", "मत्स्य", "मुर्गी पालन"
    ),
    "Technology": (
        "technology", "software", "app", "website", "saas", "ai", "digital",
        "ecommerce", "startup", "edtech", "fintech", "सॉफ्टवेयर", "ऐप", "तकनीक"
    ),
}

SUPPORT_TYPES = {
    "Loan": ("loan", "credit", "rin", "karz", "ऋण", "लोन"),
    "Subsidy": ("subsidy", "margin money", "anudan", "सब्सिडी", "अनुदान"),
    "Grant": ("grant", "seed fund", "aid", "सीड ग्रांट"),
    "Training": ("training", "skill", "prashikshan", "कौशल", "प्रशिक्षण"),
    "Toolkit": ("toolkit", "machinery", "machine", "aujaar", "उपकरण", "टूलकिट"),
    "Mentorship": ("mentor", "mentorship", "guidance", "मार्गदर्शन"),
    "Market Linkage": ("market", "tender", "procurement", "exhibition", "बाज़ार"),
}


def _parse_indian_amount(raw_num: str, unit: str) -> float:
    num = float(raw_num.replace(",", ""))
    u = unit.lower().strip()
    if u in ("cr", "crore", "crores", "करोड़"):
        return round(num * 10_000_000, 2)
    if u in ("l", "lac", "lacs", "lakh", "lakhs", "लाख"):
        return round(num * 100_000, 2)
    if u in ("k", "thousand", "thousands", "hazar", "hazhar", "हजार", "हज़ार"):
        return round(num * 1_000, 2)
    return round(num, 2)


def _extract_amounts(text: str) -> Tuple[Optional[float], Optional[float]]:
    """Extract funding_requirement and household_income using distance from contextual markers."""
    annual_income: Optional[float] = None
    funding_req: Optional[float] = None

    amount_pattern = re.compile(
        r"(?:rupees|rs\.?|inr|₹)?\s*(\d[\d,]*(?:\.\d+)?)\s*(crores?|cr|lakhs?|lacs?|l|thousands?|hazar|hazhar|k|लाख|हजार|हज़ार|करोड़)?",
        re.IGNORECASE
    )

    income_markers = ("income", "earn", "salary", "family income", "household income", "turnover", "aay", "kamai", "आय", "कमाई", "सालाना")
    funding_markers = ("need", "loan", "fund", "funding", "capital", "require", "grant", "subsidy", "investment", "ऋण", "लोन", "चाहिए", "आवश्यकता")

    # Split into grammatical clauses avoiding splitting on decimals
    clauses = re.split(r"(?<!\d)[.,](?!\d)|[;।\n]|(?:\band\b|\bbut\b|\sऔर\s|\sतथा\s)", text, flags=re.IGNORECASE)

    for clause in clauses:
        lower_clause = clause.lower()
        for match in amount_pattern.finditer(clause):
            digits = match.group(1)
            unit = match.group(2) or ""
            raw_val = float(digits.replace(",", ""))
            if not unit and raw_val < 1000:
                continue
            if not unit and 1990 <= raw_val <= 2035 and "rupees" not in lower_clause and "rs" not in lower_clause:
                continue

            amount = _parse_indian_amount(digits, unit)

            def get_min_dist(markers):
                best = None
                for m in markers:
                    idx = lower_clause.find(m)
                    while idx != -1:
                        d = abs(idx - match.start())
                        if best is None or d < best:
                            best = d
                        idx = lower_clause.find(m, idx + 1)
                return best

            inc_dist = get_min_dist(income_markers)
            fund_dist = get_min_dist(funding_markers)

            if inc_dist is not None and (fund_dist is None or inc_dist <= fund_dist):
                if annual_income is None:
                    annual_income = amount
                elif funding_req is None:
                    funding_req = amount
            elif fund_dist is not None:
                if funding_req is None:
                    funding_req = amount
                elif annual_income is None:
                    annual_income = amount
            elif funding_req is None and amount >= 5000:
                funding_req = amount

    return annual_income, funding_req


def extract_entities_from_text(raw_text: str) -> Dict[str, Any]:
    """Parse text using rule-based multilingual NER."""
    norm = normalize_text(raw_text)

    # 1. State & District
    detected_state: Optional[str] = None
    detected_district: Optional[str] = None

    for state, aliases in INDIAN_STATES.items():
        for alias in aliases:
            if re.search(r"\b" + re.escape(alias) + r"\b", norm):
                detected_state = state
                break
        if detected_state:
            break

    for dist, aliases in DISTRICT_HINTS.items():
        for alias in aliases:
            if re.search(r"\b" + re.escape(alias) + r"\b", norm):
                detected_district = dist
                if not detected_state:
                    # Infer state for well-known cities
                    if dist in ("Varanasi", "Lucknow", "Kanpur", "Gorakhpur", "Prayagraj", "Agra", "Meerut"):
                        detected_state = "Uttar Pradesh"
                    elif dist == "Patna":
                        detected_state = "Bihar"
                    elif dist in ("Jaipur", "Jodhpur", "Kota", "Udaipur"):
                        detected_state = "Rajasthan"
                    elif dist in ("Bhopal", "Indore", "Gwalior"):
                        detected_state = "Madhya Pradesh"
                    elif dist in ("Pune", "Mumbai", "Nagpur"):
                        detected_state = "Maharashtra"
                break
        if detected_district:
            break

    # 2. Gender
    detected_gender: Optional[str] = None
    if re.search(r"\b(female|woman|women|mahila|lady|girl|stree)\b", norm):
        detected_gender = "Female"
    elif re.search(r"\b(male|man|men|purush|boy)\b", norm):
        detected_gender = "Male"
    elif re.search(r"\b(transgender|trans|kinnar)\b", norm):
        detected_gender = "Transgender"

    # 3. Social Category
    detected_category: Optional[str] = None
    if re.search(r"\b(sc|scheduled caste|dalit)\b", norm):
        detected_category = "SC"
    elif re.search(r"\b(st|scheduled tribe|adivasi)\b", norm):
        detected_category = "ST"
    elif re.search(r"\b(obc|other backward|pichda)\b", norm):
        detected_category = "OBC"
    elif re.search(r"\b(minority|muslim|christian|sikh|jain|buddhist|alpsankhyak)\b", norm):
        detected_category = "Minority"
    elif re.search(r"\b(ews|economically weaker)\b", norm):
        detected_category = "EWS"
    elif re.search(r"\b(general|open|samanya)\b", norm):
        detected_category = "General"

    # 4. Sector
    detected_sector: Optional[str] = None
    best_sector_hits = 0
    for sector, kws in SECTOR_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw in norm)
        if hits > best_sector_hits:
            best_sector_hits = hits
            detected_sector = sector

    # 5. Stage
    detected_stage: Optional[str] = None
    if re.search(r"\b(ideation|idea|shuru karna|planning|new unit|starting)\b", norm):
        detected_stage = "Ideation"
    elif re.search(r"\b(startup|early stage|recently started|few months)\b", norm):
        detected_stage = "Startup"
    elif re.search(r"\b(existing msme|existing|running for|established|scale)\b", norm):
        detected_stage = "Existing MSME"

    # 6. Location Type
    detected_loc: Optional[str] = None
    if re.search(r"\b(rural|village|gaon|gramin|dehat)\b", norm):
        detected_loc = "Rural"
    elif re.search(r"\b(urban|city|shehar|metro|town)\b", norm):
        detected_loc = "Urban"

    # 7. Financial amounts
    annual_income, funding_requirement = _extract_amounts(raw_text)

    # 8. Support Types
    support_found = []
    for s_type, kws in SUPPORT_TYPES.items():
        if any(kw in norm for kw in kws):
            support_found.append(s_type)
    if not support_found and funding_requirement:
        support_found.append("Loan")

    # 9. Udyam
    has_udyam = True if ("udyam" in norm or "उद्यम" in norm) else False

    # Calculate Confidence Score (0-100%)
    fields = [detected_state, detected_gender, detected_category, detected_sector, detected_stage, funding_requirement]
    filled = sum(1 for f in fields if f is not None)
    confidence = int((filled / len(fields)) * 100)

    extracted = {
        "state": detected_state,
        "district": detected_district or "",
        "gender": detected_gender,
        "social_category": detected_category,
        "sector": detected_sector,
        "business_stage": detected_stage,
        "location_type": detected_loc or "Urban",
        "household_income": annual_income,
        "funding_requirement": funding_requirement,
        "support_type": support_found,
        "udyam_registered": has_udyam,
        "confidence_score": confidence,
        "extraction_method": "Local Rule-Assisted NLP Pipeline"
    }

    # Optional external LLM refinement if configured
    if Config.OPENAI_API_KEY and raw_text.strip():
        try:
            llm_res = _call_external_llm_extractor(raw_text)
            if llm_res:
                for k, v in llm_res.items():
                    if v is not None and extracted.get(k) is None:
                        extracted[k] = v
                extracted["extraction_method"] = "Hybrid NLP (Local Engine + Configured AI API)"
        except Exception:
            pass

    return extracted


def _call_external_llm_extractor(text: str) -> Optional[Dict[str, Any]]:
    """Optional OpenAI API caller with strict timeout and fallback."""
    api_key = Config.OPENAI_API_KEY
    if not api_key:
        return None
    prompt = (
        "Extract Indian entrepreneur profile fields as JSON with keys: "
        "state, district, gender, social_category, sector, business_stage, "
        "location_type, household_income, funding_requirement, support_type (list). "
        f"Text: {text}"
    )
    body = json.dumps({
        "model": Config.OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "response_format": {"type": "json_object"}
    }).encode("utf-8")
    req = url_request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST"
    )
    try:
        with url_request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return json.loads(data["choices"][0]["message"]["content"])
    except Exception:
        return None
