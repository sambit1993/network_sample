import sys
from socket import *
import re

IP = sys.argv[1]
PORT = int(sys.argv[2])


def create_header(ip):
    return '''Host: %s\r\nConnection: close\r\nUser-agent: py\r\nAccept-language: en\r\n''' % (ip)


def check_status(received_message):
    lines = re.split('\r\n', received_message)
    if lines[0].split(" ")[1] == '404':
        return False
    return True

filename = sys.argv[3]
request_line = "GET %s HTTP/1.1" % (filename)
header = create_header(IP)
request_string = '\r\n'.join([request_line,header])+'\r\n'

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((IP,PORT))
clientSocket.send(request_string)

received_message = clientSocket.recv(4096)

if not check_status(received_message):
    print "File Not Found"
else:
    lines = re.split('\r\n',received_message)
    file_size = 0
    start_ind = 0
    for i,elem in enumerate(lines):
        if 'Content-Length' in elem:
            file_size = int(elem.split(" ")[1])
        if elem == '':
            start_ind = i+1

    initial_file_string = '\r\n'.join(lines[start_ind:])
    received_file_size = len(initial_file_string)
    file = open(filename,'wb')
    file.write(initial_file_string)
    file.close()
    file = open(filename,'ab')
    while received_file_size < file_size:
        print str(received_file_size)+"/"+str(file_size)
        received_message, serverAddress = clientSocket.recvfrom(4096)
        file.write(received_message)
        received_file_size += len(received_message)
    file.close()


