import errno
import socket
import threading
import queue
import time

class Server:
    def __init__(self, host="127.0.0.1", port=50000):
        self.HOST = host
        self.PORT = port
        self.iBuffer = queue.Queue()
        self.oBuffer = queue.Queue()

        self.running = True
        self.writing = True
        self.reading = True
        self.processing = True

        # single connection and address variables - single client only
        self.conn = None
        self.addr = None
        self.client = False

        # Create threads
        self.readThread = threading.Thread(target=self.read)
        self.writeThread = threading.Thread(target=self.write)

    def write(self):
        print("Write thread started")
        while self.writing:
            if not self.running and self.oBuffer.empty():
                self.writing = False
            if not self.oBuffer.empty():
                try:
                    self.conn.sendall(self.oBuffer.get().encode("utf-8"))
                    time.sleep(0.1)
                except:
                    print("Network error, shutting down")
                    self.running = False
                    self.oBuffer.clear()

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
            self.client = True
            with self.conn:
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
                            time.sleep(0.1)
                            #print(f"no data to read from {self.addr}")
                        else:
                            # an actual error has occurred, shut down the program as our sole client is now disconnected
                            self.running = False
                            self.conn.shutdown(socket.SHUT_RDWR)

    def process(self):
        # start the reading and writing threads
        self.readThread.start()
        self.writeThread.start()

    def hasClient(self):
        return self.client

    def getMessage(self):
        if not self.iBuffer.empty():
            return self.iBuffer.get()
        else:
            return None

    def pushMessage(self, message):
        self.oBuffer.put(message)

    def quit(self):
        self.running = False
        self.readThread.join()
        self.writeThread.join()

    def process(self):
        # start the reading, writing and ui threads
        self.readThread.start()
        self.writeThread.start()


if __name__=="__main__":
    server = Server("127.0.0.1", 50001)
    server.process()