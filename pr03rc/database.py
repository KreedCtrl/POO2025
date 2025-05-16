import tkinter as tk
from tkinter import messagebox
import sqlite3

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionare Studenti")

        tk.Label(root, text="Nume").grid(row=0, column=0)
        self.entry_nume = tk.Entry(root)
        self.entry_nume.grid(row=0, column=1)

        tk.Label(root, text="Prenume").grid(row=1, column=0)
        self.entry_prenume = tk.Entry(root)
        self.entry_prenume.grid(row=1, column=1)

        tk.Label(root, text="Varsta").grid(row=2, column=0)
        self.entry_varsta = tk.Entry(root)
        self.entry_varsta.grid(row=2, column=1)

        tk.Label(root, text="Media").grid(row=3, column=0)
        self.entry_media = tk.Entry(root)
        self.entry_media.grid(row=3, column=1)

        # Butoane
        tk.Button(root, text="Adaugă student", command=self.adauga_student).grid(row=4, column=0, pady=10)
        tk.Button(root, text="Afisează studenti", command=self.afiseaza_studenti).grid(row=4, column=1)

        # TextBox pentru afișare
        self.text_afisare = tk.Text(root, width=50, height=10)
        self.text_afisare.grid(row=5, column=0, columnspan=2, pady=10)

        self.creeaza_tabel()

    def creeaza_tabel(self):
        con = sqlite3.connect("studenti.db")
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS studenti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nume TEXT,
                prenume TEXT,
                varsta INTEGER,
                media REAL
            )
        """)
        con.commit()
        con.close()

    def adauga_student(self):
        nume = self.entry_nume.get()
        prenume = self.entry_prenume.get()
        varsta = self.entry_varsta.get()
        media = self.entry_media.get()

        # Validare simplă
        if not nume or not prenume:
            messagebox.showerror("Eroare", "Introduceti numele si prenumele.")
            return
        try:
            varsta = int(varsta)
            media = float(media)
            if media < 1 or media > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Eroare", "Varsta trebuie să fie un numar, iar media între 1 și 10.")
            return

        # Inserare în BD
        con = sqlite3.connect("studenti.db")
        cur = con.cursor()
        cur.execute("INSERT INTO studenti (nume, prenume, varsta, media) VALUES (?, ?, ?, ?)",
                    (nume, prenume, varsta, media))
        con.commit()
        con.close()

        messagebox.showinfo("Succes", "Student adaugat cu succes.")
        self.entry_nume.delete(0, tk.END)
        self.entry_prenume.delete(0, tk.END)
        self.entry_varsta.delete(0, tk.END)
        self.entry_media.delete(0, tk.END)

    def afiseaza_studenti(self):
        con = sqlite3.connect("studenti.db")
        cur = con.cursor()
        cur.execute("SELECT nume, prenume, varsta, media FROM studenti")
        studenti = cur.fetchall()
        con.close()

        self.text_afisare.delete(1.0, tk.END)
        for s in studenti:
            linie = f"Nume: {s[0]} {s[1]}, Varsta: {s[2]}, Media: {s[3]}\n"
            self.text_afisare.insert(tk.END, linie)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
