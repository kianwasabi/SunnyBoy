import socket

hostname = socket.gethostname()
hostIP = socket.gethostbyname(hostname)
port = 8080