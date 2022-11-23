__author__ = "Kieran Osborne"
__version__ = "0.0.1"
__status__ = "Development"

import threading

if (__name__ == "__main__"):
    import chattle
    import config
    import socket
    import sys

    username = input("username: ")
    address = (config.host, config.port)

    print("Starting connection to", address)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        is_running = True

        server_socket.connect_ex(address)

        def handle_server():
            while True:
                response_data = server_socket.recv(config.message_max)

                if not response_data:
                    exit(0)

                print(response_data.decode("utf-8"))

        # Listen for input.
        threading.Thread(target=handle_server).start()

        for line in sys.stdin:
            if not line.startswith("/"):
                sys.stdout.write("<You> ")
                sys.stdout.write(line)
                sys.stdout.flush()

            server_socket.send(chattle.encode_message(username, line))
