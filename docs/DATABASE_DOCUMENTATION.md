# AI Scheme Sahayak - Database Schema Documentation

Database Engine: **MySQL 8.0**  
Charset: **utf8mb4**  
Collation: **utf8mb4_unicode_ci**  

The database architecture is composed of **16 normalized relational tables** enforcing foreign keys, indexes, and field-level encryption for sensitive user information.

---

## Entity Relationship Overview

```
users (1) ────< (1) user_profiles
  │
  ├────< (M) match_result >──── (1) scheme_master
  ├────< (M) saved_schemes >─── (1) scheme_master
  ├────< (M) application_checklists >─── (1) scheme_master
  │                │
  │                └───< (M) checklist_items
  ├────< (M) chat_sessions ───< (M) chat_messages
  └────< (M) notifications

scheme_master (1) ────< (1) eligibility_rule
      │
      ├────< (M) scheme_document
      ├────< (M) guide_step
      └────< (M) scheme_verification_history

admin_users (1) ────< (M) audit_logs
```

---

## 16 Table Specifications

### 1. `users`
Core user identity and consent records.
- `id` (INT PK AUTO_INCREMENT)
- `email` (VARCHAR(191) UNIQUE NOT NULL)
- `password_hash` (VARCHAR(255) NOT NULL, PBKDF2-SHA256)
- `name` (VARCHAR(120) NOT NULL)
- `phone` (VARCHAR(20))
- `preferred_language` (VARCHAR(10) DEFAULT 'en')
- `consent_given` (TINYINT(1) NOT NULL DEFAULT 0)
- `consent_timestamp` (DATETIME)
- `is_active` (TINYINT(1) DEFAULT 1)
- `role` (ENUM('user', 'admin') DEFAULT 'user')
- `created_at`, `updated_at` (DATETIME)

### 2. `user_profiles`
AES-256 encrypted fields for sensitive personal, financial, and demographic data.
- `id` (INT PK AUTO_INCREMENT)
- `user_id` (INT UNIQUE FK -> `users.id`)
- `gender` (VARCHAR(50))
- `social_category` (VARCHAR(50))
- `state` (VARCHAR(80))
- `district` (VARCHAR(80))
- `location_type` (ENUM('Rural', 'Urban', 'Semi-Urban'))
- `annual_income_encrypted` (VARCHAR(500))
- `funding_requirement` (DECIMAL(14,2))
- `business_name` (VARCHAR(150))
- `business_sector` (VARCHAR(100))
- `business_stage` (VARCHAR(60))
- `udyam_number_encrypted` (VARCHAR(500))

### 3. `scheme_master`
Master catalog of official and verified government and CSR schemes.
- `id` (INT PK AUTO_INCREMENT)
- `scheme_code` (VARCHAR(50) UNIQUE NOT NULL)
- `scheme_name` (VARCHAR(200) NOT NULL)
- `scheme_name_hi` (VARCHAR(255))
- `scheme_category` (VARCHAR(80))
- `authority_level` (ENUM('Central', 'State', 'Private_CSR'))
- `ministry_or_org` (VARCHAR(150))
- `max_benefit_amount` (DECIMAL(14,2))
- `subsidy_percentage` (DECIMAL(5,2))
- `is_demo` (TINYINT(1) DEFAULT 0)
- `verification_status` (ENUM('Verified', 'Pending', 'Deprecated'))
- `official_portal_url` (VARCHAR(500))

### 4. `eligibility_rule`
Configurable rules and weights for the 4-stage matching engine.
- `id` (INT PK AUTO_INCREMENT)
- `scheme_id` (INT UNIQUE FK -> `scheme_master.id`)
- `eligible_genders` (VARCHAR(100))
- `gender_mandatory` (TINYINT(1) DEFAULT 0)
- `eligible_categories` (VARCHAR(150))
- `category_mandatory` (TINYINT(1) DEFAULT 0)
- `eligible_states` (TEXT)
- `state_mandatory` (TINYINT(1) DEFAULT 0)
- `max_household_income` (DECIMAL(14,2))
- `income_mandatory` (TINYINT(1) DEFAULT 0)
- `weight_category` (DECIMAL(5,2) DEFAULT 20.00)
- `weight_gender` (DECIMAL(5,2) DEFAULT 15.00)
- `weight_sector` (DECIMAL(5,2) DEFAULT 25.00)

### 5. `match_result`
Evaluation history with score and explainability breakdown.
- `id` (INT PK AUTO_INCREMENT)
- `user_id` (INT FK -> `users.id`)
- `scheme_id` (INT FK -> `scheme_master.id`)
- `match_score` (DECIMAL(5,2))
- `eligibility_status` (ENUM('Eligible', 'Partially Eligible', 'Not Eligible'))
- `matched_criteria_json` (JSON)
- `failed_criteria_json` (JSON)
- `missing_criteria_json` (JSON)
- `explanation_summary` (TEXT)

### 6. `scheme_document`
Mandatory and optional document requirements per scheme.

### 7. `guide_step`
Sequential step-by-step application guidance.

### 8. `saved_schemes`
User bookmarks.

### 9. `application_checklists`
User progress tracker per scheme.

### 10. `checklist_items`
Checklist document items marked ready or pending.

### 11. `chat_sessions`
Conversational chat assistant sessions.

### 12. `chat_messages`
Chat message history with sender tags ('user'/'bot').

### 13. `notifications`
User alerts and deadline reminders.

### 14. `admin_users`
Officer and admin credentials with role-based access.

### 15. `audit_logs`
Security, update, and scheme verification logs.

### 16. `scheme_verification_history`
Verification audits and timestamped ministry reference changes.
