Chattle is a chat client and server designed to demonstrate the basics of implementing communication protocols over a network.

Out of the box, Chattle comes with:

  * JSON-encoded byte buffer protocol for transporting authored messages over a network.
  * Multi-client server capable of broadcasting messages between clients and acting as the communication authority.
  * Command framework built into the messaging protocol for sending slash commands over the network. Out of the box, only a `/quit` command is provided.

Chattle lacks any security layers to its protocol, its transport format could be more efficient, and user IPs are made visible to every connected client. It is intended to be used as a foundation for experimentation and learning.
