from NetworkInterface import NetworkInterface
import threading
from EchoFunctionality import EchoFunctionality
from DictionaryFunctionality import DictionaryFunctionality
import time

class TalkToYourServer:
    def __init__(self, host="127.0.0.1", port=50000, ui_interface=None):
        self.networkHandler = NetworkInterface()
        self.ui_interface = ui_interface
        self.host = host
        self.port = port
        self.tab_id = 0

        # # Handlers are provided reference to the network manager
        self.echoHandler = EchoFunctionality(self.networkHandler, self.ui_interface)
        self.dictionaryHandler = DictionaryFunctionality(self.networkHandler, self.ui_interface)

        # Variables to handle our internal client connections
        self.clientConnection = None
        self.uiThread = threading.Thread(target=self.ui, daemon=True)
        self.server_thread = threading.Thread(target=self.process, daemon=True)
        self.running = True


    def echo_handler(self, client_connection):
        self.echoHandler.add(client_connection)

    def dict_handler(self, client_connection):
        self.dictionaryHandler.add(client_connection)

    # Simple UI thread
    def ui(self):
        # Handle incoming messages from the server - at the moment that is simply "display them to the user"
        while self.running:
            if self.clientConnection:
                message = self.clientConnection.iBuffer.get()
                if message:
                    print(message)
                    if self.clientConnection:
                        if self.clientConnection.tab_id != 0:
                            self.ui_interface.add_text(self.clientConnection.tab_id, message)


    def process(self):
        # Start the two handlers on port 50001, 50002
        self.networkHandler.start_server(self.host, self.port, self.dict_handler)
        self.networkHandler.start_server(self.host, self.port+1, self.echo_handler)


        # Create a client connection to a server - in this case our own dictionary server
        self.clientConnection = self.networkHandler.start_client(self.host, self.port)
        self.ui_interface.add_entry(self.clientConnection)

        while self.running:
            time.sleep(1)
            message = input("Please enter a command: ")
            if self.clientConnection:
                self.clientConnection.oBuffer.put(message)
            else:
                self.running = False

            if message == "Quit":
                self.running = False

    def stop(self):
        # stop the network components and the UI thread
        self.uiThread.join()
        self.networkHandler.quit()


    def start(self):
        self.uiThread.start()
        self.server_thread.start()

if __name__ == "__main__":
    server = TalkToYourServer("127.0.0.1", 50001)
    server.process()
