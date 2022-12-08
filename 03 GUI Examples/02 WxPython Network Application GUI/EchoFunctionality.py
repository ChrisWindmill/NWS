import threading


class EchoFunctionality:
    def __init__(self, network, ui_interface):
        self.network = network
        self.ui_interface = ui_interface
        self.running = True
        self.connections = []

    def add(self, connection):
        self.connections.append(connection)
        handler_thread = threading.Thread(target=self.process, args=(connection,), daemon=True)
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