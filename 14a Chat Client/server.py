__author__ = "Kieran Osborne"
__version__ = "0.0.1"
__status__ = "Development"

if (__name__ == "__main__"):
    import threading
    import chattle
    import config
    import socket

    # Sockets don't automatically close on their own, making a with statement is necessary.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Avoid "bind() exception: OSError: [Errno 48] Address already in use" error
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.bind((config.host, config.port))
        client_socket.listen()

        clients = set()

        def broadcast(broadcasting_connection, message: str) -> None:
            """
            Handles requests from a client to broadcast a message to all other connected clients but the one requesting
            the broadcast.

            :param broadcasting_connection: Originating connection that requested the message be broadcast.
            :param message: Message requested to be broadcast.
            :return: Nothing.
            """

            print(message)

            for client in clients:
                # No point broadcasting the message that the client sent the server back to the same client, it already
                # has its own local copy since it was the one that wrote it.
                if client != broadcasting_connection:
                    try:
                        client.send(message.encode("utf-8"))

                    except socket.error:
                        # Remove clients who's connections to the server have been broken
                        client.close()
                        clients.discard(client)

        def handle_client(client_connection, client_address) -> None:
            """
            Handles a single client connection, awaiting and processing input from it as and when it comes.

            :param client_connection: Client connection.
            :param client_address: Client IP and port address tuple.
            :return: Nothing.
            """

            client_ip = client_address[0]

            # Roll out the red carpet.
            client_connection.send(config.server_greeting.encode("utf-8"))

            try:
                # Handle each incoming message from the connected client.
                data = client_connection.recv(config.message_max)

                while data:
                    message = chattle.Message(data)
                    command = message.as_command()

                    if (command):
                        # It's a command message!
                        if (command == "quit"):
                            clients.discard(client_connection)
                            broadcast(client_connection, client_ip + " disconnected")
                            client_connection.close()

                            return

                        else:
                            client_connection.send(f"Unknown command: {command}".encode("utf-8"))

                    else:
                        # It's a regular message
                        broadcast(client_connection, f"<{message.author}@{client_ip}> {message.body}")

                    data = client_connection.recv(config.message_max)

            except socket.timeout:
                print(client_ip + " timed out")
                client_connection.close()
                clients.discard(client_connection)

        while True:
            # Handle each incoming connection as and when they come.
            connection, address = client_socket.accept()

            clients.add(connection)
            print(address[0] + " connected")
            # Once a connection has been received it can be sent off to be handled elsewhere and this loop continues to
            # handle connecting users.
            threading.Thread(target=handle_client, args=(connection, address)).start()
