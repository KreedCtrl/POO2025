import socket
import threading

HOST = '192.168.56.1' 
PORT = 12345

class ChatServer:
    def __init__(self, host, port):
        self.clients = []
        self.history = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()
        print(f"[SERVER] Pornit pe {host}:{port}")

    def handle_client(self, conn, addr):
        print(f"[SERVER] Conectat: {addr}")
        self.clients.append(conn)
        try:
            while True:
                data = conn.recv(1024).decode()
                if data.startswith("/file:"):
                    filename = conn.recv(1024).decode()
                    content = conn.recv(1024)
                    for c in self.clients:
                        c.sendall(f"File received: {filename}".encode())
                        c.sendall(content)
                else:
                    self.history.append(data)
                    for c in self.clients:
                        c.sendall(data.encode())
        except:
            print(f"[SERVER] Deconectat: {addr}")
            self.clients.remove(conn)
            conn.close()

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = ChatServer(HOST, PORT)
    server.run()
