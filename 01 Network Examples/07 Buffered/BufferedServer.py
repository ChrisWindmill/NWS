# There are lots of changes made in these files - please read the notes carefully

#Explain note the differences in the imports here, specifically threading and errno
import errno
import socket
import threading
import queue
import time
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
        # Explain: we have added a pair of queues to read and write from rather than interacting with the sockets
        # Explain: rather than interacting with the sockets directly.
        self.iBuffer = queue.Queue()
        self.oBuffer = queue.Queue()

        # Explain: as we now have multiple running parts of the code, we need to ensure all messages are sent before
        # Explain: we shut down the program, so we now have running as the overall shutdown controller, and a control
        # Explain: variable for the reader/writer and the processing components, most of these aren't used for much
        self.running = True
        self.writing = True
        self.reading = True
        self.processing = True

        # single connection and address variables - single client only
        self.conn = None
        self.addr = None

        # Variables dealing with state management and state functionality
        self.currentState = State.Start
        self.previousState = None
        self.counter = 0
        self.messages = []

        # Create threads
        # Explain: uses the threading library to run these functions on a seperate thread - note: does not start
        # Explain: the threads yet.
        self.readThread = threading.Thread(target=self.read)
        self.writeThread = threading.Thread(target=self.write)

    def write(self):
        print("Write thread started")
        while self.writing:
            # Explain: The termination condition for our writing thread is that we have stopped running, and all
            # Explain: messages that are outgoing have been sent.
            if not self.running and self.oBuffer.empty():
                self.writing = False
            # Explain: if there is a message in the output buffer we should send it to the client.
            # Explain: Note - the time.sleep(1) here is to ensure that this program runs in human time as we have not
            # Explain: yet implemented the packet header and so there is no way to determine where messages start and
            # Explain: stop if they are joined together by the network.
            if not self.oBuffer.empty():
                self.conn.sendall(self.oBuffer.get().encode("utf-8"))
                time.sleep(1)

    def read(self):
        print("Read thread started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Socket binding to actual IP address/Port combination
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))

            # Set socket to listen for incoming connections, then block waiting for a connection
            s.listen()
            self.conn, self.addr = s.accept()

            # When a client connection is accepted
            with self.conn:
                # Explain: as we want to be able to loop round to terminate the running of this thread using the control
                # Explain: variables we need to set our socket to non-blocking - this means we now need to handle the
                # Explain: error conditions that come back when we have no data but the socket still exists
                self.conn.setblocking(False)
                print(f"Connected by {self.addr}")

                while self.reading:
                    # Program has stopped running - self terminate and close the socket.
                    if not self.running:
                        self.reading = False
                        break

                    # attempt to read data from the socket:
                    try:
                        data = self.conn.recv(1024)

                        # Decode the message and put it into the incoming message buffer to be processed
                        if data:
                            message = data.decode("utf-8")
                            self.iBuffer.put(message)

                    # Handle errors that come from the socket
                    except socket.error as e:
                        err = e.args[0]
                        # No data on socket, but socket still exists - wait and retry
                        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                            time.sleep(1)
                            print(f"no data to read from {self.addr}")
                        else:
                            # an actual error has occurred, shut down the program as our sole client is now disconnected
                            self.running = False
                            self.conn.shutdown(socket.SHUT_RDWR)

    def process(self):
        # start the reading and writing threads
        self.readThread.start()
        self.writeThread.start()

        # Termination condition to handle the program shutting down
        while self.processing:
            if not self.running:
                self.processing = False
                break

            # only attempt to process a message if there is a message in the incoming message buffer
            if not self.iBuffer.empty():
                message = self.iBuffer.get()

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
                    # Note that we now can handle the complex state as part of our normal message traffic - though this
                    # does introduce an edge case that Quit as the first message in this state will quit rather than
                    # being treated as text.
                    elif self.currentState == State.Complex:
                        message = self.complex(message)
                    else:
                        message = self.handleError(message)
                self.oBuffer.put(message)

        # Wait for the other two threads to complete and shutdown before continuing
        self.readThread.join()
        self.writeThread.join()

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
        self.messages.append(message)
        while True:
            # Note the changes here to interact with the buffer itself rather than the network
            if not self.iBuffer.empty():
                message = self.iBuffer.get()
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

if __name__=="__main__":
    server = Server("127.0.0.1", 50001)
    server.process()