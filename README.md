CSI-2470-42484.202440-Intro to Computer Networks


This is a simple chat application built in Python that lets people connect and chat in real time. The app has two parts: a server that handles connections and messages, and a client that users can use to join the chat. Each user gets a username, and all messages are shared with everyone connected to the chat.
What You Can Do

    Chat in Real-Time: Send and receive messages instantly.
    Choose a Username: Pick a username to show who’s talking.
    Easy-to-Use Interface: The client has a simple chat window for sending and reading messages.
    Group Chat: Everyone connected to the server can see and join the conversation.
    Disconnect Gracefully: You can leave the chat by closing the window or typing a disconnect command.

How It Works

The project has two main parts:

    server.py:
        This is the "brain" of the chat. It listens for new connections, handles incoming messages, and shares them with everyone.
        It runs on the computer acting as the server.

    client.py:
        This is what users run to join the chat. It connects to the server and lets users send and receive messages.
        It has a simple graphical interface built with tkinter.

How to Run It
Requirements

    Python 3.10 or later
    Libraries: socket, threading, tkinter (these come with Python, no extra installation needed)
    Server and clients need to be on the same network (like Wi-Fi or LAN).
    The client will need the ip address of the server pc in order to establish a   connection. Add to the client.py code   

Steps


    Start the Server:
        Run the server.py file:

    python server.py

    The server will wait for clients to join.

Run a Client:

    Run the client.py file:

        python client.py

        A small box will pop up asking for your username. Enter your name and press OK.
        The chat window will open, and you can start chatting!

    Add More Clients:
        Run client.py on other devices or terminals to add more users to the chat.

    Chat:
        Type messages into the input field and press Enter or click "Send."
        Your messages will appear in the chat, along with messages from others.

    Leave the Chat:
        Close the chat window or type DISCONNECTED! to leave.

Example
Server Example:

SERVER STARTING!!!!!!!!!!!!!!!
[LISTENING ON 192.168.0.26:5050]
NEW CONNECTION ('192.168.0.10', 5001) CONNECTED.
Username: Alice from ('192.168.0.10', 5001)
Alice has joined the chat!
[Bob] Hello everyone!
[Alice] Hi Bob!
Bob has left the chat.
Connection with Bob closed.

Client Example:

    When the client starts, you’ll see a dialog box asking for your username.
    After entering your username, the chat window will open:

    [You]: Hello everyone!
    [Alice]: Hi!

In order for it to work correctly 

    Same Network: The server and clients need to be on the same network for this to work.
    No Private Messages: All messages are shared with everyone.
    Plain Text: Messages are not encrypted, so it’s not secure for sensitive information.

Some Ideas for Improvements

    Add private messaging between users.
    Use encryption to make the chat more secure.
    Add a way to log in with a password.
    Improve the look of the chat window with a modern design.
