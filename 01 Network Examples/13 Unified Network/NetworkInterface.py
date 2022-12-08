import socket
import threading
from ConnectionHandler import ConnectionHandler
from enum import Enum

class Role(Enum):
    SERVER = 1
    CLIENT = 2


class NetworkInterface:
    def __init__(self, host="127.0.0.1", port=50000, callbackHandler=None):
        self.role = None
        self.listener = None
        self.connections = []

        self.HOST = host
        self.PORT = port
        self.callbackHandler = callbackHandler

        self.socket = None
        self.count = 0
        self.running = True


    def startServer(self):
        if not self.role:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.HOST, self.PORT))
            self.role = Role.SERVER

            self.listener = threading.Thread(target=self.listen)
            self.listener.start()
            return True
        return False

    def listen(self):
        while self.running:
            # Set socket to listen for incoming connections, then block waiting for a connection
            self.socket.listen()

            conn, addr = self.socket.accept()

            conn.setblocking(False)
            self.count = self.count + 1
            ip, port = conn.getpeername()
            connection = ConnectionHandler(conn)
            self.connections.append((ip, port, connection))

            connection.process()
            self.callbackHandler(connection)

    def startClient(self):
        if not self.role:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.connect((self.HOST, self.PORT))

            ip, port = self.socket.getpeername()
            connection = ConnectionHandler(self.socket)
            connection.process()

            # internal handler for messages
            self.connections.append((ip, int(port), connection))
            self.role = Role.CLIENT

            return True
        return False

    def getMessage(self, ip=None, port=None):
        if self.role == Role.CLIENT:
           return self.connections[0][2].getMessage()
        elif self.role == Role.SERVER:
            for conn in self.connections:
                if conn[0] == ip and int(conn[1]) == port:
                    return self.connections[2].getMessage()
        else:
            return None

    def pushMessage(self, message, ip=None, port=None):
        if self.role == Role.CLIENT:
           self.connections[0][2].pushMessage(message)
        elif self.role == Role.SERVER:
            for conn in self.connections:
                print(f"{ip} {port}:::: {conn[0]}:{conn[1]}")
                if conn[0] == ip and int(conn[1]) == port:
                    return conn[2].pushMessage(message)
        else:
            return None

    def hasClient(self):
        return self.count

    def getClients(self):
        return self.connections

    def clientExists(self, ip, port):
        for conn in self.connections:
            if conn[0] == ip and conn[1] == port:
                return True
        return False

    def quit(self):
        self.running = False
        for ip, port, connection in self.connections:
            connection.quit()
        if self.listener:
            self.listener.join()
