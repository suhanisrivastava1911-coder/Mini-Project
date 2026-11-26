# AI Scheme Sahayak - REST API Documentation

Problem Statement ID: **26092**  
Theme: **Smart Automation**  
Category: **Software**  

All API endpoints return JSON responses with standard HTTP status codes (`200 OK`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `503 Service Unavailable`).

---

## 1. System Health

### `GET /api/health`
Checks MySQL server connectivity, connection pool status, and returns the number of active schemes.
- **Response `200 OK`**:
```json
{
  "active_schemes_in_db": 12,
  "app_name": "AI Scheme Sahayak",
  "database": "MySQL 8.0",
  "message": "Connected to MySQL successfully.",
  "mysql_connected": true,
  "status": "healthy"
}
```

---

## 2. Authentication & Consent

### `POST /api/auth/register`
Creates a user account with explicit data collection consent.
- **Request Body**:
```json
{
  "name": "Ramesh Kumar",
  "email": "ramesh@example.com",
  "password": "Password@123",
  "phone": "9876543210",
  "preferred_language": "hi",
  "consent_data_collection": true
}
```
- **Response `201 Created`**:
```json
{
  "success": true,
  "message": "User registered successfully.",
  "user_id": 2
}
```

### `POST /api/auth/login`
Authenticates a user and starts a secure server session.
- **Request Body**:
```json
{
  "email": "asha.devi@demo.local",
  "password": "DemoPass@123"
}
```

### `GET /api/auth/me`
Retrieves currently authenticated user details or returns anonymous status.

### `POST /api/auth/logout`
Terminates the session.

---

## 3. NLP & Multilingual Processing

### `POST /api/nlp/extract`
Parses free-text or voice transcripts into structured entrepreneur profile attributes using rule-based multilingual NER and Hinglish token normalization.
- **Request Body**:
```json
{
  "text": "Main aurat hun, Varanasi UP se, handloom ka kaam hai, 2.5 lakh loan chahiye"
}
```
- **Response `200 OK`**:
```json
{
  "success": true,
  "extracted_profile": {
    "gender": "Female",
    "social_category": null,
    "state": "Uttar Pradesh",
    "district": "Varanasi",
    "business_sector": "Textiles & Handloom",
    "business_stage": "Ideation",
    "funding_requirement": 250000.0,
    "confidence_score": 66,
    "extraction_method": "Local Rule-Assisted NLP Pipeline"
  },
  "missing_attributes": [
    {
      "field": "social_category",
      "question_en": "Which social category do you belong to (SC, ST, OBC, Minority, EWS, General)?",
      "question_hi": "आप किस सामाजिक श्रेणी से संबंधित हैं?"
    }
  ]
}
```

---

## 4. Conversational AI Assistant

### `POST /api/chat/message`
Processes chat messages, maintains session state, executes entity extraction, and provides polite follow-up clarification questions.
- **Request Body**:
```json
{
  "message": "Namaste, boutique factory lagani hai UP mein",
  "language": "hi"
}
```

---

## 5. Intelligent Scheme Matching Engine

### `POST /api/matching/find-schemes`
Executes the transparent 4-stage hybrid matching algorithm:
1. Hard Gate (Mandatory filters)
2. Weighted Relevance Scoring (0 - 100)
3. Ranking
4. Explainability breakdown

- **Request Body**:
```json
{
  "profile": {
    "gender": "Female",
    "social_category": "OBC",
    "state": "Uttar Pradesh",
    "district": "Varanasi",
    "business_sector": "Textiles & Handloom",
    "funding_requirement": 500000,
    "business_stage": "Ideation"
  }
}
```
- **Response `200 OK`**:
```json
{
  "success": true,
  "eligible_count": 5,
  "partially_eligible_count": 1,
  "not_eligible_count": 6,
  "results": [
    {
      "scheme_id": 1,
      "scheme_code": "PMEGP",
      "scheme_name": "Prime Minister Employment Generation Programme",
      "match_score": 96.0,
      "eligibility_status": "Eligible",
      "matched_criteria": [
        { "criterion": "Mandatory Eligibility", "detail": "All mandatory gates passed." },
        { "criterion": "Gender Alignment", "detail": "Eligible for 35% rural subsidy." }
      ],
      "explanation_summary": "Eligible (96% match): Satisfies all mandatory criteria."
    }
  ]
}
```

---

## 6. Public Schemes Directory

- `GET /api/schemes`: Lists all schemes with query parameters `?q=`, `?authority=`, `?category=`, `?state=`.
- `GET /api/schemes/<id>`: Returns full scheme metadata, eligibility rules, required document checklist, and step-by-step guidance.

---

## 7. Administrative API (Role Protected)

- `POST /api/admin/login`: Superadmin / Officer authentication.
- `GET /api/admin/dashboard/stats`: Returns count of schemes, registered entrepreneurs, match executions, and checklist progress.
- `GET /api/admin/schemes`: Full scheme CRUD listing.
- `POST /api/admin/schemes`: Create new scheme record.
- `DELETE /api/admin/schemes/<id>`: Soft-delete scheme from active repository.
- `GET /api/admin/audit-logs`: Audit trail of all administrative and verification actions.
