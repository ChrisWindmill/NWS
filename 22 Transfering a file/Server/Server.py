from NetworkInterface import NetworkInterface
import threading
import os
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
import base64

class FunctionalityHandler:
    def __init__(self, network):
        self.network = network
        self.running = True
        self.connections = []

    def add(self, connection):
        self.connections.append(connection)
        handlerThread = threading.Thread(target=self.process, args=(connection,))
        handlerThread.start()

    def process(self, connection=None):
        # Termination condition to handle the program shutting down
        while self.running:
            # only attempt to process a message if there is a message in the incoming message buffer
            if connection:
                message = connection.iBuffer.get()

                if message:
                    if message.startswith("FILELIST"):
                        files = self.get_file_list()
                        for file in files:
                            print(f"{Fore.GREEN}{file}\t{Style.RESET_ALL}")
                            connection.oBuffer.put(file)
                    elif message.startswith("GET"):
                        components = message.split(" ")
                        if len(components) < 2:
                            connection.oBuffer.put(f"Error: no filename specified")
                        else:
                            data = self.get_file_data(components[1])
                            if len(data) == 0:
                                connection.oBuffer.put(f"Error: {components[1]} does not exist")
                            else:
                                connection.oBuffer.put(f"FNAME {components[1]}")
                                current = 0
                                total = 0
                                i = 0
                                blocksize = 300
                                blocks = []
                                datalength = len(data)
                                fullblockcount = datalength // blocksize
                                partialblock = False if (datalength % blocksize) == 0 else True

                                for i in range(0, fullblockcount):
                                    blocks.append(data[i*blocksize:(i+1)*blocksize])

                                if partialblock:
                                    blocks.append(data[fullblockcount*blocksize:])
                                print(f"{Fore.BLUE}{len(blocks)}{Style.RESET_ALL}")
                                for chunk in blocks:
                                    total = total + len(chunk)

                                counter = 0
                                for chunk in blocks:
                                    current = current + len(chunk)
                                    print(f"{Fore.RED}{current}/{total}{Style.RESET_ALL}")
                                    message = "".join((f"CHUNK {counter} {len(blocks)} ", chunk))
                                    response = "".join((f"FILE {len(message)} ", message))
                                    connection.oBuffer.put(response)
                                    counter = counter + 1
                    else:
                        host, port = connection.sock.getpeername()
                        print(f"{Fore.GREEN}{host}:{port}\t{Fore.RED}ERROR\t{Style.RESET_ALL} message")
                        connection.oBuffer.put(f"server received {message}")

        self.network.quit()

    def get_file_list(self, path="\\files"):
        path = os.getcwd() + path
        fileList = []
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            if os.path.isfile(filepath):
                fileList.append(file)

        return fileList
        # List comprehension version - creates list of files with their paths.
        # fileList = [file for file in listdir(path) if isfile(join(path, file))]

    def get_file_data(self, filename, blocksize=300, path="\\files"):
        blocks = []
        path = os.getcwd() + path
        filename = os.path.join(path, filename)
        try:
            with open(filename, "rb") as file:
                data = file.read()
                base64_encoded_data = base64.b64encode(data)
                base64_message = base64_encoded_data.decode('utf-8')
            return base64_message

            #     datalength = len(data)
            #     fullblockcount = datalength // blocksize
            #     partialblock = False if (datalength % blocksize) == 0 else True
            #
            #     for i in range(0, fullblockcount):
            #         blocks.append(data[i*blocksize:(i+1)*blocksize])
            #
            #     if partialblock:
            #         blocks.append(data[fullblockcount*blocksize:])
            # return blocks, partialblock
        except:
            return ""#[], False



class AbstractServer:
    def __init__(self, host="127.0.0.1", port=50000):
        self.networkHandler = NetworkInterface()
        self.functionalityHandler = FunctionalityHandler(self.networkHandler)
        self.host = host
        self.port = port

    def client_handler(self, clientConnection):
        self.functionalityHandler.add(clientConnection)

    def process(self):
        self.networkHandler.start_server(self.host, self.port, self.client_handler)

        while True:
            print(self.networkHandler.get_clients())
            message = input("Enter string:")
            ip = input("enter Ip")
            port = input("enter port")

            self.networkHandler.push_message(message, ip, int(port))


if __name__ == "__main__":
    just_fix_windows_console()
    server = AbstractServer("127.0.0.1", 50001)
    server.process()
