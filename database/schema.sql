-- =============================================================================
-- AI Scheme Sahayak: AI-Driven Scheme Matching for Marginalized Entrepreneurs
-- Problem Statement ID: 26092 | Theme: Smart Automation
-- Production MySQL 8.0 Relational Database Schema (16 Tables)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS ai_scheme_sahayak
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ai_scheme_sahayak;

SET FOREIGN_KEY_CHECKS = 0;

-- 1. Users Table (Core authentication, role & privacy consent)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_uuid VARCHAR(36) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    phone VARCHAR(20) NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    preferred_language VARCHAR(10) NOT NULL DEFAULT 'en',
    consent_given BOOLEAN NOT NULL DEFAULT FALSE,
    consent_version VARCHAR(20) NOT NULL DEFAULT '1.0',
    consent_timestamp TIMESTAMP NULL,
    reset_token VARCHAR(100) NULL,
    reset_token_expiry TIMESTAMP NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. User Profiles Table (Structured entrepreneur attributes & AES encrypted sensitive data)
CREATE TABLE IF NOT EXISTS user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    business_name VARCHAR(180) NOT NULL DEFAULT '',
    business_sector VARCHAR(80) NOT NULL,
    business_type VARCHAR(60) NOT NULL DEFAULT 'Proprietorship',
    business_stage ENUM('Ideation', 'Startup', 'Existing MSME') NOT NULL DEFAULT 'Startup',
    udyam_registered BOOLEAN NOT NULL DEFAULT FALSE,
    business_age_months INT NOT NULL DEFAULT 0,
    annual_turnover DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    household_income DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    funding_requirement DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    funding_purpose TEXT NULL,
    support_types JSON NULL,
    state VARCHAR(80) NOT NULL,
    district VARCHAR(80) NOT NULL DEFAULT '',
    location_type ENUM('Rural', 'Urban', 'Semi-Urban') NOT NULL DEFAULT 'Urban',
    gender ENUM('Female', 'Male', 'Transgender', 'Other', 'Prefer Not to Say') NOT NULL,
    social_category ENUM('SC', 'ST', 'OBC', 'Minority', 'General', 'EWS', 'Other') NOT NULL,
    age INT NULL,
    encrypted_sensitive_data TEXT NULL,
    raw_description TEXT NULL,
    profile_completion_percent INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_prof_sector (business_sector),
    INDEX idx_prof_state (state),
    INDEX idx_prof_category (social_category),
    INDEX idx_prof_gender (gender),
    CONSTRAINT fk_profile_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Scheme Master Table (Central, State, and CSR Schemes)
CREATE TABLE IF NOT EXISTS scheme_master (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_code VARCHAR(50) NOT NULL UNIQUE,
    scheme_name VARCHAR(220) NOT NULL,
    scheme_name_hi VARCHAR(255) NULL,
    scheme_description TEXT NOT NULL,
    scheme_description_hi TEXT NULL,
    scheme_category VARCHAR(80) NOT NULL,
    authority_level ENUM('Central', 'State', 'CSR') NOT NULL DEFAULT 'Central',
    ministry_or_org VARCHAR(200) NOT NULL,
    eligible_states VARCHAR(255) NOT NULL DEFAULT 'All India',
    target_beneficiary_groups VARCHAR(255) NOT NULL,
    benefit_type VARCHAR(100) NOT NULL,
    max_benefit_amount DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    subsidy_percentage DECIMAL(5, 2) NULL,
    subsidy_info VARCHAR(255) NULL,
    application_deadline DATE NULL,
    deadline_note VARCHAR(160) NOT NULL DEFAULT 'Ongoing / Rolling Basis',
    official_url VARCHAR(255) NOT NULL,
    source_url VARCHAR(255) NOT NULL,
    scheme_status ENUM('Active', 'Inactive', 'Expired') NOT NULL DEFAULT 'Active',
    verification_status ENUM('Verified', 'Requires Verification', 'Demo') NOT NULL DEFAULT 'Verified',
    last_verified_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_scheme_status (scheme_status),
    INDEX idx_scheme_auth (authority_level),
    INDEX idx_scheme_category (scheme_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Eligibility Rules Table (Hard gates & configurable weights)
CREATE TABLE IF NOT EXISTS eligibility_rule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_id INT NOT NULL UNIQUE,
    min_age INT NULL,
    max_age INT NULL,
    eligible_genders VARCHAR(120) NOT NULL DEFAULT 'All',
    gender_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_categories VARCHAR(160) NOT NULL DEFAULT 'All',
    category_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_states VARCHAR(255) NOT NULL DEFAULT 'All India',
    state_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    max_household_income DECIMAL(14, 2) NULL,
    income_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_sectors VARCHAR(255) NOT NULL DEFAULT 'All',
    sector_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_stages VARCHAR(160) NOT NULL DEFAULT 'All',
    stage_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    min_funding DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    max_funding DECIMAL(14, 2) NULL,
    funding_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    location_preference ENUM('Rural', 'Urban', 'All') NOT NULL DEFAULT 'All',
    requires_udyam BOOLEAN NOT NULL DEFAULT FALSE,
    keywords VARCHAR(255) NOT NULL DEFAULT '',
    special_criteria TEXT NULL,
    -- Configurable Weights (Default summing to 100)
    weight_category DECIMAL(5, 2) NOT NULL DEFAULT 20.00,
    weight_gender DECIMAL(5, 2) NOT NULL DEFAULT 15.00,
    weight_state DECIMAL(5, 2) NOT NULL DEFAULT 15.00,
    weight_income DECIMAL(5, 2) NOT NULL DEFAULT 15.00,
    weight_sector DECIMAL(5, 2) NOT NULL DEFAULT 15.00,
    weight_stage DECIMAL(5, 2) NOT NULL DEFAULT 10.00,
    weight_funding DECIMAL(5, 2) NOT NULL DEFAULT 10.00,
    weight_location DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    weight_support DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_rule_scheme FOREIGN KEY (scheme_id) REFERENCES scheme_master (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Match Results Table (Persisted ranked recommendation records with explainability)
CREATE TABLE IF NOT EXISTS match_result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    scheme_id INT NOT NULL,
    match_score DECIMAL(5, 2) NOT NULL,
    eligibility_status ENUM('Eligible', 'Partially Eligible', 'Not Eligible', 'Requires Clarification') NOT NULL,
    matched_criteria_json JSON NOT NULL,
    failed_criteria_json JSON NOT NULL,
    missing_criteria_json JSON NOT NULL,
    explanation_summary TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_match_user (user_id),
    INDEX idx_match_score (user_id, match_score),
    CONSTRAINT fk_match_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_match_scheme FOREIGN KEY (scheme_id) REFERENCES scheme_master (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Scheme Documents Table (Document requirements per scheme)
CREATE TABLE IF NOT EXISTS scheme_document (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_id INT NOT NULL,
    document_name VARCHAR(160) NOT NULL,
    document_name_hi VARCHAR(200) NULL,
    description VARCHAR(255) NOT NULL DEFAULT '',
    is_mandatory BOOLEAN NOT NULL DEFAULT TRUE,
    document_category VARCHAR(60) NOT NULL DEFAULT 'Identity & Address',
    sort_order INT NOT NULL DEFAULT 1,
    INDEX idx_doc_scheme (scheme_id, sort_order),
    CONSTRAINT fk_doc_scheme FOREIGN KEY (scheme_id) REFERENCES scheme_master (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Guide Steps Table (Step-by-step application preparation guide)
CREATE TABLE IF NOT EXISTS guide_step (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_id INT NOT NULL,
    step_number INT NOT NULL,
    step_title VARCHAR(180) NOT NULL,
    step_title_hi VARCHAR(220) NULL,
    step_description TEXT NOT NULL,
    step_description_hi TEXT NULL,
    tips VARCHAR(255) NULL,
    official_action_url VARCHAR(255) NULL,
    INDEX idx_step_scheme (scheme_id, step_number),
    CONSTRAINT fk_step_scheme FOREIGN KEY (scheme_id) REFERENCES scheme_master (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Saved Schemes Table (Bookmarked schemes per user)
CREATE TABLE IF NOT EXISTS saved_schemes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    scheme_id INT NOT NULL,
    notes TEXT NULL,
    saved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_saved_scheme (user_id, scheme_id),
    CONSTRAINT fk_saved_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_saved_scheme FOREIGN KEY (scheme_id) REFERENCES scheme_master (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Application Checklists Table (User checklist progress tracker)
CREATE TABLE IF NOT EXISTS application_checklists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    scheme_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    progress_percent DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_scheme_checklist (user_id, scheme_id),
    CONSTRAINT fk_check_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_check_scheme FOREIGN KEY (scheme_id) REFERENCES scheme_master (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Checklist Items Table (Item-level completion tracking)
CREATE TABLE IF NOT EXISTS checklist_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    checklist_id INT NOT NULL,
    document_id INT NULL,
    item_name VARCHAR(200) NOT NULL,
    is_checked BOOLEAN NOT NULL DEFAULT FALSE,
    checked_at TIMESTAMP NULL,
    INDEX idx_item_checklist (checklist_id),
    CONSTRAINT fk_item_checklist FOREIGN KEY (checklist_id) REFERENCES application_checklists (id) ON DELETE CASCADE,
    CONSTRAINT fk_item_document FOREIGN KEY (document_id) REFERENCES scheme_document (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. Chat Sessions Table (Conversational AI sessions)
CREATE TABLE IF NOT EXISTS chat_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_uuid VARCHAR(36) NOT NULL UNIQUE,
    user_id INT NULL,
    language VARCHAR(10) NOT NULL DEFAULT 'en',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_chat_user (user_id),
    CONSTRAINT fk_chat_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. Chat Messages Table (Messages with extracted entities)
CREATE TABLE IF NOT EXISTS chat_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    sender ENUM('user', 'assistant', 'system') NOT NULL,
    message_text TEXT NOT NULL,
    extracted_entities_json JSON NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_msg_session (session_id),
    CONSTRAINT fk_msg_session FOREIGN KEY (session_id) REFERENCES chat_sessions (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. Notifications Table (Deadline alerts & updates)
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(180) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('deadline', 'system', 'match') NOT NULL DEFAULT 'system',
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    action_url VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notif_user (user_id, is_read),
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 14. Admin Users Table (Administrative authentication & role management)
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('super_admin', 'scheme_manager', 'auditor') NOT NULL DEFAULT 'scheme_manager',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 15. Audit Logs Table (Administrative audit trail)
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NULL,
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(60) NOT NULL,
    target_id INT NULL,
    details TEXT NULL,
    ip_address VARCHAR(45) NOT NULL DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_admin (admin_id),
    INDEX idx_audit_action (action),
    CONSTRAINT fk_audit_admin FOREIGN KEY (admin_id) REFERENCES admin_users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 16. Scheme Verification History Table (Verification logs)
CREATE TABLE IF NOT EXISTS scheme_verification_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_id INT NOT NULL,
    verified_by INT NULL,
    verification_status ENUM('Verified', 'Requires Verification', 'Demo') NOT NULL,
    notes TEXT NULL,
    verification_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_verif_scheme (scheme_id),
    CONSTRAINT fk_verif_scheme FOREIGN KEY (scheme_id) REFERENCES scheme_master (id) ON DELETE CASCADE,
    CONSTRAINT fk_verif_admin FOREIGN KEY (verified_by) REFERENCES admin_users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
