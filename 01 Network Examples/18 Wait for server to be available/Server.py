from NetworkInterface import NetworkInterface
import time
from datetime import datetime
import threading
from colorama import Fore, Back, Style


class FunctionalityHandler:
    def __init__(self, network):
        self.network = network
        self.running = True
        self.connections = []

    def add(self, connection):
        self.connections.append(connection)
        handler_thread = threading.Thread(target=self.process, args=(connection,))
        handler_thread.start()

    def update_heartbeat(self, connection):
        duration = connection.time_since_last_message()

        # You should perform your disconnect / ping as appropriate here.
        if duration > 5:
            connection.update_time()
            connection.add_timeout()
            ip, port = connection.sock.getpeername()
            print(f"{Fore.BLUE}{datetime.now()}{Style.RESET_ALL} ", end="")
            print(
                f"{Fore.RED}The last message from {Fore.GREEN}{ip}:{port}{Fore.RED} sent more than 5 seconds ago, {connection.get_timeouts()} have occurred{Style.RESET_ALL}")

    def process(self, connection=None):
        while self.running:
            if connection:
                #                Heartbeat update
                # ------------------------------------------------
                self.update_heartbeat(connection)

                if not connection.iBuffer.empty():
                    message = connection.iBuffer.get()
                    if message:
                        if message.startswith("ping"):
                            connection.oBuffer.put("pong")
                        else:
                            connection.oBuffer.put(f"Echoing: {message}")
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
            clients = self.networkHandler.get_clients()
            if len(clients) > 0:
                print(f"{Fore.BLUE}{datetime.now()}{Style.RESET_ALL}")
                for client in clients:
                    ip, port = client.sock.getpeername()
                    print(f"{Fore.YELLOW}{ip}:{port} {Style.RESET_ALL}", end="")
                print()
            time.sleep(2)


if __name__ == "__main__":
    server = AbstractServer("127.0.0.1", 50005)
    server.process()
