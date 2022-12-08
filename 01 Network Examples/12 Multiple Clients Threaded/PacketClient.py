import socket
import errno
import time
import threading
import queue


class Client:
    def __init__(self, host="127.0.0.1", port=50000):
        self.HOST = host
        self.PORT = int(port)
        self.iBuffer = queue.Queue()
        self.oBuffer = queue.Queue()

        self.running = True
        self.writing = True
        self.reading = True
        self.processing = True

        # Packet handling information
        self.packetHeaderLength = 4
        self.networkBuffer = ""
        self.messageBuffer = ""
        self.messageInProgress = False
        self.messageBytesRemaining = 0

        self.conn = None

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

                    # Decode the message and put it into the incoming message buffer to be processed
                    if data:
                        message = data.decode("utf-8")

                        # handle the packet format: XXXXMessage
                        self.networkBuffer = ''.join([self.networkBuffer, message])

                        # Attempt to empty the network buffer:
                        bufferEmpty = False
                        while not bufferEmpty:
                            if self.messageInProgress:
                                if len(self.networkBuffer) >= self.messageBytesRemaining:
                                    # Get all remaining data from the packet from the network buffer
                                    self.messageBuffer = ''.join(
                                        [self.messageBuffer, self.networkBuffer[:self.messageBytesRemaining]])
                                    # Remove the data from the network buffer
                                    self.networkBuffer = self.networkBuffer[self.messageBytesRemaining:]

                                    # Enqueue the message:
                                    self.iBuffer.put(self.messageBuffer)

                                    # reset control variables
                                    self.messageInProgress = False
                                    self.messageBytesRemaining = 0
                                    self.messageBuffer = ""
                                else:
                                    self.messageBuffer = ''.join([self.messageBuffer, self.networkBuffer])
                                    self.messageBytesRemaining = self.messageBytesRemaining - len(
                                        self.networkBuffer)
                                    self.networkBuffer = ""
                                    bufferEmpty = True
                            else:
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
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        time.sleep(0)
                    else:
                        self.running = False
                        self.conn.shutdown(socket.SHUT_RDWR)

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


if __name__ == "__main__":
    client = Client("127.0.0.1", 50001)
    client.process()
