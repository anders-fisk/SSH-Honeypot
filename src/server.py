"""Basic server for password auth."""
import logging
import socket
import threading

import paramiko

# Set up logging globally.
# basically an alternative for print, just puts DEBUG before everything
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
# silences paramikos logger
logging.getLogger("paramiko").setLevel(logging.WARNING)

HOSTKEY_ED25519 = paramiko.Ed25519Key(filename="C:/Users/user/.ssh/id_ed25519.txt")

class Server(paramiko.ServerInterface):
    # all these functions get called automatically
    def __init__(self):
        # used to distinguish different running threads in the progrma
        self.event = threading.Event()

    # check_channel_request and check_auth_password are both need to be implemented manually
    # otherwise will return negative default

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
        logger.info("channel_exec request received: %s", cmd)
        if cmd == "banner" :
            self.banner(channel)

        elif cmd.split(' ')[0] == "echo" :
            self.echo(channel, cmd)
        else:
            return False
        return True

# these two functions give the program two different command options, either display the banner or echo back the cmd
    def banner(self, chan: paramiko.Channel):
        banner="""===== Test server banner =====
                We should include some ascii art...
            """
        banner = banner.encode("utf-8")
        chan.send(banner)


    def echo(self, chan: paramiko.Channel, cmd: str):
        cmd = cmd.encode("utf-8")
        chan.send(cmd)

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 2222))
    sock.listen(100)
    client, addr = sock.accept()

    t = paramiko.Transport(client)
    t.add_server_key(HOSTKEY_ED25519)

    # Starts the server and negotiates a new session as server
    server = Server()
    t.start_server(server=server)


    chan = t.accept(20)
    if chan is None:
        print("[Server] No channel opened.")
        t.close()
        return

    print(f"[Server] Channel opened successfully:")
    # function for retrieving username, part of paramiko
    print(t.get_username())

    server.event.wait(timeout=10)

    # Cleanly close the channel, then the transport
    chan.close()
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