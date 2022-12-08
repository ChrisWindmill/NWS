# All of the processing code has now been pulled into this file - the network code remains in the other file Abstract...

from PacketClient import Client
import threading

class abstractClient:
    def __init__(self, host="127.0.0.1", port=50000):
        self.client = Client(host, port)
        self.uiThread = threading.Thread(target=self.ui)
        self.running = True

    # Simple UI thread
    def ui(self):
        # Handle incoming messages from the server - at the moment that is simply "display them to the user"
        while self.running:
            message = self.client.getMessage()
            if message:
                print(message)

    def process(self):
        # Start the UI thread and start the network components
        self.uiThread.start()
        self.client.process()

        while self.running:
            message = input("Please enter a command: ")
            self.client.pushMessage(message)

            if message == "Quit":
                self.running = False

        # stop the network components and the UI thread
        self.client.quit()
        self.uiThread.join()

if __name__ == "__main__":
    client = abstractClient("127.0.0.1", 50001)
    client.process()