"""Input validation and sanitization utilities."""
import re
from typing import Any, Dict, List, Optional, Tuple

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

VALID_GENDERS = ("Female", "Male", "Transgender", "Other", "Prefer Not to Say")
VALID_CATEGORIES = ("SC", "ST", "OBC", "Minority", "General", "EWS", "Other")
VALID_STAGES = ("Ideation", "Startup", "Existing MSME")
VALID_LOCATIONS = ("Rural", "Urban", "Semi-Urban")
VALID_SECTORS = (
    "Manufacturing", "Services", "Trading", "Retail", "Food Processing",
    "Handicrafts", "Textiles", "Agri-Allied", "Dairy", "Technology",
    "Repair & Maintenance", "Other"
)
VALID_STATES = (
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir",
    "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Madhya Pradesh", "Maharashtra",
    "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal", "All India", "Other UT / State"
)


def sanitize_text(text: Any, max_len: int = 500) -> str:
    """Strip whitespace and dangerous control chars."""
    if text is None:
        return ""
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", str(text)).strip()
    return cleaned[:max_len]


def validate_email(email: str) -> bool:
    return bool(email and EMAIL_REGEX.match(email.strip()))


def parse_amount(val: Any) -> Optional[float]:
    if val is None or str(val).strip() == "":
        return None
    raw = str(val).replace(",", "").replace("₹", "").replace("Rs.", "").replace("Rs", "").strip()
    try:
        amt = float(raw)
        return round(amt, 2) if 0 <= amt <= 10_000_000_000 else None
    except ValueError:
        return None
