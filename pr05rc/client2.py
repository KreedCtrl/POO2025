import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os

HOST = '192.168.195.81'
PORT = 12345

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat LAN - Client")

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
        except ConnectionRefusedError:
            messagebox.showerror("Conexiune eșuată", f"Nu s-a putut conecta la {HOST}:{PORT}. Verifică dacă serverul rulează.")
            master.destroy()
            return

        self.chat_log = scrolledtext.ScrolledText(master, state='disabled')
        self.chat_log.pack(padx=10, pady=10)

        self.entry = tk.Entry(master, width=50)
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = tk.Button(master, text="Trimite", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)
        
        self.reply_btn = tk.Button(master, text="Răspunde", command=self.reply_to_message)
        self.reply_btn.pack(side=tk.LEFT)


        self.file_btn = tk.Button(master, text="Trimite fișier", command=self.send_file)
        self.file_btn.pack(side=tk.LEFT)

        self.last_message = ""
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def send_message(self):
        msg = self.entry.get()
        if msg:
            full_msg = f"Client-2: {msg}"
            self.sock.sendall(full_msg.encode())
            self.entry.delete(0, tk.END)

    def reply_to_message(self):
        if self.last_message:
            self.entry.insert(0, f"@{self.last_message}: ")

    def send_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as f:
                content = f.read()
            self.sock.sendall("/file:".encode())
            self.sock.sendall(filename.encode())
            self.sock.sendall(content)

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                self.last_message = data
                self.chat_log.config(state='normal')
                self.chat_log.insert(tk.END, data + "\n")
                self.chat_log.yview(tk.END)
                self.chat_log.config(state='disabled')
            except:
                break

if __name__ == '__main__':
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
