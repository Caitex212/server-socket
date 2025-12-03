import threading
import socket

class CHandler:
    def __init__(self, socket, address, serversocket):
        self.socket = socket
        self.address = address
        self.serversocket = serversocket
        self.thread = threading.Thread(target=self.handle)
        self.thread.start()

    def handle(self):
        # a timeout for receiving the MAC
        self.socket.settimeout(3.0)

        try:
            self.socket.sendall(b'MAC\n')
            data = b""
            while not data.endswith(b'\n'):
                chunk = self.socket.recv(1024)
                if not chunk:
                    raise ConnectionError("Client disconnected")
                data += chunk

            mac = data.strip().decode('utf-8')

            client = {
                'socket': self.socket,
                'address': self.address,
                'mac': mac
            }

            self.serversocket.clients.append(client)
            print(f"New client connected: {self.address}, MAC: {mac}")

        except socket.timeout:
            print(f"Timed out waiting for MAC from {self.address}")
            self.socket.close()

        except Exception as e:
            print(f"Error handling client {self.address}: {e}")
            self.socket.close()
