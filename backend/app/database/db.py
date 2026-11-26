"""MySQL Database connectivity with automatic local SQLite database resilience fallback.
When MySQL 8.0 is running, all queries run on MySQL.
When MySQL is offline, all queries run on a local SQLite store so registration, login, and scheme operations never crash.
"""
import os
import re
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple
import mysql.connector
from mysql.connector import Error as MySQLError
from backend.app.config import Config
from backend.app.utils.logger import logger

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
LOCAL_SQLITE_PATH = os.path.join(BASE_DIR, "database", "local_sahayak.db")

_USE_SQLITE = False
_MYSQL_TESTED = False


class DatabaseConnectionError(RuntimeError):
    """Raised when database server cannot be reached."""


def get_db_config() -> Dict[str, Any]:
    return {
        "host": Config.MYSQL_HOST,
        "port": Config.MYSQL_PORT,
        "user": Config.MYSQL_USER,
        "password": Config.MYSQL_PASSWORD,
        "database": Config.MYSQL_DATABASE,
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
        "use_unicode": True,
        "autocommit": False,
    }


def _init_sqlite_schema(conn: sqlite3.Connection):
    """Ensure SQLite schema exists for fallback operations."""
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT UNIQUE,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            preferred_language TEXT DEFAULT 'en',
            consent_given INTEGER DEFAULT 1,
            consent_version TEXT DEFAULT '1.0',
            consent_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            reset_token TEXT,
            reset_token_expiry DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            business_name TEXT,
            sector TEXT,
            business_stage TEXT,
            annual_turnover REAL DEFAULT 0,
            household_income REAL DEFAULT 0,
            funding_requirement REAL DEFAULT 0,
            gender TEXT,
            social_category TEXT,
            state TEXT,
            district TEXT,
            location_type TEXT DEFAULT 'Urban',
            is_rural INTEGER DEFAULT 0,
            is_differently_abled INTEGER DEFAULT 0,
            is_ex_serviceman INTEGER DEFAULT 0,
            udyam_registered INTEGER DEFAULT 0,
            support_types TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            is_active INTEGER DEFAULT 1,
            last_login DATETIME
        );

        CREATE TABLE IF NOT EXISTS saved_schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            scheme_id INTEGER NOT NULL,
            notes TEXT,
            saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, scheme_id)
        );

        CREATE TABLE IF NOT EXISTS application_checklists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            scheme_id INTEGER NOT NULL,
            title TEXT,
            progress_percent REAL DEFAULT 0.0,
            is_completed INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS checklist_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checklist_id INTEGER NOT NULL,
            document_id INTEGER,
            item_name TEXT,
            is_checked INTEGER DEFAULT 0,
            checked_at DATETIME
        );
    """)

    # Seed demo user and admin if not exist
    from werkzeug.security import generate_password_hash
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = 'asha.devi@demo.local'")
    if not cur.fetchone():
        pw_hash = generate_password_hash("DemoPass@123", method="pbkdf2:sha256:600000")
        cur.execute(
            "INSERT INTO users (user_uuid, full_name, email, phone, password_hash, role, preferred_language, consent_given) VALUES ('u-asha-001', 'Asha Devi', 'asha.devi@demo.local', '9876543210', ?, 'user', 'hi', 1)",
            (pw_hash,)
        )
        user_id = cur.lastrowid
        cur.execute(
            "INSERT INTO user_profiles (user_id, business_name, sector, business_stage, annual_turnover, household_income, funding_requirement, gender, social_category, state, district, location_type) VALUES (?, 'Devi Handlooms', 'Textiles & Handloom', 'Ideation', 150000, 240000, 250000, 'Female', 'OBC', 'Uttar Pradesh', 'Varanasi', 'Rural')",
            (user_id,)
        )

    cur.execute("SELECT id FROM admin_users WHERE username = 'superadmin'")
    if not cur.fetchone():
        admin_hash = generate_password_hash("Admin@Sahayak2026", method="pbkdf2:sha256:600000")
        cur.execute(
            "INSERT INTO admin_users (username, email, password_hash, role, is_active) VALUES ('superadmin', 'admin@sahayak.gov.in', ?, 'superadmin', 1)",
            (admin_hash,)
        )
    conn.commit()


def _get_sqlite_connection():
    os.makedirs(os.path.dirname(LOCAL_SQLITE_PATH), exist_ok=True)
    conn = sqlite3.connect(LOCAL_SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    _init_sqlite_schema(conn)
    return conn


@contextmanager
def get_db_connection():
    """Yield active MySQL database connection, or fallback to SQLite if MySQL is offline."""
    global _USE_SQLITE, _MYSQL_TESTED

    if not _USE_SQLITE:
        try:
            conn = mysql.connector.connect(**get_db_config())
            _MYSQL_TESTED = True
            yield conn
            if conn.is_connected():
                conn.commit()
            if conn.is_connected():
                conn.close()
            return
        except MySQLError:
            _USE_SQLITE = True

    # Fallback to local SQLite connection
    conn = _get_sqlite_connection()
    try:
        yield conn
        conn.commit()
    except Exception as exc:
        conn.rollback()
        raise exc
    finally:
        conn.close()


def _format_query_for_sqlite(query: str) -> str:
    """Convert MySQL-specific %s placeholders and syntax to SQLite equivalents."""
    # Convert %s to ?
    q = re.sub(r"%s", "?", query)
    q = re.sub(r"CURRENT_TIMESTAMP\(\)", "CURRENT_TIMESTAMP", q, flags=re.IGNORECASE)
    return q


def fetch_all(query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
    """Execute SELECT and return all rows as dicts."""
    with get_db_connection() as conn:
        if isinstance(conn, sqlite3.Connection):
            cursor = conn.cursor()
            try:
                cursor.execute(_format_query_for_sqlite(query), params or ())
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
            finally:
                cursor.close()
        else:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                return cursor.fetchall()
            finally:
                cursor.close()


def fetch_one(query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
    """Execute SELECT and return first row as a dict."""
    with get_db_connection() as conn:
        if isinstance(conn, sqlite3.Connection):
            cursor = conn.cursor()
            try:
                cursor.execute(_format_query_for_sqlite(query), params or ())
                row = cursor.fetchone()
                return dict(row) if row else None
            finally:
                cursor.close()
        else:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                return cursor.fetchone()
            finally:
                cursor.close()


def execute_query(query: str, params: Optional[Tuple[Any, ...]] = None) -> int:
    """Execute INSERT/UPDATE/DELETE and return lastrowid or rowcount."""
    with get_db_connection() as conn:
        if isinstance(conn, sqlite3.Connection):
            cursor = conn.cursor()
            try:
                cursor.execute(_format_query_for_sqlite(query), params or ())
                last_id = cursor.lastrowid
                row_count = cursor.rowcount
                return last_id if last_id else row_count
            finally:
                cursor.close()
        else:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or ())
                last_id = cursor.lastrowid
                row_count = cursor.rowcount
                return last_id if last_id else row_count
            finally:
                cursor.close()


def check_db_health() -> Tuple[bool, str, int]:
    """Test connection and return scheme count."""
    global _USE_SQLITE
    try:
        row = fetch_one("SELECT COUNT(*) AS total FROM users")
        count = row["total"] if row else 0
        db_type = "SQLite (Local Failover)" if _USE_SQLITE else "MySQL 8.0"
        return True, f"Connected to {db_type}.", count
    except Exception as exc:
        return False, str(exc), 0
