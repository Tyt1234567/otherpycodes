from socket import *
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_DGRAM)  # use IPV4 and UDP socket
serverSocket.bind(('', serverPort))  # bind the port number to the socket's server
print('The server is ready to receive')

while True:
    message, ClientAddress = serverSocket.recvfrom(2048)
    print(message.decode())
    print(ClientAddress)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), ClientAddress)