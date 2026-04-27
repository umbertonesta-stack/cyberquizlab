# main.py
from db import create_tables

def main_menu():
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
            print("Funzione Login qui")
            # TODO: chiamare login()
        elif choice == "2":
            print("Funzione Registrazione qui")
            # TODO: chiamare register()
        elif choice == "3":
            print("Avvia Quiz - da implementare")
        elif choice == "4":
            print("Report personali - da implementare")
        elif choice == "5":
            print("Report globali - da implementare")
        elif choice == "6":
            print("Menu Admin - da implementare")
        elif choice == "0":
            print("Uscita...")
            break
        else:
            print("Scelta non valida, riprova.")

if __name__ == "__main__":
    # 1. Creiamo il database e le tabelle se non esistono
    create_tables()
    
    # 2. Avviamo il menu principale
    main_menu()