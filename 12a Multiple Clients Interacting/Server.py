from PacketServer import Listener
import threading

class functionality_handler:
    def __init__(self):
        # Variables dealing with state management and state functionality
        self.running = True
        self.connections = []
        self.services = []
        self.handlerThread = threading.Thread(target=self.process)

    def run(self):
        self.handlerThread.start()

    def quit(self):
        self.running = False

    def add_connection(self, network):
        self.connections.append(network)

    def process(self):
        # Termination condition to handle the program shutting down
        while self.running:
            for client in self.connections:
                message = client.getMessage()
                if message:
                    # Handle termination
                    if message == "Quit":
                        message = "Acknowledge quitting"
                        self.running = False

                    #               GET COMMAND
                    # -------------------------------------------
                    elif message.startswith("GET"):
                        # message in format: GET service_name
                        components = message.split(" ")
                        found = False

                        # This attempts to find the first service registered with the name requested
                        # to load balance you will want to alter this such that instead of finding the first - you find
                        # all instances of a service, then select one of those to respond with.
                        for service in self.services:
                            if service[0] == components[1]:
                                message = f"REDIRECT {service[1]} {service[2]}"
                                found = True
                                break

                        if not found:
                            message = f"ERROR SERVICE NOT_FOUND"

                    #              REGISTER COMMAND
                    # -------------------------------------------
                    elif message.startswith("REGISTER"):
                        # message in format: REGISTER ip port service_name
                        components = message.split(" ")
                        self.services.append((components[3], components[1], components[2]))
                    else:
                       message = f"ERROR INVALID_COMMAND"

                    if message:
                        client.pushMessage(message)
        for client in self.connections:
            client.quit()



class abstractServer:
    def __init__(self, host="127.0.0.1", port=50000):
        self.listener = Listener(self.client_handler, host, port)
        self.handler = functionality_handler()
        self.handler.run()

    def client_handler(self, network):
        self.handler.add_connection(network)

    def process(self):
        self.listener.listen()


if __name__ == "__main__":
    server = abstractServer("127.0.0.1", 50001)
    server.process()
