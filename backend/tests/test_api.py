"""
Integration tests for REST API endpoints using Flask test client:
- Static landing page
- NLP extraction and normalization
- Matching engine API
- Public health check and Anonymous session check
"""

from unittest.mock import patch
import pytest
from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key-123"
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"AI Scheme Sahayak" in response.data


def test_auth_me_anonymous(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    data = response.get_json()
    assert data["authenticated"] is False


def test_nlp_extract_endpoint(client):
    payload = {
        "text": "Main mahila hun, Varanasi UP se, boutique chalati hun aur 2.5 lakh loan chahiye"
    }
    response = client.post("/api/nlp/extract", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    profile = data["extracted_profile"]
    assert profile.get("gender") == "Female"
    assert profile.get("state") == "Uttar Pradesh"
    assert profile.get("district") == "Varanasi"
    assert profile.get("funding_requirement") == 250000


def test_nlp_normalize_endpoint(client):
    payload = {"text": "Mujhe 2 lakh loan chahiye"}
    response = client.post("/api/nlp/normalize", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "loan" in data["normalized"]


@patch("backend.app.routes.scheme_routes.get_all_schemes")
def test_schemes_api_public_mocked(mock_get_schemes, client):
    mock_get_schemes.return_value = [
        {
            "id": 1,
            "scheme_name": "PMEGP",
            "scheme_category": "Credit",
            "authority_level": "Central",
            "eligible_states": "All India",
            "benefit_type": "Subsidy",
            "scheme_description": "Prime Minister Employment Generation Programme",
            "ministry_or_org": "MSME"
        }
    ]
    response = client.get("/api/schemes")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["schemes"]) == 1
    assert data["schemes"][0]["scheme_name"] == "PMEGP"


@patch("backend.app.routes.matching_routes.get_all_schemes")
def test_matching_api_endpoint_mocked(mock_get_schemes, client):
    mock_get_schemes.return_value = [
        {
            "id": 1,
            "scheme_code": "PMEGP",
            "scheme_name": "PMEGP",
            "applicable_states": "All India",
            "eligible_genders": "All",
            "eligible_categories": "All",
            "eligible_sectors": "All",
            "max_benefit_amount": 5000000,
            "benefit_type": "Subsidy"
        }
    ]
    payload = {
        "profile": {
            "gender": "Female",
            "social_category": "OBC",
            "state": "Uttar Pradesh",
            "district": "Varanasi",
            "business_sector": "Textiles & Handloom",
            "funding_requirement": 500000
        }
    }
    response = client.post("/api/matching/find-schemes", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "results" in data
    assert len(data["results"]) > 0


@patch("backend.app.routes.chat_routes.process_user_message")
@patch("backend.app.routes.chat_routes.get_or_create_session")
def test_chat_message_endpoint_mocked(mock_get_session, mock_process_msg, client):
    mock_get_session.return_value = {"id": 1, "session_uuid": "sess-uuid-123"}
    mock_process_msg.return_value = {
        "reply": "Namaste! Aapki details note kar li gayi hain.",
        "extracted_profile": {"funding_requirement": 1000000, "state": "Gujarat"},
        "suggested_replies": ["Find Schemes", "Edit Profile"]
    }
    payload = {
        "session_id": "test_session_123",
        "message": "Mujhe 10 lakh loan chahiye manufacturing factory ke liye, Gujarat se hun",
        "language": "hinglish"
    }
    response = client.post("/api/chat/message", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "reply" in data
    assert data["extracted_profile"]["state"] == "Gujarat"
