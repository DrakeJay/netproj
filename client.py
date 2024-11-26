

### this is for all the connection stuff
import socket
import threading




### this is for the graphics interface
import tkinter as tk
from tkinter import scrolledtext, simpledialog

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED!"
SERVER = "35.50.68.33"   #oakland universities probably will change when connecting to oakland network again
#SERVER ip for home
#SERVER = "192.168.0.26"



#SERVER =  socket.gethostbyname(socket.gethostname())      #SERVER IP 
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

###make a interface

class ChatClient:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("400x500")

        self.username = username



        ##where all the prior text will go
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)


        #  where the user will input their text
        self.input_field = tk.Entry(self.master, font=("Arial", 12))
        self.input_field.pack(pady=5, padx=10, fill=tk.X)

        # Send button
        self.send_button = tk.Button(self.master, text="Send", command=self.send_messages)
        self.send_button.pack(pady=5)


        # Start the receiving thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # Bind Enter key to send message
        self.input_field.bind("<Return>", lambda event: self.send_messages())


        # Send username to server
        self.send_username()


    #### format the username for the server
    def send_username(self):

        try:
            message = self.username.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
        except Exception as e:
            print(f"ERROR SENDING USERNAME: {e}")

    def send_messages(self):
        #print("Type here and 'EXIT' to leave.")
        msg = self.input_field.get()
        if msg:
            #this should show the user who sent the message to their chat box
            self.show_message(f"[YOU]: {msg}")

            self.send_to_server(msg)
           
            self.input_field.delete(0, tk.END)


            if msg == DISCONNECT_MESSAGE:
                self.master.quit()

    ### This will listen for messages from the server.
    def receive_messages(self):
        while True:
            try:
                message = client.recv(2048).decode(FORMAT)
                self.show_message(message)
            except Exception as e:
                self.show_message(f"ERROR COULD NOT GET MESSAGE: {e}")
                
                break


    def show_message(self, message):
        """
        Displays a message in the chat area.
        """
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.yview(tk.END)   ##auto scroll thing
        self.chat_area.config(state=tk.DISABLED)


    ## format the message for the server
    def send_to_server(self, msg):
        try:
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
        except (ConnectionResetError, BrokenPipeError):
            self.show_message("FAILED TO SEND MESSAGE. CONNECTION HAS BEEN LOST.")
            self.master.quit()
        except Exception as e:
            self.show_message(f"ERROR COULD NOT SEND MESSAGE: {e}")
    
    



### this will make the user give us a name

if __name__ == "__main__":
    
    root = tk.Tk()
    root.withdraw()
    # Prompt for username
    username = simpledialog.askstring("Username", "Enter your username:")
    root.deiconify()


    if username:

        # Start the GUI
       
        app = ChatClient(root, username)
        root.mainloop()

        # Close the connection when GUI is closed
        
        app.send_to_server(DISCONNECT_MESSAGE)
        client.close()



##     old shit
#print("Connected to the server")
#threading.Thread(target=receive_messages, daemon=True).start()
#send_messages()

##client.close()