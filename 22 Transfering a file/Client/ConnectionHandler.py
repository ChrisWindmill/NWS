import socket
import threading
import selectors
import queue


class Connection:
    def __init__(self, ip, port, sock):
        self.iBuffer = queue.Queue()
        self.oBuffer = queue.Queue()
        self.ip = ip
        self.port = int(port)
        self.sock = sock
        self.packetHeaderLength = 4
        self.networkBuffer = ""
        self.messageBuffer = ""
        self.messageInProgress = False
        self.messageBytesRemaining = 0


class ConnectionHandler:
    def __init__(self):
        # Packet handling information
        self.selector = selectors.DefaultSelector()
        self.connections = []
        self.count = 0
        self.running = True
        self.connectionThread = threading.Thread(target=self.process)
        self.connectionThread.start()

    def add_connection(self, sock):
        ip, port = sock.getpeername()
        print(f"Creating a new connection to: {ip}:{port}")
        connection = Connection(ip, port, sock)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(sock, events, data=connection)
        self.connections.append(connection)
        self.count = self.count +1
        return connection

    def service_connection(self, key, mask):
        sock = key.fileobj
        connection = key.data
        if mask & selectors.EVENT_READ:
            result = self.read(connection)
            if not result:
                self.selector.unregister(sock)
                self.connections.remove(connection)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            self.write(connection)

    def write(self, connection):
        if not connection.oBuffer.empty():
            message = connection.oBuffer.get()
            message_len = str(len(message)).zfill(connection.packetHeaderLength)
            connection.sock.sendall(''.join([message_len, message]).encode("utf-8"))

    def read(self, connection):
        # ip, port = connection.sock.getpeername()
        # print(f"Reading message from: {ip}:{port}")
        try:
            data = connection.sock.recv(1024)
            if data:
                message = data.decode("utf-8")
                connection.networkBuffer = ''.join([connection.networkBuffer, message])
                # Attempt to empty the network buffer:
                bufferEmpty = False
                while not bufferEmpty:
                    if connection.messageInProgress:
                        if len(connection.networkBuffer) >= connection.messageBytesRemaining:
                            # Get all remaining data from the packet from the network buffer
                            connection.messageBuffer = ''.join(
                                [connection.messageBuffer, connection.networkBuffer[:connection.messageBytesRemaining]])
                            # Remove the data from the network buffer
                            connection.networkBuffer = connection.networkBuffer[connection.messageBytesRemaining:]

                            # Enqueue the message:
                            connection.iBuffer.put(connection.messageBuffer)

                            # reset control variables
                            connection.messageInProgress = False
                            connection.messageBytesRemaining = 0
                            connection.messageBuffer = ""
                        else:
                            connection.messageBuffer = ''.join([connection.messageBuffer, connection.networkBuffer])
                            connection.messageBytesRemaining = connection.messageBytesRemaining - len(
                                connection.networkBuffer)
                            connection.networkBuffer = ""
                            bufferEmpty = True
                    else:
                        if len(connection.networkBuffer) >= connection.packetHeaderLength:
                            # Get the length of the next packet
                            connection.messageBytesRemaining = int(connection.networkBuffer[:connection.packetHeaderLength])
                            # remove the header from the network buffer
                            connection.networkBuffer = connection.networkBuffer[connection.packetHeaderLength:]
                            connection.messageInProgress = True
                        else:
                            # We do not have a full packet header, wait for another incoming packet
                            bufferEmpty = True
            return True
        # Handle errors that come from the socket
        except socket.error as e:
            return False

    def getMessage(self, ip, port):
        # print(f"Getting message from connection: {ip}:{port}")
        for connection in self.connections:
            if connection.ip == ip and connection.port == port:
                if not connection.iBuffer.empty():
                    return connection.iBuffer.get()
                else:
                    return None

    def pushMessage(self, ip, port, message):
        # print(f"Sending message to connection: {ip}:{port}")
        for connection in self.connections:
            if connection.ip == ip and connection.port == port:
                connection.oBuffer.put(message)
                break

    def has_client(self):
        return self.count

    def get_clients(self):
        return self.connections

    def client_exists(self, ip, port):
        for conn in self.connections:
            ip_remote, port_remote = conn.sock.getpeername()
            if ip_remote == ip and int(port_remote) == port:
                return True
        return False

    def quit(self):
        self.running = False

    def process(self):
        try:
            while self.running:
                if len(self.connections) > 0:
                    events = self.selector.select(timeout=None)
                    for key, mask in events:
                        if key.data is None:
                            self.add_connection(key.fileobj)
                        else:
                            self.service_connection(key, mask)
        finally:
            self.selector.close()
