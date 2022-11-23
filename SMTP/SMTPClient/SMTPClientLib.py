import selectors
import queue
import SMTPEncryption
from threading import Thread

class Module (Thread):
    def __init__(self, sock, addr):
        Thread.__init__(self)

        self._selector = selectors.DefaultSelector()
        self._sock = sock
        self._addr = addr
        self._incoming_buffer = queue.Queue()
        self._outgoing_buffer = queue.Queue()

        self.running = True
        self.encryption = SMTPEncryption.nws_encryption()
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self._selector.register(self._sock, events, data=None)

    def run(self):
        try:
            while self.running:
                events = self._selector.select(timeout=1)
                for key, mask in events:
                    try:
                        if mask & selectors.EVENT_READ:
                            self._read()
                        if mask & selectors.EVENT_WRITE and not self._outgoing_buffer.empty():
                            self._write()
                    except Exception:
                        self.close()
                # Check for a socket being monitored to continue.
                if not self._selector.get_map():
                    break
        finally:
            self._selector.close()

    def _read(self):
        try:
            data = self._sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._incoming_buffer.put(self.encryption.decrypt(data.decode()))
            else:
                raise RuntimeError("Peer closed.")

        self._process_response()

    def _write(self):
        try:
            message = self._outgoing_buffer.get_nowait()
        except:
            message = None

        if message:
            print("sending", repr(message), "to", self._addr)
            try:
                sent = self._sock.send(message)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass

    def create_message(self, content):
        encoded = self.encryption.encrypt(content.encode())
        self._outgoing_buffer.put(encoded)

    def _process_response(self):
        message = self._incoming_buffer.get()
        header_length = 3
        if len(message) >= header_length:
            print(message[0:header_length], message[header_length:])
        print("Processing thing")

    def close(self):
        print("closing connection to", self._addr)

        self.running = False
        try:
            self._selector.unregister(self._sock)
            self._sock.close()
        except OSError as e:
            pass
        finally:
            # Delete reference to socket object for garbage collection
            self._sock = None


