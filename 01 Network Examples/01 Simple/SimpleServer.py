# import the socket library - will be referenced by "socket" within the program
import socket

# Global variables: host IP address and port
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


# with: this command is effectively a try/catch control block, so the code within the block is only executed if the
# resource can be acquired. The socket is referenced with the name s, AF_INET means an IP based socket, SOCK_STREAM
# means a TCP (stream based) socket.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Socket binding to actual IP address/Port combination
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))

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