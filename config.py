import socket

# works on: local:host w/ any router 
hostname = socket.gethostname()
hostIP = socket.gethostbyname(hostname)
port = 8080

# works on: local:host&Raspberry-Server w/ "new" router
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("8.8.8.8",80))
#hostIP = s.getsockname()[0]