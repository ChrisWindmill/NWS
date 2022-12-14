import socket
import threading
from ConnectionHandler import ConnectionHandler
from enum import Enum


class Role(Enum):
    SERVER = 1
    CLIENT = 2


class NetworkInterface:
    def __init__(self):
        self.listeners = []
        self.connectionHandler = ConnectionHandler()
        self.running = True

    def start_server(self, ip, port, callbackHandler=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ip, port))

        listener = threading.Thread(target=self.listen, args=(sock, callbackHandler))
        listener.start()
        self.listeners.append(listener)
        return True

    def listen(self, sock=None, callBackHandler=None):
        while self.running:
            # Set socket to listen for incoming connections, then block waiting for a connection
            sock.listen()
            conn, addr = sock.accept()
            conn.setblocking(False)
            connection = self.connectionHandler.add_connection(conn)
            callBackHandler(connection)

    def start_client(self, ip, port, duration=20, retries=30):
        # Modification starts here
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Variables to track the connection attempts
        connected = False
        attempts = 0
        # Set the timeout on the socket to 1s - this is how long we will wait for a response
        conn.settimeout(duration)

        while not connected and attempts < retries:
            try:
                conn.connect((ip, port))
                connected = True
            except socket.error:
                attempts += 1
        if connected:
            return self.connectionHandler.add_connection(conn)
        return None

    def get_message(self, ip=None, port=None):
        return self.connectionHandler.get_message(ip, port)

    def push_message(self, message, ip=None, port=None):
        return self.connectionHandler.push_message(ip, port, message)

    def has_client(self):
        return self.connectionHandler.has_client()

    def get_clients(self):
        return self.connectionHandler.get_clients()

    def client_exists(self, ip, port):
        return self.connectionHandler.client_exists(ip,port)

    def quit(self):
        self.connectionHandler.quit()
        self.running = False
        for listener in self.listeners:
            listener.join()
