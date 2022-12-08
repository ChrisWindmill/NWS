from NetworkInterface import NetworkInterface
from types import SimpleNamespace
import threading

class FunctionalityHandler:
    def __init__(self, network):
        self.network = network
        self.running = True
        self.connections = []

    def add(self, connection):
        self.connections.append(connection)
        handlerThread = threading.Thread(target=self.process, args=(connection,))
        handlerThread.start()

    def process(self, connection=None):
        # Termination condition to handle the program shutting down
        while self.running:
            # only attempt to process a message if there is a message in the incoming message buffer
            if connection:
                message = connection.iBuffer.get()

                if message:
                    connection.oBuffer.put(message)
        self.network.quit()


class AbstractServer:
    def __init__(self, host="127.0.0.1", port=50000):
        self.networkHandler = NetworkInterface()
        self.functionalityHandler = FunctionalityHandler(self.networkHandler)
        self.host = host
        self.port = port

    def client_handler(self, clientConnection):
        self.functionalityHandler.add(clientConnection)

    def process(self):
        self.networkHandler.start_server(self.host, self.port, self.client_handler)

        while True:
            print(self.networkHandler.get_clients())
            message = input("Enter string:")
            ip = input("enter Ip")
            port = input("enter port")

            self.networkHandler.push_message(message, ip, int(port))


if __name__ == "__main__":
    server = AbstractServer("127.0.0.1", 50001)
    server.process()
