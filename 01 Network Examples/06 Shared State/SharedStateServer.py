import socket
from enum import Enum


class State(Enum):
    Start = 1
    Echo = 2
    Counting = 3
    Complex = 4
    Error = 99


class Server:
    def __init__(self, host="127.0.0.1", port=50000):
        self.HOST = host
        self.PORT = port
        self.currentState = State.Start
        self.previousState = None
        self.running = True
        self.counter = 0
        self.messages = []

        self.conn = None
        self.addr = None

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
        while True:
            data = self.conn.recv(1024)
            if not data:
                self.running = False
                message = "Error"
                break

            message = data.decode("utf-8")
            print(message)
            # Handle termination
            if message == "TERMINATE":
                message = "".join(self.messages)
                break
            else:
                self.messages.append(message)

        self.currentState = State.Start
        self.previousState = State.Complex
        return message

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Socket binding to actual IP address/Port combination
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))

            # Set socket to listen for incoming connections, then block waiting for a connection
            s.listen()
            self.conn, self.addr = s.accept()

            # When a client connection is accepted
            with self.conn:
                print(f"Connected by {self.addr}")
                while self.running:
                    # Note the change of order here: complex state alters how messages are handled, so must be checked
                    # first or we will eat a message we didn't plan to.
                    if self.currentState == State.Complex:
                        message = self.complex(message)
                    else:

                        data = self.conn.recv(1024)
                        if not data:
                            break

                        message = data.decode("utf-8")

                        # Handle termination
                        if message == "Quit":
                            message = "Acknowledge quitting"
                            self.running = False
                        else:
                            # Handle simple states with client->server, server-> client pattern
                            if self.currentState == State.Start:
                                message = self.start(message)
                            elif self.currentState == State.Echo:
                                message = self.echo(message)
                            elif self.currentState == State.Counting:
                                message = self.count(message)
                            else:
                                message = self.handleError(message)

                    # send back the response
                    self.conn.sendall(message.encode("utf-8"))


if __name__ == "__main__":
    server = Server("127.0.0.1", 50001)
    server.run()