# import_questions.py
import sqlite3
import json

def import_questions(db_path="cyberquiz.db", json_path="data/questions.json"):
    """Importa domande da JSON nel database SQLite."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    for q in questions:
        cursor.execute("""
            INSERT INTO questions (category, difficulty, question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q['category'],
            q['difficulty'],
            q['question'],
            q['options']['A'],
            q['options']['B'],
            q['options']['C'],
            q['options']['D'],
            q['answer']
        ))

    conn.commit()
    conn.close()
    print(f"Inserite {len(questions)} domande nel database!")