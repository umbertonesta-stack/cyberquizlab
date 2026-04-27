# db.py
import sqlite3

DB_FILE = "cyberquiz.db"

def get_connection():
    """Ritorna una connessione al database SQLite."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # consente di accedere ai risultati come dizionari
    return conn

def create_tables():
    """Esegue il file schema.sql per creare le tabelle."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        with open("schema.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
        conn.commit()
        print("Database e tabelle creati correttamente.")
    except Exception as e:
        print("Errore durante la creazione delle tabelle:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables()