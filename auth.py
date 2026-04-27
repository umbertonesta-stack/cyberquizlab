# auth.py
import sqlite3
import hashlib
import secrets
from db import get_connection

def hash_password(password: str, salt: str) -> str:
    """Ritorna l'hash SHA-256 della password combinata con il salt."""
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

def register():
    """Registra un nuovo utente con username e password."""
    username = input("Inserisci username: ").strip()
    password = input("Inserisci password: ").strip()

    if not username or not password:
        print("Username e password non possono essere vuoti.")
        return

    # Generiamo un salt sicuro
    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, salt)
            VALUES (?, ?, ?)
        """, (username, password_hash, salt))
        conn.commit()
        print(f"Utente '{username}' registrato con successo!")
    except sqlite3.IntegrityError:
        print("Username già esistente. Scegli un altro username.")
    finally:
        conn.close()

def login() -> tuple[int, str] | tuple[int, None]:
    """
    Login utente.
    Ritorna (user_id, username) se successo, (-1, None) altrimenti.
    """
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash, salt FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        print("Login fallito. Username o password errati.")
        return -1, None

    user_id, password_hash_db, salt = user["id"], user["password_hash"], user["salt"]

    if not salt or not password_hash_db:
        # Utente creato senza salt o hash
        print("Errore: utente con password non sicura, resettare la password.")
        return -1, None

    if password_hash_db == hash_password(password, salt):
        print(f"Login effettuato con successo. Benvenuto {username}!")
        return user_id, username

    print("Login fallito. Username o password errati.")
    return -1, None