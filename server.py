import socket
import threading

PORT = 5050

HEADER = 64         #64 bytes length of the message


SERVER = socket.gethostbyname(socket.gethostname())     #this gets the name of device/ip address
print(socket.gethostname())

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"


#A list to have all the clients in
clients = []
client_lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
# handle all invidial connections of the client and server

# make the server send messages to all clients 

def broadcast(message, sender_conn):
    """
    Send the message to all clients except the sender.
    """
    with client_lock:
        for client in clients:
            conn, _ = client
            if conn != sender_conn:
                try:
                    conn.send(message.encode(FORMAT))
                except Exception as e:
                    print(f"Error sending message to a client: {e}")


def handle_client(conn, addr):
    print("NEW CONNECTION  {addr} CONNECTED.")
    username = None  #set it to none

    conn.settimeout(None)  # will close the server after x amount of time

    try:
        # Receive username
        print("Waiting to receive username...")
        msg_length = conn.recv(HEADER).decode(FORMAT)
        print(f"Received message length: {msg_length}")
        if msg_length:
            msg_length = int(msg_length)
            username = conn.recv(msg_length).decode(FORMAT)
            print(f"Username: {username} from {addr}")



            #add the clients to the list
            with client_lock:
                clients.append((conn, username))

            ## let all users know of a new connection
            broadcast(f"{username} has joined the chat!", conn)




        connected = True
        while connected:
            try:
                msg_length = conn.recv(HEADER).decode(FORMAT) 
                print(f"Received raw message length: {msg_length}")   #how many bytes we want to accept from the connection? Use the header variable
                if msg_length:                                                #decode will decode the bytes to a string
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)

                    if msg == DISCONNECT_MESSAGE:
                        connected = False

                        #let people know that a person has left
                        print(f"{username} DISCONNECTED")
                        broadcast(f"{username} has left the chat.", conn)
                        #broadcast the message to all clients connected
                    else:
                        print(f"[{username}] {msg}")
                        broadcast(f"[{username}] {msg}" , conn)
                else:
                    # If no data is received, break the connection loop
                    print(f"Connection with {addr} lost.")
                    connected = False

                    print(f"[{addr}] {msg}")



            except socket.timeout:
                print(f"Connection with {addr} timed out.")
                connected = False
            except Exception as e:
                print(f"ERROR handling Client {addr}: {e}")
                connected = False
                break
    finally:
    #Remove the clients
        with client_lock:
            if username:
                clients.remove((conn, username))
            else:
                print(f"Could not remove {addr} from list.")
        conn.close()
        print(f"Connection with {username} ({addr}) closed.")

               #close connection



### handle new connections and distibute where they need to go
def start():
    server.listen()
    print("[LISTENING ON {SERVER}]")
    while True:
        conn, addr = server.accept()       #store the info of the host connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS {threading.activeCount() - 1}")




print("SERVER STARTING!!!!!!!!!!!!!!!")
start()