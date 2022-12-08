import socket
from enum import Enum

class State(Enum):
    Start = 1
    Echo = 2
    Counting = 3
    Error = 99

class Server:
    def __init__(self, host="127.0.0.1", port=50000):
        self.HOST = host
        self.PORT = port
        self.currentState = State.Start
        self.previousState = None
        self.running = True
        self.counter = 0

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Socket binding to actual IP address/Port combination
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))

            # Set socket to listen for incoming connections, then block waiting for a connection
            s.listen()
            conn, addr = s.accept()

            # When a client connection is accepted
            with conn:
                print(f"Connected by {addr}")
                while self.running:
                    data = conn.recv(1024)
                    if not data:
                        break

                    message = data.decode("utf-8")

                    # Handle termination
                    if message == "Quit":
                        message = "Acknowledge quitting"
                        self.running = False
                    else:
                        # Handle simple state:
                        if self.currentState == State.Start:
                            if message.startswith("Echo"):
                                self.previousState = self.currentState
                                self.currentState = State.Echo
                                message = "Moving to echo"
                            elif message.startswith("Count"):
                                self.previousState = self.currentState
                                self.currentState = State.Counting
                                message = "Moving to count"
                            else:
                                message = "That was not a valid command"
                        elif self.currentState == State.Echo:
                            if message.startswith("Count"):
                                self.previousState = self.currentState
                                self.currentState = State.Counting
                                message = "Moving to count"
                            else:
                                message = "Echoing: " + message
                        elif self.currentState == State.Counting:
                            if message.startswith("Echo"):
                                self.previousState = self.currentState
                                self.currentState = State.Echo
                                message = "Moving to Echo"
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

                        else:
                            message = "An Error has occurred, returning to start state"
                            self.currentState = State.Start
                            self.previousState = State.Error

                    # send back the response
                    conn.sendall(message.encode("utf-8"))

if __name__=="__main__":
    server = Server("127.0.0.1", 50001)
    server.run()