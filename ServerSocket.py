import socket
import threading
from CHandler import CHandler as ch

class ServerSocket:
    def __init__(self, host='0.0.0.0', port=7368):
        self.host = host
        self.port = port
        self.clients = []
        self.start_running = False
        self.start_thread = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

    def start(self): # starting the start thread
        if not self.start_running:
            self.start_thread = threading.Thread(target=self.run)
            self.start_thread.start()
            print("Server started")

    def run(self): # the start thread
        self.start_running = True
        self.server_socket.settimeout(1.0)  # Set timeout to allow periodic checks for shutdown

        while self.start_running:
            try:
                client_socket, addr = self.server_socket.accept()
                ch(client_socket, addr, self)
            except socket.timeout:
                continue
            except OSError:
                print("Server socket closed, stopping server.")
                break
    
    def stop(self):
        self.start_running = False
        self.server_socket.close()
        self.start_thread.join()
        print("Server socket closed")
    
    def broadcast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto("AudioControler discovery", ("255.255.255.255", 7368))
        print("Broadcast sent!")
        sock.close()

if __name__ == "__main__":
    server = ServerSocket()
    server.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop()
    print(server.clients)