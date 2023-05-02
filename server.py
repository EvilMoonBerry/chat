import socket
import threading
# Connection Data
host = '127.0.0.1'
port = 55554

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients


def broadcast(message):

    for client in clients:
        client.send(message)

# Handling private messages From Clients


def private(nick, user, message):
    text = '{} says: {}'.format(nick, message).encode('ascii')
    index2 = nicknames.index(nick)
    try:
        index = nicknames.index(user)
        for client in clients:
            print(client)
            if client == clients[index]:
                client.send(text)
    except:
        clients[index2].send(
            ("Something went wrong. There might not be user with that name").encode('ascii'))

# Cheking the user feed and acting accoringly


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            text = message.split(":")
            if text[1] == "private" or text[1] == "Private":
                # send a private message
                private(text[0], text[2], text[3])
            else:
                # if not private message send to all
                broadcast(message.encode('ascii'))
        except:
            # Removing And Closing Clients
            print("Error has occured")
            index = clients.index(client)
            print(index)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
