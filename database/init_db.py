"""Initialize MySQL schema, seed data, and ensure default demo entrepreneur and admin exist."""
import os
import sys
import uuid
import mysql.connector
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "ai_scheme_sahayak")


def run_sql_file(cursor, file_path):
    print(f"Executing {os.path.basename(file_path)}...")
    with open(file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    statements = []
    current = []
    for line in sql.splitlines():
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("--"):
            continue
        current.append(line)
        if line_clean.endswith(";"):
            statements.append("\n".join(current))
            current = []
    if current:
        statements.append("\n".join(current))

    for stmt in statements:
        if stmt.strip():
            cursor.execute(stmt)


def initialize():
    print(f"Connecting to MySQL server at {MYSQL_HOST}:{MYSQL_PORT} as {MYSQL_USER}...")
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset="utf8mb4"
        )
    except mysql.connector.Error as err:
        print(f"\n[ERROR] Could not connect to MySQL: {err}")
        print("Please ensure MySQL 8.0 is running and credentials in .env are configured.\n")
        sys.exit(1)

    cursor = conn.cursor()
    try:
        schema_path = os.path.join(BASE_DIR, "database", "schema.sql")
        seed_path = os.path.join(BASE_DIR, "database", "seed.sql")

        run_sql_file(cursor, schema_path)
        conn.commit()

        run_sql_file(cursor, seed_path)
        conn.commit()

        # Ensure demo user exists
        demo_email = "asha.devi@demo.local"
        cursor.execute("SELECT id FROM users WHERE email = %s", (demo_email,))
        row = cursor.fetchone()
        if not row:
            user_uuid = str(uuid.uuid4())
            pw_hash = generate_password_hash("DemoPass@123", method="pbkdf2:sha256:600000")
            cursor.execute(
                """
                INSERT INTO users (user_uuid, full_name, email, password_hash, role, preferred_language, consent_given, consent_version, consent_timestamp)
                VALUES (%s, %s, %s, %s, 'user', 'hi', TRUE, '1.0', CURRENT_TIMESTAMP)
                """,
                (user_uuid, "Asha Devi (Demo)", demo_email, pw_hash)
            )
            user_id = cursor.lastrowid
            cursor.execute(
                """
                INSERT INTO user_profiles (
                    user_id, business_name, business_sector, business_type, business_stage,
                    udyam_registered, business_age_months, annual_turnover, household_income,
                    funding_requirement, funding_purpose, support_types, state, district,
                    location_type, gender, social_category, age, raw_description, profile_completion_percent
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 100
                )
                """,
                (
                    user_id,
                    "Asha Handloom & Tailoring Unit",
                    "Textiles",
                    "Proprietorship",
                    "Startup",
                    True,
                    8,
                    180000.00,
                    180000.00,
                    120000.00,
                    "Need collateral-free micro loan for sewing machines and fabric raw materials",
                    '["Loan", "Subsidy", "Toolkit"]',
                    "Uttar Pradesh",
                    "Varanasi",
                    "Rural",
                    "Female",
                    "SC",
                    29,
                    "SC woman entrepreneur from Varanasi running an early stage tailoring and handloom unit."
                )
            )
            conn.commit()
            print(f"Created demo user: {demo_email} (Password: DemoPass@123)")

        print("\nDatabase initialization successfully completed!")
        cursor.execute("SELECT COUNT(*) FROM scheme_master;")
        scheme_cnt = cursor.fetchone()[0]
        print(f"Total active schemes in database: {scheme_cnt}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    initialize()
