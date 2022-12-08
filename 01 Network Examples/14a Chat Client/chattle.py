import json
import struct


class Message:
    """
    Data carrier for messages. Before a Message may be sent over the network, it must be encoded using the
    `encode_message` function
    """
    def __init__(self, buffer: bytes) -> None:
        # The byte layout of the structure is a buffer of JSON data preceded by a 2-byte header that specifies how long
        # it is.
        message_length_size = 2
        message_length = struct.unpack(">H", buffer[0:message_length_size])[0]
        message = json.loads(buffer[message_length_size:(message_length_size + message_length)])
        self.author = message["author"]
        self.body = message["body"]

    def as_command(self) -> str:
        """
        Attempts to extract a command from the message.

        :return: Contents of the command without the command character or an empty string if `self` is not a command.
        """
        return (self.body[1:] if self.body.startswith("/") else "")


def encode_message(author: str, body: str) -> bytes:
    """
    Encodes a message in the Chattle protocol format for transporting over a network connection.

    :param author: Screen name of the user that the message originated from
    :param body: Content of the message. Note that any trailing whitespace characters are stripped.
    :return: An encoded byte buffer of the message that can be decoded by creating a `Message` instance from it.
    """

    message = json.dumps({
        "author": author,
        "body": body.strip(),
    }).encode("utf-8")

    return (struct.pack(">H", len(message)) + message)
