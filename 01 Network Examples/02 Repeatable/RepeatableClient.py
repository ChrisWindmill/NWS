import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        message = input("Please enter a command: ")
        s.sendall(message.encode("utf-8"))

        data = s.recv(1024)
        # formatted string - calls str.format() function which calls object.__format__()
        # !r indicated we call this on repr(object).__format__() instead, !s calls str() and !a ascii()
        print(f"Received {data!r}")

        if message == "Quit":
            s.shutdown(socket.SHUT_RDWR)
            break

