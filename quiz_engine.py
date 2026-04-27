# quiz_engine.py
import sqlite3
import time

DB_PATH = "cyberquiz.db"

def start_quiz(user_id, category=None, num_questions=5):
    """
    Avvia un quiz per l'utente.
    category: categoria specifica, se None prende domande casuali
    num_questions: numero di domande da somministrare
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Seleziona domande
    if category:
        cursor.execute("""
            SELECT id, question, option_a, option_b, option_c, option_d, correct_option 
            FROM questions 
            WHERE category=? 
            ORDER BY RANDOM() LIMIT ?
        """, (category, num_questions))
    else:
        cursor.execute("""
            SELECT id, question, option_a, option_b, option_c, option_d, correct_option 
            FROM questions 
            ORDER BY RANDOM() LIMIT ?
        """, (num_questions,))
    
    questions = cursor.fetchall()
    if not questions:
        print("Nessuna domanda disponibile per questa categoria.")
        conn.close()
        return

    print(f"\n--- Avvio quiz ({len(questions)} domande) ---")
    correct_count = 0
    wrong_count = 0
    start_time = time.time()

    # Loop sulle domande
    for idx, q in enumerate(questions, start=1):
        q_id, question, a, b, c, d, correct = q
        print(f"\nDomanda {idx}: {question}")
        print(f"A) {a}")
        print(f"B) {b}")
        print(f"C) {c}")
        print(f"D) {d}")

        while True:
            answer = input("Risposta (A/B/C/D): ").strip().upper()
            if answer in ("A","B","C","D"):
                break
            print("Input non valido, riprova.")

        is_correct = 1 if answer == correct else 0
        if is_correct:
            correct_count += 1
        else:
            wrong_count += 1

        # Salva risposta singola
        cursor.execute("""
            INSERT INTO attempt_answers (attempt_id, question_id, user_answer, is_correct)
            VALUES (?, ?, ?, ?)
        """, (0, q_id, answer, is_correct))  # placeholder attempt_id = 0

    end_time = time.time()
    duration = int(end_time - start_time)
    score = correct_count  # punti = numero corrette, puoi aggiungere pesi

    # Salva tentativo complessivo
    cursor.execute("""
        INSERT INTO attempts (user_id, score, correct_count, wrong_count, total_questions, duration_seconds)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, score, correct_count, wrong_count, len(questions), duration))
    attempt_id = cursor.lastrowid

    # Aggiorna attempt_answers con attempt_id corretto
    cursor.execute("""
        UPDATE attempt_answers SET attempt_id=? WHERE attempt_id=0 AND user_answer IS NOT NULL
    """, (attempt_id,))

    conn.commit()
    conn.close()

    print(f"\n--- Quiz terminato ---")
    print(f"Punteggio: {score}/{len(questions)}")
    print(f"Risposte corrette: {correct_count}")
    print(f"Risposte sbagliate: {wrong_count}")
    print(f"Tempo impiegato: {duration} secondi")