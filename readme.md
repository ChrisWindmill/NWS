
# Single Client guide

## Running order

1. Simple
2. Repeatable
3. Class
4. State
5. State with functions 
6. SharedState 
7. Buffered server 
8. Buffered client and server
9. Abstracted network interface
10. Choose your own adventure
11. Packet Server
12. Multiple clients (threaded)
13. Unified network access (threaded)
14. Multiple clients (select)
15. Simple peer-to-peer example
16. Simple GUI
17. Networked GUI
18. Simple Cipher
19. Symmetric Key Exhange (Diffie-Hellman)
20. Negotiation
21. Textbook RSA

## Descriptions

### Simple

This example provides a very minimal client-server setup that allows a single message to be sent between the client and
the server after which the server and client both shutdown.

Run order: SimpleServer.py, SimpleClient.py

### Repeatable

This example provides a minimal client-server setup that allows multiple messages to be sent by the client and echoed 
by the server. If the command "Quit" is sent both sides shut down.

Run order: RepeatableServer.py, RepeatableClient.py


### Class

This example provides a simple evolution of the repeatable server to now move the code into a class making use of
instance variables to provide a more reusable framework for the system.

Run order: ClassServer.py, ClassClient.py


### State

This example adds a three state system to the class based example adding Echo and Counting commands, some simple error 
checking has been added to this example to add resiliency when handling string parsing.

Run order: StateServer.py, StateClient.py

> #### Commands
> Echo, move to the echo state
> 
> Count, move to the counting state

While in the counting state you can use:
> Add X, add X to the current count
> 
> Sub X, subtract X from the current count
> 
> Mul X, multiply the current count by X
> 
> Div X, divide the current count by X

## StateFunction

This example takes the state example used previously and moves the state code from the main body of the run function
into separate functions to improve readability of the solution. 

Run order: StateFunctionServer.py, StateFunctionClient.py


### SharedState

This example takes the state example used previously and adds a complex state to the system where the client can send
messages repeatedly until the client sends a specific command sequence (TERMINATE) before moving back to the original
start state. You have the added commands:

> Complex, move to the complex state

In this state, any text you type will be added to an internal buffer on the server side, when you send `TERMINATE` it
will echo back all the messages sent, then move back to the start state. 

Run order: SharedStateServer.py, SharedStateClient.py

### Buffered Server Side
This example adds some simple threading to the code and separates the read/writing to use a queue instead of relying on
directly interacting with the network interfaces. The buffering is only implemented on the server side to show you how
the interaction functions.

Run order: BufferedServer.py, BufferedClient.py

### Buffered Client Side
This example adds the buffering from the server side in the previous example to the client side allowing you to see how 
a section of network code can be reused and managed to provide a more modular solution to the problem of dealing with a 
network.

Run order: ThreadedServer.py, ThreadedClient.py

### Abstracted Network
This example pulls the network code from the main code into a separate class and file allowing you to interact with the
network code only through the input and output buffer queues. This means that you can now reuse this code more easily as
the functionality has been separated out into a network layer and a functionality layer. 

Run order: AbstractedServer.py, AbstractedClient.py

### Choose your own adventure 
This example implements a very simple "Choose your own adventure" game using the abstracted network. The game allows you
to construct a `book` of `pages` each of which contains the description for that page and the options to move to other 
pages in the book. Some simple input validation is performed to stop users entering non-integer options. Options on each
page are numering, and in the default model are `1` and `2`. A standalone version of this code is shown in 
`StandAloneCYO.py` so you can see how you can develop a non-networked version of the code and then develop this into a 
networked version.

Run order: ChooseYourOwnServer.py, ChooseYourOwnClient.py

### Packet Server
This example takes the previous code base and adds a simple header format of four characters representing the length of
the message, then the message itself. The network code in the packet server and client now only return full messages to
the input and output buffers, so this code is now safe to network time. Node that there are significant changes in the 
network code base in the read and write functions - though the changes are the same in the client and server.

Run order: Server.py, Client.py

### Multiple clients (threaded)
This example takes the previous code base and implements the capability for the server to handle multiple clients at
once using a separate threaded handler for each client (read thread, write thread) making it very inefficient as there
is a large thread overhead. 

Run order: Server.py, Client.py

### Unified network access (threaded)
This example takes the previous code base and unifies the connection handling for the server and client into a single
class (`ConnectionHandler.py`) with an interface placed on top of this to manage the creation of listeners and direct
socket connections (`NetworkInterface.py`). By merging this common code we can begin to abstract the network away and 
begin to work with the system as a message passing interface.

Run order: Server.py, Client.py

### Multiple clients (select)
This example modifies the previous code base to utilise a `select` based model allowing a single thread to handle
reading and writing to all connected entities. Each listener is still created as a separate thread to minimise the
potential confusion over handling multiple incoming connections with a single handler function. You should consider
altering the code base to move this functionality into the `ConnectionHandler` so that the `NetworkInterface` can have
reduced knowledge of the network improving the layering of our system.

Run order: Server.py, Client.py

### Simple peer-to-peer example
This example creates a single `node` which starts two services - one with echo functionality, and one with dictionary 
functionality. These two simple blocks of functionality show how you can easily add new functions to a node on the
network. At current each of these creates a thread to handle each new client connected to the service - though it would 
be relatively simple to alter this to allow one thread per service, or to allow multiple services to be called from 
one processing thread.

The example starts the dictionary on port 50001, and the echo on port 50002 (specified port +1)

When connected to the echo functionality all input is echoed back to the client.

When connected to the dictionary functionality the following functionality is available:
> get `word`, returns the desription of the entered word
> 
> put `word` `description`, adds the word and associated description to the dictionary
> 
> write, writes the current dictionary to disk using a `pickle` dump.
> 
> read, loads the dictionary from disk (note: a dictionary must be present)


Run order: Server.py

### Simple GUI
You will need to have wxPython installed, `pip install wxPython` will handle this on a machine that you manage.

This programme demonstrates a simple wxPython GUI application showcasing the use of panels, sizers, and other graphical
components that you may wish to use. It has very limited functionality. [RealPython](https://realpython.com/python-gui-with-wxpython/) 
has a good tutorial on this library.


Run order: wxGui.py

### Networked GUI
This example modifies the simple GUI example to integrate with the simple peer-to-peer node that we created previously. 
It makes use of events to create GUI elements within the application and show data. 
>N.B. this example is currently in development and may not function fully correctly. The Server 
> will accept messages from itself and displays them in one tab, additional connections do not currently
> generate additional tabs.

Run order: wxGUI.py

### Simple Cipher
These example are simple transpositional ciphers - a Caesar cipher (constant shift of x places around the alphabet), and
a Vigenère cipher which uses a code word to provide `length(code word)` shifts within the ciphered phrase.

Run order: caesar.py
Run order: vigneresquare.py

### Symmetric Key Exchange (Diffie-Hellman)
This example demonstrates the mathematics underlying a Diffie-Hellman key exchange process.
The example makes use of ephemeral keys so provides forward-security but no authentication. 

Run order: DH.py

### Negotiation
This example shows how you could integrate a Diffie-Hellman key exchange into your networked application to generate a 
set of keys that can be used to feed an encryption algorithm. The example uses the Diffie-Hellman ephemeral keys to
create a code word (using the `num2words` library) which feeds a Vigenère cipher.

Renegotiation is not carried out at all during this process.


Run order: NegotiationServer.py, NegotiationClient.py

### Textbook RSA
This example implements the textbook version of the RSA algorithm for encryption and digital signatures.

Run order: SimpleRSA.py

### Transferring a file
This example implements the a simple file transfer using chunked data (300 byte blocks). The file is recreated on the
client side of the connection and can then be used normally. If you have VLC currently installed you can use `PLAY <filename>`
to hear audio files. The transfer uses a Base64 encoding of the file chunks so that the string message passing we have 
implemented previously can be utilised.

> Note: When transferring audio files default windows media players will not play the file until it has been moved from
> the directiory - the file is valid but throws an error. The VLC playback option will work.


> #### Commands:
> `FILELIST` returns a list of all files in the current directory (by default `files` of the server)
> 
> `GET <filename>` attempts to transfer the given filename, will return chunks of 300 bytes until the file is fully
> transfered if the file is present or an error otherwise.
> 
> `PLAY <filename>` if VLC is installed this will attempt to play the provided media file. Note - this has no error
> checking and VLC will likely throw a large number of "errors" from stale caching of mods.
 

Run order: Server.py, Client.py

### Simple heartbeat example
This example implements a simple heartbeat that allows you to determine if a connection has timed out, and how many such 
events have occurred. A second client is provided (`AutoPingClient.py`) that runs a background thread to maintain an 
active connection if the user has not sent a message in the last 4 seconds.

Run order: Server.py, Client.py, AutoPingClient.py

## Notes

> #### Import
>      import socket
>  import the socket library - will be referenced by "socket" within the program

> #### with
>      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
>          s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
>          s.bind((HOST, PORT))
> This command is effectively a try/finally control block.
>
>     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>     try:
>         pass # the code inside the with block
>     finally:
>         s.close()
>so the code within the block is only executed if the
> resource can be acquired. The block calls `__enter__()` and `__exit__()` on entry and exit of the with block allowing 
> you to actively manage the resource life-cycles.
> 
>The socket is referenced with the name s, AF_INET means an IP based socket, SOCK_STREAM
> means a TCP (stream based) socket.

> #### Stream based networking

> #### Threads
> 

> #### Thread Safety

> #### Selectors

> #### GUIs