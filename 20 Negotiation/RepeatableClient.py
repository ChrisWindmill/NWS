import socket
from num2words import num2words
from diffiehellman import diffie_hellman
from vigneresquare import vignere_cipher

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 50001  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))


    data = s.recv(1024)
    message = data.decode("utf-8")
    p, q, serverKey = message.split(":")

    dhgenerator = diffie_hellman(int(p), int(q))
    dhgenerator.calculate_partial_key()
    dhgenerator.calculate_full_key(int(serverKey))

    s.send(f"{dhgenerator.partial_key}".encode("utf-8"))

    key = num2words(dhgenerator.symmetric_key)

    vigcipher = vignere_cipher()
    vigcipher.set_key(key)
    print(dhgenerator.symmetric_key)

    while True:
        message = input("Please enter a command: ")
        message = vigcipher.encrypt(message)
        data = message.encode("utf-8")
        s.sendall(data)

        data = s.recv(1024)
        message = data.decode("utf-8")
        message = vigcipher.decrypt(message)

        print(f"Received {message}")

        if message == "Quit":
            s.shutdown(socket.SHUT_RDWR)
            break

