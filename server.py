import socket
import threading
import sys


HOST = "0.0.0.0"
PORT = 5555
MAX_PLAYERS = 4
BUFFER_SIZE = 1024
ENCODING = "utf-8"


class ClientHandler:
    def __init__(self, conn, addr, player_id):
        self.conn = conn
        self.addr = addr
        self.player_id = player_id
        self.name = f"Hráč {player_id}"


class GameServer:
    def __init__(self, host=HOST, port=PORT, max_players=MAX_PLAYERS):
        self.host = host
        self.port = port
        self.max_players = max_players

        self.server_socket = None
        self.clients = {}
        self.lock = threading.Lock()
        self.next_id = 1
        self.running = False

    def send_message(self, conn, message):
        try:
            conn.sendall((message + "\n").encode(ENCODING))
        except OSError:
            pass

    def broadcast(self, message, exclude_id=None):
        with self.lock:
            clients = list(self.clients.values())
        for client in clients:
            if client.player_id != exclude_id:
                self.send_message(client.conn, message)

    def assign_id(self):
        with self.lock:
            player_id = self.next_id
            self.next_id += 1
        return player_id

    def remove_client(self, player_id):
        with self.lock:
            client = self.clients.pop(player_id, None)
            online = len(self.clients)
        if client:
            try:
                client.conn.close()
            except OSError:
                pass
            print(f"[ODPOJENIE] {client.name} ({client.addr[0]}) sa odpojil. "
                  f"Online: {online}")

    def handle_client(self, conn, addr):
        player_id = self.assign_id()
        client = ClientHandler(conn, addr, player_id)

        with self.lock:
            self.clients[player_id] = client
            online = len(self.clients)

        print(f"[PRIPOJENIE] {client.name} sa pripojil z {addr[0]}:{addr[1]}. "
              f"Online: {online}")

        self.send_message(conn, f"ID:{player_id}")

        try:
            while self.running:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break

                for raw in data.decode(ENCODING, errors="ignore").splitlines():
                    raw = raw.strip()
                    if raw:
                        print(f"[{client.name}] >> {raw}")
        except (ConnectionResetError, OSError):
            pass
        finally:
            self.remove_client(player_id)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
        except OSError as e:
            print(f"[CHYBA] Server sa nepodarilo spustiť na "
                  f"{self.host}:{self.port} -> {e}")
            return

        self.server_socket.listen(self.max_players)
        self.server_socket.settimeout(1.0)
        self.running = True

        print(f"[SERVER] Spustený na {self.host}:{self.port}")
        print(f"[SERVER] Čakám na hráčov (max {self.max_players}). "
              f"Ukončenie: Ctrl+C")

        try:
            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break

                with self.lock:
                    full = len(self.clients) >= self.max_players
                if full:
                    print(f"[ODMIETNUTÉ] {addr[0]} – server je plný.")
                    self.send_message(conn, "FULL")
                    conn.close()
                    continue

                thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()
        except KeyboardInterrupt:
            print("\n[SERVER] Ukončovanie (Ctrl+C)...")
        finally:
            self.shutdown()

    def shutdown(self):
        self.running = False

        with self.lock:
            clients = list(self.clients.values())

        for client in clients:
            self.send_message(client.conn, "SERVER_CLOSED")
            try:
                client.conn.close()
            except OSError:
                pass

        with self.lock:
            self.clients.clear()

        if self.server_socket:
            try:
                self.server_socket.close()
            except OSError:
                pass

        print("[SERVER] Server bol korektne zatvorený.")


if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Neplatný port '{sys.argv[1]}', použijem {PORT}.")

    server = GameServer(port=port)
    server.start()