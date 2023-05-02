import socket
import threading
import os

# https://www.neuralnine.com/tcp-chat-in-python/ was used to make this TCP chat program

# Choosing Nickname and instuctions to send a private message
nickname = input("To send a private message start the chat with 'private: the nickname of the person you wan't to send a message to : the actual message'\n Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('127.0.0.1', 55554))
except OSError:
    print("Server is not responding")
    client.close()
    exit(1)

# Listening to Server and Sending Nickname


def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server


def write():
    while True:
        try:
            message = '{}:{}'.format(nickname, input())
            client.send(message.encode('ascii'))
        except:
            print("Error has occured. Closing client")
            client.close()
            break


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
