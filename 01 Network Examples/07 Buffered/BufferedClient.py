import socket


class Client:
    def __init__(self, host="127.0.0.1", port=50000):
        self.HOST = host
        self.PORT = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))

            while True:
                message = input("Please enter a command: ")
                s.sendall(message.encode("utf-8"))

                data = s.recv(1024)
                # formatted string - calls str.format() function which calls object.__format__()
                # !r indicated we call this on repr(object).__format__() instead, !s calls str() and !a ascii()
                print(f"Received {data!r}")

                response = data.decode("utf-8")
                if response.startswith("COMPLEXTEST"):
                    print("Entering a different style of state")
                    while True:
                        message = input("Please enter a message: ")

                        s.sendall(message.encode())

                        if message == "TERMINATE":
                            data = s.recv(1024)
                            print(f"Received {data!r}")
                            break

                if message == "Quit":
                    s.shutdown(socket.SHUT_RDWR)
                    break

if __name__ == "__main__":
    client = Client("127.0.0.1", 50001)
    client.run()
