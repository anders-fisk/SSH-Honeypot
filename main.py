from server.src.server import listen
from map.app import app, get_ip_address
import threading
import sys

if __name__ == "__main__":
    if sys.argv[1] == "--server" :
        while True:
            try:
                listen()
            except KeyboardInterrupt:
                exit(0)

    elif sys.argv[1] == "--run" :
        t = threading.Thread(target=get_ip_address, daemon=True)
        t.start()

        # runs on port 5000 by defualt
        app.run(threaded=True)

