import threading 
import socket
import os

name = input("Enter your name >>")
print("Send quit() to quit the application\n\n")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '127.0.0.1'
server_port = 60000
client.connect((server_host,server_port))

def client_receiving(run):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == '$SERVER Enter Name>':
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print("Error\n",e)
            client.close()
            break
        if run == False:
            break
    
def client_sending():
    while True:
        message = input("")
        if message.lower() == "quit()":
            os._exit(0)
        broadcast = f'{name}: {message}'
        client.send(broadcast.encode('utf-8'))
        

receive_thread = threading.Thread(target=client_receiving, args=(True,))
receive_thread.start()

send_thread = threading.Thread(target=client_sending)
send_thread.start()
