from socket import *
import sys
import re

def create_header_from_dict(header_dict):
    return_string = ''
    for k in header_dict.keys():
        return_string += str(k)+": "+str(header_dict[k])+'\r\n'
    return return_string

def create_header(status_code, file_size):
    status_message = 'OK'
    if status_code == '404':
        status_message = 'NOT FOUND'
    status_line = 'HTTP/1.1 %s %s'%(status_code,status_message)
    header_dict={}
    header_dict['Connection'] = 'close'
    header_dict['Date'] = 'close'
    header_dict['Server'] = 'close'
    header_dict['Last-Modified'] = 'close'
    header_dict['Content-Length'] = file_size
    header_dict['Content-Type'] = 'close'
    header = create_header_from_dict(header_dict)
    return status_line + '\r\n' + header
                                    
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print "The server is ready to receive"
while 1:
    connectionSocket, addr = serverSocket.accept()
    request = connectionSocket.recv(4096)
    lines = re.split('\r\n',request)
    filename = lines[0].split(" ")[1]
    status_code = '200'
    file_size = 0
    file_string = ''
    try:
        file = open(filename,'rb')
        file_string = file.read()
        file_size = len(file_string)
        file.close()
        print filename,file_size
    except:
        print filename,"here"
        status_code = '404'
    header = create_header(status_code,file_size)
    response = header + '\r\n' + file_string
    connectionSocket.send(response)
    connectionSocket.close()
