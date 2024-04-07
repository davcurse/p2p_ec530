import threading
import socket

host = '127.0.0.1'  # localhost
port = 22212

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


all_clients = []
all_usernames = []


def broadcast(message):
    for client in all_clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except NameError:
            index = all_clients.index(client)
            all_clients.remove(client)
            client.close()
            username = all_usernames[index]
            broadcast(f'{username} left the chat!'.encode('ascii'))
            all_usernames.remove(username)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        all_usernames.append(username)
        all_clients.append(client)

        print(f'Username of the client is {username}')
        broadcast(f'{username} joined the chat!'.encode('ascii'))
        client.send('\nConnected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
