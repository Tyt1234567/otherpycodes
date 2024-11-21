from socket import *
serverName = gethostname()
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)  # use IPV4 and TCP socket

# here differ from UDP (in line 7 build connection and in line 9 send message to server with this connection directly)
clientSocket.connect((serverName, serverPort))
sentence = input('please enter your sentence here:')
clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024)
print('from server: ', modifiedSentence.decode())
clientSocket.close()