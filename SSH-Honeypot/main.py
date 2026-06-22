"""Basic server for password auth."""
import logging
import socket

import paramiko

# Set up logging globally.
# basically an alternative for print, just puts DEBUG before everything
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
# silences paramikos logger
logging.getLogger("paramiko").setLevel(logging.WARNING)

HOSTKEY_ED25519 = paramiko.Ed25519Key(filename="C:/Users/user/.ssh/id_ed25519.txt")

class Server(paramiko.ServerInterface):
    def check_channel_request(self, kind, chanid):
        if kind == "session" :
            return paramiko.OPEN_SUCCEEDED

# checks user's password
    def check_auth_password(self, username: str, password: str):
        if username == "user" and password == "password":
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

# if program runs with a command
    def check_channel_exec_request(self, channel: paramiko.Channel, command: bytes):
        self.event.set()
        cmd = command.decode()
        print("skibidi")
        logger.info("channel_exec request received: %s", cmd)

        if cmd == "banner" :
            self.banner(channel)

        elif cmd.startswith("echo ") :
            self.echo(channel, cmd)
        else:
            return False
        return True

# these two functions give the program two different command options, either display the banner or echo back the cmd
    def banner(self, chan: paramiko.Channel):
        chan.send(
            """===== Test server banner =====
    We should include some ascii art...
    """
        )

    def echo(self, chan: paramiko.Channel, cmd: str):
        _, s = cmd.split("echo ")
        chan.send(s)

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 2222))
    sock.listen(100)
    client, addr = sock.accept()

    t = paramiko.Transport(client)
    t.add_server_key(HOSTKEY_ED25519)

    # Starts the server and negotiates a new session as server. Either returns
    server = Server()
    t.start_server(server=server)

    t.accept(timeout=20)  # blocks until channel opens
    print(f"[Server] Channel opened successfully:")
    t.close()

if __name__ == "__main__":
    while True:
        try:
            listen()
        except KeyboardInterrupt:
            exit(0)
        except OSError:
            logger.exception("Caught OSError, usually address already in use")
            exit(1)
        except Exception as exc:
            logger.error(exc)