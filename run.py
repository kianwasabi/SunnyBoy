from app.routes import *
from database.models import *
from config import *

def main(): 

    drop_db_table()
    create_db_table("schema.sql","processcontrol.sql")
    try: 
        app.run(hostIP, port, debug=True)
        print("🫡 Server started")
    except Error as e:
        print (f"Starting Server failed - Error: {e}")

if __name__ == '__main__':
    main()