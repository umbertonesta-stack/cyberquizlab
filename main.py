# main.py
import random
from db import create_tables, get_connection
from auth import register, login
from import_questions import import_questions

def start_quiz(user_id: int, category: str = None, num_questions: int = 5):
    """Avvia il quiz per l'utente corrente."""
    conn = get_connection()
    cursor = conn.cursor()

    # Carichiamo le domande
    if category:
        cursor.execute("SELECT * FROM questions WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()

    if not questions:
        print("Nessuna domanda disponibile per il quiz. Importa le domande o scegli un'altra categoria.")
        return

    quiz_questions = random.sample(questions, min(num_questions, len(questions)))

    correct_count = 0
    wrong_count = 0

    # Creiamo un tentativo nel DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attempts (user_id, total_questions)
        VALUES (?, ?)
    """, (user_id, len(quiz_questions)))
    attempt_id = cursor.lastrowid
    conn.commit()

    print("\n=== INIZIO QUIZ ===\n")

    for q in quiz_questions:
        print(f"Categoria: {q['category']} | Difficoltà: {q['difficulty']}")
        print(f"Domanda: {q['question']}")
        print(f"A) {q['option_a']}")
        print(f"B) {q['option_b']}")
        print(f"C) {q['option_c']}")
        print(f"D) {q['option_d']}")
        
        answer = input("Risposta (A/B/C/D): ").strip().upper()
        is_correct = 1 if answer == q['correct_option'] else 0

        if is_correct:
            correct_count += 1
        else:
            wrong_count += 1

        # Salviamo la risposta nel DB
        cursor.execute("""
            INSERT INTO attempt_answers (attempt_id, question_id, user_answer, is_correct)
            VALUES (?, ?, ?, ?)
        """, (attempt_id, q['id'], answer, is_correct))
        conn.commit()

    # Aggiorniamo il tentativo
    cursor.execute("""
        UPDATE attempts
        SET score = ?, correct_count = ?, wrong_count = ?
        WHERE id = ?
    """, (correct_count, correct_count, wrong_count, attempt_id))
    conn.commit()
    conn.close()

    print(f"\n=== FINE QUIZ ===")
    print(f"Risposte corrette: {correct_count}")
    print(f"Risposte errate: {wrong_count}")
    print(f"Punteggio: {correct_count}/{len(quiz_questions)}")

def main_menu():
    current_user_id = None
    current_username = None

    while True:
        print("\n=== CYBERQUIZ LAB ===")
        print("1) Login")
        print("2) Registrati")
        print("3) Avvia Quiz")
        print("4) Report personali")
        print("5) Report globali")
        print("6) Admin")
        print("0) Esci")

        choice = input("Seleziona un'opzione: ").strip()
        
        if choice == "1":
            user_id, username = login()
            if user_id != -1:
                current_user_id = user_id
                current_username = username
        elif choice == "2":
            register()
        elif choice == "3":
            if current_user_id:
                category = input("Scegli categoria (o premi Invio per casuale): ").strip() or None
                num_q = input("Quante domande vuoi? [5]: ").strip()
                num_q = int(num_q) if num_q.isdigit() else 5
                start_quiz(current_user_id, category, num_q)
            else:
                print("Devi fare il login prima di avviare il quiz.")
        elif choice == "4":
            if current_user_id:
                print(f"Report personali per {current_username} - funzione da implementare")
            else:
                print("Devi fare il login per vedere i tuoi report.")
        elif choice == "5":
            print("Report globali - funzione da implementare")
        elif choice == "6":
            # Menu Admin
            print("\n--- MENU ADMIN ---")
            print("1) Importa domande da JSON")
            print("2) Gestione domande (aggiungi/modifica/elimina)")
            print("0) Torna al menu principale")
            admin_choice = input("Seleziona un'opzione: ").strip()
            if admin_choice == "1":
                import_questions()
            elif admin_choice == "2":
                print("Gestione domande - da implementare")
            elif admin_choice == "0":
                continue
            else:
                print("Opzione Admin non valida.")
        elif choice == "0":
            print("Uscita...")
            break
        else:
            print("Scelta non valida, riprova.")

if __name__ == "__main__":
    create_tables()
    main_menu()