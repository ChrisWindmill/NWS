from AbstractedServer import Server
from enum import Enum

class State(Enum):
    Start = 1
    Echo = 2
    Counting = 3
    Complex = 4
    Error = 99

class abstractServer:
    def __init__(self, host="127.0.0.1", port=50000):
        self.server = Server(host, port)

        # Variables dealing with state management and state functionality
        self.currentState = State.Start
        self.previousState = None
        self.counter = 0
        self.messages = []

        self.running = True

    def process(self):
        self.server.process()

        # Termination condition to handle the program shutting down
        while self.running:
            # only attempt to process a message if there is a message in the incoming message buffer
            message = self.server.getMessage()
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
                    elif self.currentState == State.Counting:
                        message = self.count(message)
                    # Note the change here again - complex now processes in the same way as any other state
                    elif self.currentState == State.Complex:
                        message = self.complex(message)
                    else:
                        message = self.handleError(message)
                # As complex can now return a None message, we need to handle that concept
                if message:
                    self.server.pushMessage(message)
        self.server.quit()


    def echo(self, message):
        if message.startswith("Count"):
            self.previousState = self.currentState
            self.currentState = State.Counting
            message = "Moving to count"
        elif message.startswith("Complex"):
            self.previousState = self.currentState
            self.currentState = State.Complex
            message = "COMPLEXTEST"
        else:
            message = "Echoing: " + message
        return message

    def count(self, message):
        if message.startswith("Echo"):
            self.previousState = self.currentState
            self.currentState = State.Echo
            message = "Moving to Echo"
        elif message.startswith("Complex"):
            self.previousState = self.currentState
            self.currentState = State.Complex
            message = "COMPLEXTEST"
        else:
            try:
                cmd, arg = message.split(" ", 1)
            except ValueError:
                cmd = "Error"

            try:
                value = int(arg)
            except ValueError:
                value = 0

            if cmd.startswith("Add"):
                self.counter += value
            elif cmd.startswith("Sub"):
                self.counter -= value
            elif cmd.startswith("Mul"):
                self.counter = self.counter * value
            elif cmd.startswith("Div"):
                self.counter = self.counter / value
            else:
                pass

            message = str(self.counter)

        return message

    def start(self, message):
        if message.startswith("Echo"):
            self.previousState = self.currentState
            self.currentState = State.Echo
            message = "Moving to echo"
        elif message.startswith("Count"):
            self.previousState = self.currentState
            self.currentState = State.Counting
            message = "Moving to count"
        elif message.startswith("Complex"):
            self.previousState = self.currentState
            self.currentState = State.Complex
            message = "COMPLEXTEST"
        else:
            message = "That was not a valid command"

        return message

    def handleError(self, message):
        message = "An Error has occurred, returning to start state"
        self.currentState = State.Start
        self.previousState = State.Error
        return message

    def complex(self, message):
        # Complex now only needs to manage the state itself, as the network flow change is handled by the network and
        # the buffers.
        if message == "TERMINATE":
            message = "".join(self.messages)
            self.currentState = State.Start
            self.previousState = State.Complex
        else:
            self.messages.append(message)
            message = None
        return message


if __name__=="__main__":
    server = abstractServer("127.0.0.1", 50001)
    server.process()