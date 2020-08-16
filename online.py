import socket

def IPs():
    return [i[-1][0] for i in socket.getaddrinfo(socket.gethostname(),0,socket.AF_INET)]