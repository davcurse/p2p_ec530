import threading
import socket
import sqlite3
import bleach

host = '127.0.0.1'  # localhost
port = 22212
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

all_clients = []
all_usernames = []

# generates database to store user info/message history
conn = sqlite3.connect('chat_database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('PRAGMA secure_delete = ON')

# creates client table
cursor.execute('''CREATE TABLE IF NOT EXISTS clients
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL,
                   address TEXT NOT NULL)''')

# creates message table
cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   client_id INTEGER NOT NULL,
                   message TEXT NOT NULL,
                   FOREIGN KEY (client_id) REFERENCES clients (id))''')


def broadcast(message):
    for client in all_clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'EXIT':
                index = all_clients.index(client)
                username = all_usernames[index]
                broadcast(f'{username} has left the chat.'.encode('ascii'))
                all_usernames.remove(username)
                all_clients.remove(client)
                client.close()
                exit()
            else:
                clean_message = bleach.clean(message)
                broadcast(clean_message.encode('ascii'))
                client_id = all_clients.index(client) + 1
                cursor.execute("INSERT INTO messages (client_id, message)\
                        VALUES (?, ?)", (client_id, clean_message))
                conn.commit()
        except ConnectionResetError:
            index = all_clients.index(client)
            all_clients.remove(client)
            client.close()
            username = all_usernames[index]
            broadcast(f'{username} has left the chat!'.encode('ascii'))
            all_clients.remove(client)
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

        cursor.execute("INSERT INTO clients (username, address) VALUES\
                      (?, ?)", (username, address[0]))
        conn.commit()

        print(f'Username of the client is {username}')
        broadcast(f'{username} joined the chat!'.encode('ascii'))
        client.send('\nConnected to the server! Enter q! at anytime to exit.'
                    .encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
