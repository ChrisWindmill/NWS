import threading

class EchoFunctionality:
    def __init__(self, network):
        self.network = network
        self.running = True
        self.connections = []

    def add(self, connection):
        self.connections.append(connection)
        handler_thread = threading.Thread(target=self.process, args=(connection,))
        handler_thread.start()

    def process(self, connection=None):
        # Termination condition to handle the program shutting down
        while self.running:
            # only attempt to process a message if there is a message in the incoming message buffer
            if connection:
                message = connection.iBuffer.get()

                if message:
                    connection.oBuffer.put(message)
        self.network.quit()

    def quit(self):
        self.running = False