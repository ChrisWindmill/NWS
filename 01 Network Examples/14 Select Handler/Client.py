# All of the processing code has now been pulled into this file - the network code remains in the other file Abstract...

from NetworkInterface import NetworkInterface
from ConnectionHandler import ConnectionHandler
import threading

class abstractClient:
    def __init__(self, host="127.0.0.1", port=50000):
        self.host = host
        self.port = port
        self.networkHandler = NetworkInterface()
        self.connection = None
        self.uiThread = threading.Thread(target=self.ui)
        self.running = True

    # Simple UI thread
    def ui(self):
        # Handle incoming messages from the server - at the moment that is simply "display them to the user"
        while self.running:
            if self.connection:
                message = self.connection.iBuffer.get()
                if message:
                    print(message)

    def process(self):
        # Start the UI thread and start the network components
        self.uiThread.start()
        self.connection = self.networkHandler.start_client(self.host, self.port)

        while self.running:
            message = input("Please enter a command: ")
            if self.connection:
                self.connection.oBuffer.put(message)
            else:
                self.running = False

            if message == "Quit":
                self.running = False

        # stop the network components and the UI thread
        self.networkHandler.quit()
        self.uiThread.join()

if __name__ == "__main__":
    client = abstractClient("127.0.0.1", 50001)
    client.process()