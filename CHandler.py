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
        self.socket.settimeout(3.0)
        try:
            self.socket.sendall(b'\x02MAC:\x03\n') #request MAC address
            mac = self.readLine(self.socket)

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
    
    def readLine(self, sock):
        sock.settimeout(3.0)
        data = bytearray()
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                raise ConnectionError("Client disconnected")
            for b in chunk:
                if b == 0x02: #STX
                    data.clear()
                    continue
                if b == 0x03: #ETX
                    string =bytes(data).strip().decode('utf-8', errors='replace')
                    return string
                data.append(b)
