"""
Unit tests for NLP components:
- Hinglish normalization
- Entity extraction (amount, category, gender, sector, location)
- Missing field clarification
"""

import pytest
from backend.app.nlp.hinglish_normalizer import normalize_text
from backend.app.nlp.entity_extractor import extract_entities_from_text
from backend.app.nlp.clarification import detect_missing_attributes, format_conversational_response


class TestHinglishNormalizer:
    def test_basic_normalization(self):
        text = "mujhe vyapar shuru karne ke liye loan chahiye"
        norm = normalize_text(text)
        assert "loan" in norm

    def test_number_words(self):
        norm = normalize_text("mahila aurat loan")
        assert "female" in norm


class TestEntityExtractor:
    def test_extract_female_entrepreneur_up(self):
        text = "Main aurat hun, Varanasi UP se, handloom ka kaam hai, 2.5 lakh loan chahiye"
        entities = extract_entities_from_text(text)
        assert entities.get("gender") == "Female"
        assert entities.get("state") == "Uttar Pradesh"
        assert entities.get("district") == "Varanasi"
        assert entities.get("funding_requirement") == 250000

    def test_extract_sc_artisan(self):
        text = "We belong to SC caste, traditional pottery artisan, needing 300000 tool finance"
        entities = extract_entities_from_text(text)
        assert entities.get("social_category") == "SC"
        assert entities.get("funding_requirement") == 300000

    def test_extract_crore_amount(self):
        text = "Manufacturing plant project cost 1.5 crore"
        entities = extract_entities_from_text(text)
        assert entities.get("funding_requirement") == 15000000

    def test_street_vendor(self):
        text = "Street vendor in Delhi needing 10 hazar loan"
        entities = extract_entities_from_text(text)
        assert entities.get("state") == "Delhi"
        assert entities.get("funding_requirement") == 10000


class TestClarificationEngine:
    def test_detect_missing_attributes(self):
        partial_profile = {
            "gender": "Female",
            "state": "Uttar Pradesh"
        }
        missing = detect_missing_attributes(partial_profile)
        fields = [m["field"] for m in missing]
        assert "funding_requirement" in fields
        assert "social_category" in fields

    def test_format_conversational_response(self):
        partial_profile = {"gender": "Female"}
        missing = detect_missing_attributes(partial_profile)
        reply, suggestions = format_conversational_response(partial_profile, missing, lang="hi")
        assert reply and len(reply) > 5
        assert isinstance(suggestions, list)
