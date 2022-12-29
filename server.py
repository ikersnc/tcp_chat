import socket
import threading

#Connection data
host = '127.0.0.1'
port = 55555

#Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#Clients
clients = []
nicknames = []

#Send messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            #broadcast message
            message = client.recv(1024)
            broadcast(message)
        except:
            #removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left!.'.encode('ascii'))
            nicknames.remove(nickname)
            break

#receiving/listening function
def receive():
    while True:
        #Accept connection
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        #Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        #Print and broadcast nickname
        print(f'Nickname is {nickname}')
        broadcast(f'{nickname} joined!'.encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        #Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Chat initiated...')
receive()