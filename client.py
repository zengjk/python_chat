"""Script for Tkinter GUI chat client."""
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving messages"""
    total_msg = ''
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            total_msg = total_msg + msg
            # print(total_msg)
            if '{END}' in total_msg:
                index = total_msg.find('{END}')
                while index != -1:
                    msg_list.insert(tkinter.END, total_msg[:index])
                    total_msg = total_msg[index+5:]
                    index = total_msg.find('{END}')
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):
    """Handles sending messages"""
    msg = my_msg.get()  # my_msg is the input field on the GUI
    msg = msg + '{END}'
    print(msg)
    my_msg.set("")  # clear the input field in the GUI
    client_socket.send(bytes(msg, "utf8"))


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()
    client_socket.close()
    top.quit()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
# To navigate through past messages
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15,
                           width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = '127.0.0.1'
PORT = None
if not PORT:
    PORT = 33002  # Default value.
else:
    PORT = int(PORT)
BUFFER_SIZE = 10
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
