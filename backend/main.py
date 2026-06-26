"""
Hopify Backend — SQLite-based authentication and user management.
Supports both Patient and Doctor registration/login.
"""

import sqlite3
import hashlib
import os
import shutil
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "hopify.db")
DOCS_DIR = os.path.join(BASE_DIR, "doctor_documents")

os.makedirs(DOCS_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Database initialisation
# ---------------------------------------------------------------------------

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they do not exist."""
    conn = _get_conn()
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            full_name   TEXT    NOT NULL,
            phone       TEXT    NOT NULL,
            age         INTEGER NOT NULL,
            blood_group TEXT    NOT NULL,
            gender      TEXT    NOT NULL,
            address     TEXT    NOT NULL,
            created_at  TEXT    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT    UNIQUE NOT NULL,
            password        TEXT    NOT NULL,
            full_name       TEXT    NOT NULL,
            phone           TEXT    NOT NULL,
            age             INTEGER NOT NULL,
            blood_group     TEXT    NOT NULL,
            gender          TEXT    NOT NULL,
            address         TEXT    NOT NULL,
            specialization  TEXT    NOT NULL,
            nmc_doc_path    TEXT,
            created_at      TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _copy_document(src_path: str, username: str) -> str:
    """Copy an NMC document into the managed docs folder and return the stored path."""
    if not src_path or not os.path.isfile(src_path):
        return ""
    ext      = os.path.splitext(src_path)[1]
    dst_name = f"{username}_nmc{ext}"
    dst_path = os.path.join(DOCS_DIR, dst_name)
    shutil.copy2(src_path, dst_path)
    return dst_path


# ---------------------------------------------------------------------------
# Patient operations
# ---------------------------------------------------------------------------

def register_patient(username: str, password: str, full_name: str,
                     phone: str, age: int, blood_group: str,
                     gender: str, address: str) -> tuple[bool, str]:
    """Register a new patient. Returns (success, message)."""
    conn = _get_conn()
    try:
        conn.execute("""
            INSERT INTO patients
                (username, password, full_name, phone, age, blood_group, gender, address, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, _hash_password(password), full_name, phone,
              int(age), blood_group, gender, address,
              datetime.now().isoformat()))
        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' is already taken."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def login_patient(username: str, password: str) -> tuple[bool, dict | str]:
    """Authenticate a patient. Returns (success, row_dict | error_message)."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM patients WHERE username = ? AND password = ?",
            (username, _hash_password(password))
        ).fetchone()
        if row:
            return True, dict(row)
        return False, "Invalid username or password."
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Doctor operations
# ---------------------------------------------------------------------------

def register_doctor(username: str, password: str, full_name: str,
                    phone: str, age: int, blood_group: str,
                    gender: str, address: str, specialization: str,
                    nmc_doc_src: str = "") -> tuple[bool, str]:
    """Register a new doctor. Returns (success, message)."""
    stored_doc = _copy_document(nmc_doc_src, username)
    conn = _get_conn()
    try:
        conn.execute("""
            INSERT INTO doctors
                (username, password, full_name, phone, age, blood_group,
                 gender, address, specialization, nmc_doc_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, _hash_password(password), full_name, phone,
              int(age), blood_group, gender, address, specialization,
              stored_doc, datetime.now().isoformat()))
        conn.commit()
        return True, "Doctor registration successful!"
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' is already taken."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def login_doctor(username: str, password: str) -> tuple[bool, dict | str]:
    """Authenticate a doctor. Returns (success, row_dict | error_message)."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM doctors WHERE username = ? AND password = ?",
            (username, _hash_password(password))
        ).fetchone()
        if row:
            return True, dict(row)
        return False, "Invalid username or password."
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Generic login (tries both tables)
# ---------------------------------------------------------------------------

def login(username: str, password: str) -> tuple[bool, str, dict | str]:
    """
    Try doctor login first, then patient login.
    Returns (success, role, data)  role is 'doctor' | 'patient' | ''.
    """
    ok, data = login_doctor(username, password)
    if ok:
        return True, "doctor", data
    ok, data = login_patient(username, password)
    if ok:
        return True, "patient", data
    return False, "", "Invalid username or password."


# ---------------------------------------------------------------------------
# Initialise on import
# ---------------------------------------------------------------------------
init_db()
