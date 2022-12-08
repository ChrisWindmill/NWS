import socket

class Server:
    def __init__(self, host="127.0.0.1", port="50000"):
        self.HOST = host
        self.PORT = port

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

                # While the socket is connected and alive (recv blocks awaiting data, if data is None the connection is gone
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    # process the data and respond - in this case echo the result back.
                    conn.sendall(data)

if __name__=="__main__":
    server = Server("127.0.0.1", 50001)
    server.run()