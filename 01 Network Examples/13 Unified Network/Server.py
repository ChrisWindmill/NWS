from NetworkInterface import NetworkInterface
from ConnectionHandler import ConnectionHandler
from enum import Enum
import threading

class State(Enum):
    Start = 1
    Echo = 2
    Counting = 3
    Complex = 4
    Error = 99


class FunctionalityHandler:
    def __init__(self, network):
        # Variables dealing with state management and state functionality
        self.currentState = State.Start
        self.previousState = None
        self.counter = 0
        self.messages = []

        self.network = network
        self.running = True

        self.handlerThread = threading.Thread(target=self.process)

    def run(self):
        self.handlerThread.start()

    def process(self):
        # Termination condition to handle the program shutting down
        while self.running:
            # only attempt to process a message if there is a message in the incoming message buffer
            message = self.network.getMessage()
            if message:
                # Handle termination
                if message == "Quit":
                    message = "Acknowledge quitting"
                    self.running = False

                else:
                    # Handle simple state:
                    if self.currentState == State.Start:
                        message = self.start(message)
                    elif self.currentState == State.Echo:
                        message = self.echo(message)
                    else:
                        message = self.handleError(message)
                # As complex can now return a None message, we need to handle that concept
                if message:
                    self.network.pushMessage(message)
        self.network.quit()

    def echo(self, message):
        if message.startswith("Count"):
            self.previousState = self.currentState
            self.currentState = State.Counting
            message = "Moving to count"
        else:
            message = "Echoing: " + message
        return message

    def start(self, message):
        if message.startswith("Echo"):
            self.previousState = self.currentState
            self.currentState = State.Echo
            message = "Moving to echo"
        else:
            message = "That was not a valid command"

        return message

    def handleError(self, message):
        message = "An Error has occurred, returning to start state"
        self.currentState = State.Start
        self.previousState = State.Error
        return message


class AbstractServer:
    def __init__(self, host="127.0.0.1", port=50000):
        self.networkHandler = NetworkInterface(host, port, self.client_handler)

    def client_handler(self, network):
        # This still creates a new thread to handle each client connection - as such there is no way for the server to
        # actively read messages between the client and this handler. At the moment network is simply an instance of the
        # ConnectionHandler the FunctionalityHandler can use to add/send messages, we would likely need to add an
        # intermediate stage to catch messages and decide what to do with them.
        handler = FunctionalityHandler(network)
        handler.run()

    def process(self):
        self.networkHandler.startServer()

        while True:
            print(self.networkHandler.getClients())
            message = input("Enter string:")
            ip = input("enter Ip")
            port = input("enter port")

            self.networkHandler.pushMessage(message, ip, int(port))




if __name__ == "__main__":
    server = AbstractServer("127.0.0.1", 50001)
    server.process()
