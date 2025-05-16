import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def genereaza_raport_pdf(nume_fisier="raport_studenti.pdf", media_minima=0, sortare_dupa="media", ordine="Descrescator"):
    con = sqlite3.connect("studenti.db")
    cur = con.cursor()

    query = f"SELECT id, nume, prenume, varsta, media FROM studenti WHERE media >= ? ORDER BY {sortare_dupa} {ordine}"
    cur.execute(query, (media_minima,))
    studenti = cur.fetchall()

    total_studenti = len(studenti)
    suma_medii = sum([s[4] for s in studenti])
    media_generala = round(suma_medii / total_studenti, 2) if total_studenti > 0 else 0

    # Validare nume fisier
    if not nume_fisier.lower().endswith(".pdf"):
        nume_fisier += ".pdf"
    nume_fisier = os.path.basename(nume_fisier)

    c = canvas.Canvas(nume_fisier, pagesize=A4)
    width, height = A4

    def scrie_antet(pagina):
        c.drawString(50, height - 50, f"Raport Studenti - Pagina {pagina}")
        c.drawString(50, height - 70, f"Generat la: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, height - 100, "Nr.")
        c.drawString(80, height - 100, "Nume")
        c.drawString(200, height - 100, "Prenume")
        c.drawString(320, height - 100, "Varsta")
        c.drawString(380, height - 100, "Media")

    y = height - 120
    nr_pagina = 1
    scrie_antet(nr_pagina)

    for i, student in enumerate(studenti, start=1):
        id, nume, prenume, varsta, media = student
        c.drawString(50, y, str(i))
        c.drawString(80, y, nume)
        c.drawString(200, y, prenume)
        c.drawString(320, y, str(varsta))
        c.drawString(380, y, f"{media:.2f}")
        y -= 20

        if y < 60:
            c.showPage()
            nr_pagina += 1
            y = height - 120
            scrie_antet(nr_pagina)

    if y < 100:
        c.showPage()
        nr_pagina += 1
        y = height - 120
        scrie_antet(nr_pagina)

    y -= 30
    c.drawString(50, y, f"Total Studenti: {total_studenti}")
    y -= 20
    c.drawString(50, y, f"Media generala: {media_generala:.2f}")

    c.save()
    messagebox.showinfo("Succes", f"Raport PDF generat: {nume_fisier}")


# Interfata
def interfata_raport():
    def generare():
        try:
            media_minima = float(entry_media.get())
        except ValueError:
            messagebox.showerror("Eroare", "Introduceti o valoare valida pentru media minima.")
            return

        nume_fisier = entry_fisier.get().strip()
        if not nume_fisier:
            messagebox.showerror("Eroare", "Introduceti un nume pentru fisierul PDF.")
            return

        criteriu = sortare_var.get()
        ordine = ordine_var.get()

        genereaza_raport_pdf(
            nume_fisier=nume_fisier,
            media_minima=media_minima,
            sortare_dupa=criteriu,
            ordine=ordine
        )

    root = tk.Tk()
    root.title("Generare Raport Studenti")

    tk.Label(root, text="Media minima:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_media = tk.Entry(root)
    entry_media.insert(0, "5")
    entry_media.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Sortare dupa:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    sortare_var = tk.StringVar(value="media")
    sortare_menu = ttk.Combobox(root, textvariable=sortare_var, values=["media", "varsta"], state="readonly")
    sortare_menu.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Ordine:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    ordine_var = tk.StringVar(value="Descrescator")
    ordine_menu = ttk.Combobox(root, textvariable=ordine_var, values=["Crescator", "Descrescator"], state="readonly")
    ordine_menu.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Nume fisier PDF:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_fisier = tk.Entry(root)
    entry_fisier.insert(0, "raport_studenti.pdf")
    entry_fisier.grid(row=3, column=1, padx=10, pady=5)

    btn_genereaza = tk.Button(root, text="Genereaza Raport", command=generare)
    btn_genereaza.grid(row=4, column=0, columnspan=2, pady=15)

    root.mainloop()


if __name__ == "__main__":
    interfata_raport()
