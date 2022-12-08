import errno
import socket
import threading
import queue
import time


class ConnectionHandler:
    def __init__(self, conn, addr):
        self.iBuffer = queue.Queue()
        self.oBuffer = queue.Queue()

        # Packet handling information
        self.packetHeaderLength = 4
        self.networkBuffer = ""
        self.messageBuffer = ""
        self.messageInProgress = False
        self.messageBytesRemaining = 0

        self.running = True
        self.writing = True
        self.reading = True
        self.processing = True

        # Connection and address variables
        self.conn = conn
        self.addr = addr

        # Create threads
        self.readThread = threading.Thread(target=self.read)
        self.writeThread = threading.Thread(target=self.write)

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

    def write(self):
        print("Write thread started")
        while self.writing:
            if not self.running and self.oBuffer.empty():
                self.writing = False
            if not self.oBuffer.empty():
                try:
                    # Get the message to the client and sort the length of the message - note no error checking on len
                    # This should be capped at 9999 bytes for our current header length of 4 digits.
                    message = self.oBuffer.get()
                    messageLen = str(len(message)).zfill(self.packetHeaderLength)
                    self.conn.sendall(''.join([messageLen, message]).encode("utf-8"))
                except:
                    print("Network error, shutting down")
                    self.running = False
                    self.oBuffer.clear()

    def read(self):
        # When a client connection is accepted
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

                        # handle the packet format: XXXXMessage
                        self.networkBuffer = ''.join([self.networkBuffer, message])

                        print(self.networkBuffer)
                        # Attempt to empty the network buffer:
                        bufferEmpty = False
                        while not bufferEmpty:
                            if self.messageInProgress:
                                # We have received a message header successfully, or have a partial message
                                if len(self.networkBuffer) >= self.messageBytesRemaining:
                                    # Get all remaining data from the packet from the network buffer
                                    self.messageBuffer = ''.join([self.messageBuffer, self.networkBuffer[:self.messageBytesRemaining]])
                                    # Remove the data from the network buffer
                                    self.networkBuffer = self.networkBuffer[self.messageBytesRemaining:]

                                    # Enqueue the message:
                                    self.iBuffer.put(self.messageBuffer)

                                    # reset control variables
                                    self.messageInProgress = False
                                    self.messageBytesRemaining = 0
                                    self.messageBuffer = ""
                                else:
                                    # Take as much of the message as possible from the buffer
                                    self.messageBuffer = ''.join([self.messageBuffer, self.networkBuffer])
                                    self.messageBytesRemaining = self.messageBytesRemaining - len(self.networkBuffer)
                                    self.networkBuffer = ""

                                    # Exit the packet handler this iteration
                                    bufferEmpty = True
                            else:
                                # We handle messages by looking for the packet header, then iterating back round
                                if len(self.networkBuffer) >= self.packetHeaderLength:
                                    # Get the length of the next packet
                                    self.messageBytesRemaining = int(self.networkBuffer[:self.packetHeaderLength])
                                    # remove the header from the network buffer
                                    self.networkBuffer = self.networkBuffer[self.packetHeaderLength:]
                                    self.messageInProgress = True
                                else:
                                    # We do not have a full packet header, wait for another incoming packet
                                    bufferEmpty = True

                # Handle errors that come from the socket
                except socket.error as e:
                    err = e.args[0]
                    # No data on socket, but socket still exists - wait and retry
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        time.sleep(0)
                        # print(f"no data to read from {self.addr}")
                    else:
                        # an actual error has occurred, shut down the program as our sole client is now disconnected
                        self.running = False
                        self.conn.shutdown(socket.SHUT_RDWR)

class Listener:
    def __init__(self, callback_handler, host="127.0.0.1", port=50000):
        self.HOST = host
        self.PORT = port

        # Client handlers
        self.clients = []
        self.count = 0

        # Control variable
        self.running = True

        # callback handler for creating
        self.callbackHandler = callback_handler

    def listen(self):
        print("Listening thread started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Socket binding to actual IP address/Port combination
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))

            while self.running:
                # Set socket to listen for incoming connections, then block waiting for a connection
                s.listen()
                conn, addr = s.accept()
                self.count = self.count+1

                connection = ConnectionHandler(conn, addr)
                self.clients.append((self.count, connection))
                connection.process()
                self.callbackHandler(connection)

    def hasClient(self):
        return self.count

    def quit(self):
        self.running = False
        for id, connection in self.clients:
            connection.quit()



if __name__=="__main__":
    server = Listener(None, "127.0.0.1", 50001)
    server.listen()