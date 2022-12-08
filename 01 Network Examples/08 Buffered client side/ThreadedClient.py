# A large number of changes have been made to this file - you should notice that it now looks a lot more like the server
# that we created in the last example than the client we have dealt with before.

import socket
import errno
import time
import threading
import queue

class Client:
    def __init__(self, host="127.0.0.1", port="50000"):
        self.HOST = host
        self.PORT = port
        self.iBuffer = queue.Queue()
        self.oBuffer = queue.Queue()

        self.running = True
        self.writing = True
        self.reading = True
        self.processing = True

        self.conn = None

        # Create threads
        # Explain: As we can now receive messages out of order there is now a UI thread to deal with displaying messages
        # Explain: if this client was intelligent then we would have some actual processing in there but for now it is
        # Explain: simply a display mechanism.
        self.readThread = threading.Thread(target=self.read)
        self.writeThread = threading.Thread(target=self.write)
        self.uiThread = threading.Thread(target=self.ui)

    def write(self):
        print("Write thread started")
        while self.writing:
            if not self.running and self.oBuffer.empty():
                self.writing = False
            if not self.oBuffer.empty():
                self.conn.sendall(self.oBuffer.get().encode("utf-8"))
                time.sleep(0.1)

    def read(self):
        print("Read thread started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            self.conn.connect((self.HOST, self.PORT))
            self.conn.setblocking(False)

            while self.reading:
                # Program has stopped running - self terminate and close the socket.
                if not self.running:
                    self.reading = False
                    break

                # attempt to read data from the socket:
                try:
                    data = self.conn.recv(1024)
                    if data:
                        message = data.decode("utf-8")
                        self.iBuffer.put(message)

                # Handle errors that come from the socket
                except socket.error as e:
                    err = e.args[0]
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        time.sleep(0.1)
                    else:
                        self.running = False
                        self.conn.shutdown(socket.SHUT_RDWR)

    def ui(self):
        # Handle incoming messages from the server - at the moment that is simply "display them to the user"
        while self.running:
            if not self.iBuffer.empty():
                message = self.iBuffer.get()
                print(message)

    def process(self):
        # start the reading, writing and ui threads
        self.readThread.start()
        self.writeThread.start()
        self.uiThread.start()

        # Termination condition to handle the program shutting down
        while self.processing:
            if not self.running:
                self.processing = False
                break

            # Note that this example now only handles input at our control - we have no need of the reflow required
            # to manage the complex state before as the ui thread is managing processing of messages. We could implement
            # shared state again if we had a complex state that altered our actions, or required limitations.
            message = input("Please enter a command: ")
            self.oBuffer.put(message)

            if message == "Quit":
                self.running = False

        self.readThread.join()
        self.writeThread.join()
        self.uiThread.join()

if __name__ == "__main__":
    client = Client("127.0.0.1", 50001)
    client.process()
