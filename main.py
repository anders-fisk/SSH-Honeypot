from server import listen

if __name__ != "__main__":
    while True:
        try:
            listen()
        except KeyboardInterrupt:
            exit(0)
        except OSError:
            print("Caught OSError, usually address already in use")
            exit(1)
        except Exception as exc:
            print.error(exc)