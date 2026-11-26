# AI Scheme Sahayak (एआई स्कीम सहायक)
### AI-Driven Scheme Matching for Marginalized Entrepreneurs

**Problem Statement ID:** 26092  
**Theme:** Smart Automation  
**Category:** Software  

---

## 🌟 Executive Summary

**AI Scheme Sahayak** is a full-stack, production-grade web application designed to eliminate information asymmetry, language barriers, and bureaucratic paperwork hurdles for marginalized and underserved entrepreneurs across India (including Women, SC/ST, OBC, Rural Artisans, and Street Vendors).

Using a transparent **4-stage intelligent matching engine**, multilingual voice/conversational AI processing (English, Hindi, Hinglish, and 10 regional Indian languages), and field-level AES-256 encryption, the application matches entrepreneurs to verified central, state, and private CSR schemes with zero hallucination.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, Vanilla ES6+ JavaScript, Responsive Mobile-First Design (tested at 360px), Progressive Web App (PWA), Service Workers, Web Speech API (Voice Recognition & TTS Synthesis) |
| **Backend** | Python 3.12, Flask 3.1, RESTful Blueprints, Rule-Based Named Entity Recognition (NER), Multilingual Hinglish Normalization |
| **Database** | MySQL 8.0 (16 Normalized Relational Tables), Foreign Keys, Parameterized Queries |
| **Security** | PBKDF2 Password Hashing, AES-256 Field Encryption (Fernet), Session-Based Auth, User Data Collection Consent |
| **Testing & Docs** | Pytest (100% Pass Rate across 21 Tests), Postman Collection v2.1, Markdown Docs |

---

## 🏗️ 4-Stage Scheme Matching Architecture

1. **Stage 1: Deterministic Hard Filter Gate**
   - Strictly validates mandatory criteria (e.g. Stand-Up India requires an SC/ST or Woman entrepreneur; UP MMYSY requires UP domicile; turnover/income caps).
   - If a mandatory rule fails, the scheme is marked as `Not Eligible` and **never** presented as qualifying.
2. **Stage 2: Transparent Weighted Scoring (0 - 100)**
   - Computes relevance based on configurable scheme weights:
     $$\text{Match Score} = \left(\frac{\sum \text{Matched Applicable Weights}}{\sum \text{Total Applicable Weights}}\right) \times 100$$
   - Factors: Sector alignment (25%), Social category fit (20%), Gender priority (15%), Location type (15%), Stage suitability (10%), Funding bracket (15%).
3. **Stage 3: Multi-Criteria Ranking**
   - Sorts results by: Status (`Eligible` > `Partially Eligible` > `Not Eligible`), Match Score (descending), Official Verification Status, Scheme Name.
4. **Stage 4: Explainability & Guidance Breakdown**
   - Detailed rationale explaining *why* the scheme matched, required document checklists with interactive checkboxes, step-by-step application guidance, and direct verified links to official government portals.

---

## 🏛️ Verified Official Scheme Knowledge Base

The platform includes **11 officially verified central/state schemes** and **1 clearly marked demonstration record**:
1. **PMEGP (Prime Minister Employment Generation Programme)** - Up to 35% capital subsidy for rural women/SC/ST/OBC in manufacturing/services.
2. **Stand-Up India Scheme** - ₹10 Lakh to ₹1 Crore collateral-free bank credit specifically mandated for SC/ST and Women entrepreneurs.
3. **PM Mudra Yojana (PMMY)** - Shishu, Kishore, and Tarun loans up to ₹10 Lakh for non-corporate micro enterprises.
4. **PM Vishwakarma Scheme** - Collateral-free enterprise credit up to ₹3 Lakh and ₹15,000 modern toolkit incentives for 18 traditional artisan trades.
5. **National SC-ST Hub (NSSH)** - Special subsidies and capacity-building for SC/ST micro and small enterprises.
6. **CGTMSE** - Credit Guarantee Fund Trust for Micro and Small Enterprises up to ₹5 Crore collateral-free coverage.
7. **Startup India Seed Fund Scheme (SISFS)** - Proof-of-concept and prototype grants up to ₹50 Lakh for early-stage innovators.
8. **NSFDC Mahila Samriddhi Yojana** - Micro-credit up to ₹1.4 Lakh at a concessional 4% interest rate for women from backward classes.
9. **PM SVANidhi** - Collateral-free working capital micro-loans (₹10,000 to ₹50,000) for urban and peri-urban street vendors with 7% interest subsidy.
10. **UP Mukhyamantri Yuva Swarojgar Yojana (MMYSY)** - Up to ₹25 Lakh for Uttar Pradesh youth with a 25% margin money subsidy.
11. **UP One District One Product (ODOP) Margin Money Scheme** - Specialized subsidies for traditional indigenous crafts in Uttar Pradesh.
12. **Demo / Synthetic Test Scheme** - Clearly labelled demonstration record for testing synthetic scoring rules.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- MySQL 8.0 Server (or MySQL-compatible server)
- Modern Web Browser (Chrome, Edge, or Firefox recommended for speech features)

### 2. Environment Setup
Clone the repository and activate the virtual environment:
```powershell
# In PowerShell:
.\.venv\Scripts\Activate.ps1
```

Install requirements (already pre-installed in workspace):
```powershell
pip install -r requirements.txt
```

### 3. Database Initialization (MySQL)
Create your MySQL database and run the schema and seed scripts:
```sql
CREATE DATABASE IF NOT EXISTS sahayak_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Run the automated Python database initializer:
```powershell
.\.venv\Scripts\python.exe database/init_db.py
```
*Note: If MySQL is not running locally, the application starts gracefully and alerts the user with status 503 degraded mode while allowing offline/cached operations.*

### 4. Running the Application
Start the Flask development server:
```powershell
.\.venv\Scripts\python.exe backend/run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Default Credentials

### Entrepreneur Demo Account
- **Email:** `asha.devi@demo.local`
- **Password:** `DemoPass@123`
- *Profile:* Asha Devi, Handloom & Textiles Artisan, Varanasi (UP), OBC Woman Entrepreneur.

### Officer / Admin Account
- **Username:** `superadmin`
- **Password:** `Admin@Sahayak2026`
- *Admin Portal:* Navigate to `http://127.0.0.1:5000/pages/admin_login.html`

---

## 🧪 Running Automated Tests

Run the full Pytest suite:
```powershell
.\.venv\Scripts\python.exe -m pytest -v
```
All **21 automated tests** cover:
- Hinglish text normalization and token replacement
- Entity extraction (amount parsing in lakh/crore/thousand, sector, location, gender, category)
- Missing attribute detection and bilingual follow-up generation
- Hard eligibility gate enforcement
- Weighted scoring calculation
- Multi-scheme ranking and sorting
- REST API integration endpoints (Mocked DB and Service layers)

---

## 📁 Repository Structure

```
├── backend/
│   ├── app/
│   │   ├── admin/             # Admin services, statistics & audits
│   │   ├── authentication/    # PBKDF2 hashing, session tokens, @login_required
│   │   ├── database/          # Connection pool, AES-256 Fernet crypto
│   │   ├── matching/          # 4-stage engine: hard filter, weighted scorer, ranker
│   │   ├── nlp/               # Hinglish normalizer, entity extractor, clarification
│   │   ├── routes/            # Flask REST API Blueprints (auth, chat, schemes, admin)
│   │   ├── services/          # Scheme, profile, chat, and checklist services
│   │   ├── utils/             # Structured logging, input sanitization
│   │   └── config.py          # Environment settings
│   ├── tests/                 # Pytest test suite (test_nlp, test_matching, test_api)
│   └── run.py                 # Application runner
├── database/
│   ├── schema.sql             # 16 normalized MySQL tables
│   ├── seed.sql               # 12 government & demo schemes with rules & steps
│   └── init_db.py             # Database initialization script
├── docs/
│   ├── API_DOCUMENTATION.md   # Complete REST API reference
│   ├── DATABASE_DOCUMENTATION.md # 16-table relational schema guide
│   └── postman_collection.json # Exportable Postman test collection
├── frontend/
│   ├── css/                   # Responsive mobile-first stylesheets (style.css, admin.css)
│   ├── js/                    # ES6 modules: i18n, voice, chat, matching, checklist, admin, pwa
│   ├── pages/                 # HTML templates (dashboard, chat, profile, schemes, admin)
│   ├── index.html             # High-converting landing page
│   ├── manifest.json          # PWA Web App Manifest
│   └── service-worker.js      # Offline caching and network resilience
├── .env.example               # Example configuration variables
├── requirements.txt           # Python dependencies
└── README.md                  # Project master documentation
```

---

## 🛡️ Privacy, Ethics & Safeguards

1. **Mandatory User Consent:** Personal information is collected only after the user actively ticks the consent checkbox.
2. **AES-256 Field Encryption:** Sensitive demographic and financial fields (`annual_income`, `caste_category`, `udyam_number`) are stored as ciphertext in MySQL.
3. **Anonymous Browsing:** Entrepreneurs can browse schemes and execute in-memory matching without creating an account.
4. **Data Deletion:** Full compliance with data portability — users can inspect or wipe their profiles anytime.
5. **Zero Commercial Data Sharing:** Entrepreneur profiles are never monetized, sold, or shared with third parties.
