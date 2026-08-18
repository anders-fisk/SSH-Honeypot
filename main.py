from server.src.server import listen
from map.app import APP
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
        APP.run(debug=True)
