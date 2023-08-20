import threading #running each user on one thread
import socket   #communicating with each user
import time

host = '127.0.0.1'
port = 60000 #check netstat if active port error
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''AF_INET is address family of ipv4
SOCK STREAM is a tcp socket - reliable 
SOCK UDGRAM is a udp socket (conn live, send whatever possible)
'''

server.bind((host,port))
server.listen()

client_ports = [] 
'''client_ports[socket objects]'''
users = []
'''Names of the users that are live'''

def logging(message):
    message = message + "\n"
    file = open("ServerLog.txt",'a')
    file.write(message)
    file.close()

def broadcast(message):
    for client in client_ports:
        client.send(message) #client is from server.accept() which returns socket object
    message = message.decode('utf-8')
    logging(f'CLIENT: {message}')


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            #save event
        except:
            index = client_ports.index(client)
            client_ports.remove(client)
            client.close() #close socket
            name = users[index]
            broadcast(f'{name} went offline'.encode('utf-8'))
            print(f'{name} went offline')
            users.remove(name)
            break


def receive():
    while True:
        try:
            client, address = server.accept()
            print(f'Client connection at {str(address)}')
            logging(f'SERVER: Client connection at {str(address)}')
            client.send('$SERVER Enter Name>'.encode('utf-8')) 
            name = client.recv(1024).decode('utf-8')
            users.append(name)
            client_ports.append(client)
            print(f'User connected - {name}')
            broadcast(f'{name} is live'.encode('utf-8'))
            logging(f'SERVER: User connected - {name}')
            client.send('Connected'.encode('utf-8'))

            thread = threading.Thread(target=handle_client, args=(client,)) #args is a tuple 
            thread.start()
            print("Listening again...")
        except Exception:
            exit()

print('Server listening ...')
timenow = str(time.strftime("%d-%m-%Y %H:%M:%S", time.localtime()))
logging(f"SERVER: Server Started at ('127.0.0.1', 60000) at {timenow}")
receive()