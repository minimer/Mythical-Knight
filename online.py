import socket
from json import loads,dumps

def IPs():
    return [i[-1][0] for i in socket.getaddrinfo(socket.gethostname(),0,socket.AF_INET)]

class Server:
    def __init__(self,server):
        host,port=server.split(':')
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind((host,int(port)))
    def get(self,size):
        data, addres = self.sock.recvfrom(size)
        return (loads(data.decode('utf-8')),addres)
    def send(self,data,addres):
        self.sock.sendto(dumps(data).encode('utf-8'), addres)

class Client:
    def __init__(self,server):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = server.split(':')
        self.server[1]=int(self.server[1])
        self.sock.bind(('', 0))
    def get(self,size):
        return loads(self.sock.recvfrom(size).decode('utf-8'))
    def send(self,data):
        self.sock.sendto(dumps(data).encode('UTF-8'),self.server)
