#import packages 
from app.routes import *
from database.models import *
import socket

def main(): 
    models.drop_db_table()
    models.create_db_table("schema.sql")
    hostname = socket.gethostname()
    hostIP = socket.gethostbyname(hostname)
    app.run(hostIP, port=8080, debug=True)
    print("🫡Server started")

if __name__ == '__main__':
    main()