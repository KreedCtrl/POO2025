import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Redactor Text')
        
        self.text_area = tk.Text(self.window, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=tk.YES, fill=tk.BOTH)

        self.create_menu()
        self.create_styles()

        self.window.mainloop()

    def create_menu(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)

        edit_menu = tk.Menu(menu, tearoff=1)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Bold", command=lambda: self.apply_style("Bold"))
        edit_menu.add_command(label="Italic", command=lambda: self.apply_style("Italic"))
        edit_menu.add_command(label="Underline", command=lambda: self.apply_style("Underline"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Red", command=lambda: self.apply_style("Red"))
        edit_menu.add_command(label="Yellow", command=lambda: self.apply_style("Yellow"))
        edit_menu.add_command(label="Black", command=lambda: self.apply_style("Black"))
        edit_menu.add_command(label="Font 8", command=lambda: self.apply_style("Font8"))
        edit_menu.add_command(label="Font 12", command=lambda: self.apply_style("Font12"))
        edit_menu.add_command(label="Font 20", command=lambda: self.apply_style("Font20"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Căutare text", command=self.search_text)
        edit_menu.add_command(label="Înlocuire text", command=self.replace_text)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt",
                                          filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            try:
                self.window.title(f"Text Editor - {file}")
                self.text_area.delete(1.0, tk.END)
                with open(file, "r", encoding="utf-8") as f:
                    self.text_area.insert(tk.INSERT, f.read())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            try:
                with open(file, "w", encoding="utf-8") as f:
                    f.write(self.text_area.get(1.0, tk.END))
                self.window.title(f"Text Editor - {file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def apply_style(self, tag_name):
        try:
            self.text_area.tag_add(tag_name, "sel.first", "sel.last")
        except tk.TclError:
            messagebox.showinfo("Info", "Selectează textul pe care vrei să aplici stilul.")

    def create_styles(self):
        self.text_area.tag_configure("Bold", font=("Arial", 12, "bold"))
        self.text_area.tag_configure("Italic", font=("Arial", 12, "italic"))
        self.text_area.tag_configure("Underline", font=("Arial", 12, "underline"))
        self.text_area.tag_configure("Red", foreground="red")
        self.text_area.tag_configure("Yellow", foreground="yellow")
        self.text_area.tag_configure("Black", foreground="black")
        self.text_area.tag_configure("Font8", font=("Arial", 8))
        self.text_area.tag_configure("Font12", font=("Arial", 12))
        self.text_area.tag_configure("Font20", font=("Arial", 20))

    def search_text(self):
        search_term = simpledialog.askstring("Căutare", "Introdu textul căutat:")
        if not search_term:
            return
        direction = messagebox.askquestion("Direcție", "Vrei să cauți în sus?\n(Dacă apeși 'No', va căuta în jos.)")

        start_pos = self.text_area.index(tk.INSERT)

        if direction == "yes":  # Căutare în sus
            idx = self.text_area.search(search_term, start_pos, stopindex="1.0", backwards=True)
        else:  # Căutare în jos
            idx = self.text_area.search(search_term, start_pos, stopindex=tk.END)

        if idx:
            end_idx = f"{idx}+{len(search_term)}c"
            self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
            self.text_area.tag_add(tk.SEL, idx, end_idx)
            self.text_area.mark_set(tk.INSERT, end_idx)
            self.text_area.see(idx)
        else:
            messagebox.showinfo("Căutare", f"Textul '{search_term}' nu a fost găsit.")

    def replace_text(self):
        search_term = simpledialog.askstring("Înlocuire", "Textul de căutat:")
        if not search_term:
            return
        replace_with = simpledialog.askstring("Înlocuire", "Înlocuiește cu:")
        if replace_with is None:
            return

        content = self.text_area.get("1.0", tk.END)
        if search_term not in content:
            messagebox.showinfo("Înlocuire", f"Textul '{search_term}' nu a fost găsit.")
            return

        choice = messagebox.askyesno("Înlocuire", "Vrei să înlocuiești toate aparițiile?")
        if choice:
            new_content = content.replace(search_term, replace_with)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, new_content)
        else:
            start_pos = self.text_area.index(tk.INSERT)
            pos = self.text_area.search(search_term, index=start_pos, stopindex=tk.END)
            if pos:
                end_pos = f"{pos}+{len(search_term)}c"
                self.text_area.delete(pos, end_pos)
                self.text_area.insert(pos, replace_with)
                self.text_area.mark_set(tk.INSERT, f"{pos}+{len(replace_with)}c")
                self.text_area.see(f"{pos}+{len(replace_with)}c")
            else:
                messagebox.showinfo("Înlocuire", "Textul nu a fost găsit.")

if __name__ == "__main__":
    TextEditor()
