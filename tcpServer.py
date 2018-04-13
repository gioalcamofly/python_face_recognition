import socket
import sys
from video_software import find as real_find
from video_software import updateFiles as real_update

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)

print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(1)

while True:
    print (sys.stderr, 'waiting')
    connection, client_address = sock.accept()

    try:
        print (sys.stderr, 'connection from', client_address)

        while True:
            data = connection.recv(8192)
            data = data[2:]
            print (sys.stderr, 'received', data)
            if data == "start":
                print (sys.stderr, 'sending data')
                real_update()
                name = real_find()
                print (sys.stderr, 'the name is', name)
                connection.sendall(name + '\n')
            elif data == "continue":
                print(sys.stderr, 'sending data')
                name = real_find()
                print(sys.stderr, 'the name is', name)
                connection.sendall(name + '\n')
            elif data == "update":
            	print(sys.stderr, 'sending data')
            	real_update()
            else:
                print (sys.stderr, 'no more data')
                connection.sendall("no more data\n")
                break
    finally:
        connection.close()
