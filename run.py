#import packages 
from app.routes import *
from database.models import *
import socket

def main(): 
    drop_db_table()
    create_db_table("schema.sql","query.sql")
    try: 
        hostname = socket.gethostname()
        hostIP = socket.gethostbyname(hostname)
        app.run(hostIP, port=8080)#, debug=True)
        print("🫡 Server started")
    except Error as e:
        print (f"Starting Server failed - Error: {e}")

if __name__ == '__main__':
    main()