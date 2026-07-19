from src.server import listen

if __name__ == "__main__":
    while True:
        try:
            listen()
        except KeyboardInterrupt:
            exit(0)