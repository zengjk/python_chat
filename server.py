"""Server for multithreaded (asynchronous) chat application."""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

names = {}
addresses = {}

GREATING = bytes(
    "Greetings from the cave! \nNow type your name and press enter!{END}", "utf8")

HOST = ''
PORT = 33002
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)


def accept_incoming_connections():
    """sets up handling for incoming clients."""
    while True:
        client, client_addr = server.accept()
        print('Connected by ', client_addr)
        client.send(GREATING)
        addresses[client] = client_addr
        t = Thread(target=handle_client, args=(client, ))
        t.start()


def client_connect_init(client):
    '''initialize a new connection'''
    name = client.recv(BUFFER_SIZE).decode("utf8")[:-5]
    names[client] = name
    welcome_msg = 'Wassup, %s! If you want to exit, plz simply close the window' % name
    group_welcome_msg = 'Attention! %s has joined the group chat!' % name

    client.send(bytes(welcome_msg+"{END}", "utf8"))
    broadcast(group_welcome_msg)


def receive_all(client):
    total_msg = ''
    while True:
        msg = client.recv(BUFFER_SIZE)
        msg_str = msg.decode("utf8")
        total_msg = total_msg + msg_str
        if '{END}' in msg_str:
            index = total_msg.find('{END}')
            total_msg = total_msg[:index]
            return total_msg


def send_out(client, msg):
    broadcast(names[client]+": ")
    broadcast(msg)


def broadcast(msg):
    """Broadcasts a message to all the clients."""
    for sock in names:
        sock.send(bytes(msg+"{END}", "utf8"))
        print(msg)


def handle_client(client):
    client_connect_init(client)
    while True:
        msg = receive_all(client)
        if msg[:6] == '{quit}':
            client.close()
            name = names[client]
            del names[client]
            broadcast("%s has left the chat." % name)
            break
        else:
            send_out(client, msg)


if __name__ == "__main__":
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    server.close()
