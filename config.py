import socket

#hostname = socket.gethostname()
#hostIP = socket.gethostbyname(hostname)
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
hostIP = s.getsockname()[0]