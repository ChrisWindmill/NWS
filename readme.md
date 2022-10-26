
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
