"""Hinglish and multilingual normalization dictionary for Indian entrepreneur contexts."""
import re

# Common Hinglish and vernacular substitutions
HINGLISH_MAPPINGS = {
    # Genders
    r"\b(mahila|aurat|ladki|stree|nari)\b": "female",
    r"\b(purush|aadmi|ladka|mard)\b": "male",
    r"\b(kinnar|trans|transgender|tritiya panthi)\b": "transgender",

    # Categories
    r"\b(dalit|harijan|sc category|scheduled caste)\b": "sc",
    r"\b(adivasi|tribal|st category|scheduled tribe)\b": "st",
    r"\b(pichda|obc category|other backward)\b": "obc",
    r"\b(alpsankhyak|minority|muslim|christian|sikh|jain|buddhist)\b": "minority",
    r"\b(samanya|general category|open)\b": "general",
    r"\b(ews|aarthik roop se kamzor)\b": "ews",

    # Business Stages
    r"\b(shuru karna|nayi|shuruwat|start karna|planning|soch raha|idea hai)\b": "ideation",
    r"\b(recently started|abhi shuru kiya|kuch mahine hue|early stage|startup)\b": "startup",
    r"\b(purana business|chal raha hai|established|2 saal se|3 saal se|existing)\b": "existing msme",

    # Location
    r"\b(gaon|gramin|dehat|village)\b": "rural",
    r"\b(shahar|shehar|city|metro|town)\b": "urban",

    # Support types
    r"\b(karz|loan|rin|credit)\b": "loan",
    r"\b(subsidy|chhut|anudan)\b": "subsidy",
    r"\b(grant|sahayata rashi)\b": "grant",
    r"\b(training|prashikshan|seekhna)\b": "training",
    r"\b(toolkit|aujaar|machinery|machine)\b": "toolkit",
}


def normalize_text(text: str) -> str:
    """Normalize text by lowering, expanding contractions, and mapping vernacular tokens."""
    if not text:
        return ""
    norm = text.lower()
    norm = re.sub(r"[\r\n\t]+", " ", norm)
    # Standardize currency abbreviations
    norm = re.sub(r"₹|rs\.?|inr", "rupees ", norm)
    # Apply hinglish canonical substitutions
    for pattern, replacement in HINGLISH_MAPPINGS.items():
        norm = re.sub(pattern, replacement, norm, flags=re.IGNORECASE)
    return norm.strip()
