import socket
import threading


class Network:
    def __init__(self, host="127.0.0.1", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.player_id = None
        self.map_index = None
        self.connected = False
        self.buffer = ""

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            self.connected = True
            threading.Thread(target=self.listen, daemon=True).start()
            print("Úspešne pripojené k serveru!")
            return True
        except Exception as e:
            print(f"Nepodarilo sa pripojiť: {e}")
            return False

    def listen(self):
        while self.connected:
            try:
                data = self.client.recv(1024).decode(errors="ignore")
            except Exception:
                break
            if not data:
                break
            self.buffer += data
            while "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)
                line = line.strip()
                if line.startswith("ID:"):
                    self.player_id = int(line[3:])
                elif line.startswith("MAP:"):
                    self.map_index = int(line[4:])
        self.connected = False

    def send(self, msg):
        try:
            self.client.sendall((msg + "\n").encode())
        except Exception:
            pass


if __name__ == "__main__":
    import time
    net = Network("127.0.0.1")
    if net.connect():
        time.sleep(0.5)  # počkaj, kým vlákno prijme dáta zo servera
        print("Moje ID:", net.player_id)
        print("Index mapy:", net.map_index)