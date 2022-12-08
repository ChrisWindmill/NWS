import threading
import pickle


class DictionaryFunctionality:
    def __init__(self, network):
        self.network = network
        self.running = True
        self.connections = []
        self.dict = {"literally": "A synonym for figuratively", "figuratively": "not literally",
                     "test": "what you should do to your code", "comment": "your code has some right?"}

    def write_to_disk(self):
        file = open("dictionary.uod", "wb")
        pickle.dump(self.dict, file)
        file.close()


    def get_from_disk(self):
        file = open("dictionary.uod", "rb")
        self.dict = pickle.load(file)
        file.close()

    def add(self, connection):
        self.connections.append(connection)
        handler_thread = threading.Thread(target=self.process, args=(connection,))
        handler_thread.start()

    def process(self, connection=None):
        # Termination condition to handle the program shutting down
        while self.running:
            # only attempt to process a message if there is a message in the incoming message buffer
            if connection:
                message = connection.iBuffer.get()

                if message:
                    return_message = ""
                    if message.startswith("get"):
                        components = message.split(" ")
                        if len(components) > 1:
                            meaning = self.get_from_dict(components[1])
                            return_message = meaning
                        else:
                            return_message.join("Invalid command: get <no parameter>")
                    elif message.startswith("put"):
                        components = message.split(" ", 2)
                        if len(components) > 2:
                            self.add_to_dict(components[1], components[2])
                            return_message = f"added {components[1]} to dictionary"
                        else:
                            return_message = "Invalid command: get <no parameter>"
                    elif message.startswith("write"):
                        self.write_to_disk()
                    elif message.startswith("read"):
                        self.get_from_disk()
                    else:
                        return_message = "Invalid command"
                    connection.oBuffer.put(return_message)
        self.network.quit()

    def add_to_dict(self, key, meaning):
        self.dict[key] = meaning

    def get_from_dict (self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return "not in dictionary"

    def quit(self):
        self.running = False