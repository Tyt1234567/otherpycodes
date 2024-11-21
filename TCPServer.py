from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(2)  # the maximum number of queued connections
print('the server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()  # create a new socket in the server
    sentence = connectionSocket.recv(4096).decode()
    connectionSocket.send(sentence.upper().rjust(10).encode())
    connectionSocket.close()
