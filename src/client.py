import socket
import threading

username = input('Enter a username: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('127.0.0.1', 22212))
except ConnectionError:
    print("ERROR 404: Connection refused.")
    exit()


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except NameError:
            print("An error occurred.")
            client.close()
            break


def write():
    while True:
        message = input("")
        if message.lower() == 'q!':
            client.send('EXIT'.encode('ascii'))
            break
        else:
            message = f'{username}: {message}'
            client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
