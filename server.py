import socket
import threading
import random

try:
    from tanki import constants
    NUM_MAPS = len(constants.MAPS)
except Exception:
    NUM_MAPS = 5


class GameServer:
    def __init__(self, host="0.0.0.0", port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.next_id = 1
        self.map_index = random.randint(0, NUM_MAPS - 1)  # mapa pre toto kolo

    def broadcast(self, msg, origin=None):
        for c in self.clients:
            if c != origin:
                try:
                    c.sendall((msg + "\n").encode())
                except Exception:
                    pass

    def handle_client(self, conn, addr):
        pid = self.next_id
        self.next_id += 1
        print(f"--- PRIPOJENÝ Hráč {pid}: {addr} ---")
        try:
            conn.sendall(f"ID:{pid}\nMAP:{self.map_index}\n".encode())  # ID + index mapy
        except Exception:
            return

        while True:
            try:
                data = conn.recv(1024)
            except Exception:
                break
            if not data:
                break
            self.broadcast(data.decode(errors="ignore").strip(), conn)

        print(f"--- ODPOJENÝ Hráč {pid} ---")
        if conn in self.clients:
            self.clients.remove(conn)
        conn.close()

    def start(self):
        print(f"SERVER BEŽÍ na porte 5555 (mapa {self.map_index})...")
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    GameServer().start()