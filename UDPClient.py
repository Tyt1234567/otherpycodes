from socket import *
serverName = '172.20.33.80'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)  # use IPV4 and UDP socket

message = input('please enter your message here:')
clientSocket.sendto(message.encode(),(serverName,serverPort))
print('message has been sent successfully')

# wait to receive data from server
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)  # take the buffer size 2048
print(modifiedMessage.decode())
print(serverAddress)
clientSocket.close()
