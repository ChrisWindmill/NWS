# Core libraries
import base64
import threading

# Text colouring on console
try:
    from colorama import Fore, Back, Style
    VERBOSE = True
except ImportError:
    VERBOSE = False

try:
    # Playback libraries
    import vlc
    import time
    ENABLEMEDIA = True
except ImportError:
    ENABLEMEDIA = False

# Our code
from NetworkInterface import NetworkInterface


class abstractClient:
    def __init__(self, host="127.0.0.1", port=50000):
        self.host = host
        self.port = port
        self.networkHandler = NetworkInterface()
        self.connection = None
        self.uiThread = threading.Thread(target=self.ui)
        self.running = True
        self.fileBuffer = ""
        self.filename = ""
        self.WRITE = False

    # Simple UI thread
    def ui(self):
        # Handle incoming messages from the server - at the moment that is simply "display them to the user"
        while self.running:
            if self.connection:
                #            Handle File Writing
                # ----------------------------------------------
                if self.filename != "" and self.WRITE:
                    print("Writing to file")
                    self.fileBuffer = self.fileBuffer + '=' * (len(self.fileBuffer) % 4)
                    base64_img_bytes = self.fileBuffer.encode('utf-8')
                    with open(self.filename, "wb") as file:
                        decoded_image_data = base64.decodebytes(base64_img_bytes)
                        file.write(decoded_image_data)
                    self.fileBuffer = ""
                    self.filename = ""
                    self.WRITE = False

                #            Handle Normal message traffic
                # ----------------------------------------------
                message = self.connection.iBuffer.get()

                #            Handle File Name command
                # ----------------------------------------------
                if message.startswith("FNAME"):
                    command, self.filename = message.split(" ", 1)
                    #print(self.filename)

                #            Handle File Chunks
                # ----------------------------------------------
                elif message.startswith("FILE"):
                    # Note: we have a pseudo header here: command and length relate to the whole packet
                    # then cmdtype, value, max, and rest are the encapsulated content
                    # cmdtpye is "CHUNK", value is current chunk # (note no out of order processing) and max is expected
                    # number of chunks
                    command, length, cmdtype, value, max, rest = message.split(" ", 5)

                    self.fileBuffer = "".join((self.fileBuffer, rest))
                    if VERBOSE: print (f"{Fore.RED}{int(value)+1}/{Fore.GREEN}{int(max)}{Style.RESET_ALL}")

                    # If we have received all chunks of data
                    if (int(value)+1) == int(max):
                        self.WRITE = True
                    else:
                        pass

                    # Options to display parts of the message
                    # if VERBOSE:
                        # print(f"{Fore.RED}{command}{Style.RESET_ALL}")
                        # print(f"{Fore.GREEN}{length}{Style.RESET_ALL}")
                        # print(f"{Fore.RED}{cmdtype}{Style.RESET_ALL}")
                        # print(f"{Fore.GREEN}{value}{Style.RESET_ALL}")
                        # print(f"{Fore.GREEN}{max}{Style.RESET_ALL}")
                        # print(f"{Fore.BLUE}{rest}{Style.RESET_ALL}")
                else:
                    # Simply display what the server sent us
                    print(message)

    def process(self):
        # Start the UI thread and start the network components
        self.uiThread.start()
        self.connection = self.networkHandler.start_client(self.host, self.port)

        while self.running:
            message = input("Please enter a command: ")

            # Local playback to test media transfer: only enabled if VLC is present
            if message == "Quit":
                self.running = False
            elif message.startswith("PLAY"):
                if ENABLEMEDIA:
                    components = message.split(" ", 1)
                    p = vlc.MediaPlayer(components[1])
                    p.play()
                    time.sleep(15)
                    p.stop()
            elif self.connection:
                self.connection.oBuffer.put(message)
            else:
                self.running = False

        # stop the network components and the UI thread
        self.networkHandler.quit()
        self.uiThread.join()

if __name__ == "__main__":
    client = abstractClient("127.0.0.1", 50001)
    client.process()