"""Basic server for password auth."""
from src.keypair import generate_host_key
import logging
import threading
import paramiko
import socket

# different variables for different keys in byte form
UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = b'\x7f'

# chan.send sends stuff to terminal screen, commands need to be handled differently

# Set up logging globally.
# basically an alternative for print, just puts DEBUG before everything
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
# silences paramikos logger
logging.getLogger("paramiko").setLevel(logging.WARNING)

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
        return paramiko.AUTH_SUCCESSFUL

# if program runs with a command
    # have to rework this
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

    def check_channel_shell_request(self, channel):
        # Allow the user to get a shell
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
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
        chan.send(b"\r\n")

    def whoami(self, chan: paramiko.Channel, cmd: str):
        cmd = cmd.encode("utf-8")
        chan.send(b"root")
        chan.send(b"\r\n")

def shell_env(server,chan, t):
    try:
        chan.send(b"Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-128-generic x86_64)\r\n\r\n")
        run = True
        while run:
            chan.send(b"$ ")
            command = ""
            while not command.endswith("\r"):
                # byte form
                transport = chan.recv(1024)
                print("PLACEHOLDER_FOR_IP" + "- received:", transport)
                # handles backspace character and end charactetr erasing
                if transport == BACK_KEY :
                    chan.send(b"\x08 \x08")
                    command = command[:-1]

                elif (
                        transport != UP_KEY
                        and transport != DOWN_KEY
                        and transport != LEFT_KEY
                        and transport != RIGHT_KEY
                ):
                    chan.send(transport)
                    command += transport.decode("utf-8")

            # puts curson at start of line
            chan.send(b"\r\n")
            # remoces any endspace characteres
            command = command.rstrip()
            logging.info('Command receied ({}): {}'.format("PLACEHOLDER_IP", command))

            if "exit" in command:
                print("Connection closed (via exit command): " + "PLACEHOLDER_IP" + "\n")
                run = False

            elif "echo" in command:
                server.echo(chan, command)

            elif "whoami" in command:
                server.whoami(chan, command)

            else:
                print(command + " PLACEHOLDER_IP")

    except Exception as err:
        print('!!! Exception: {}: {}'.format(err.__class__, err))
    finally:
        try:
            chan.close()
        except Exception:
            pass
        try:
            t.close()
        except Exception:
            pass

def listen():
    # generates key_pair
    generate_host_key()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 2222))
    sock.listen(100)
    client, addr = sock.accept()
    t = paramiko.Transport(client)

    # presents the client with a host key to add to known hosts
    # sign(H, private_key)   = H raised to a secret power, mod some number
    # verify(signature, public_key) = signature raised to the public power, mod the same number
    # use ed25519 since smaller, faster, more modern, less vulnerabilities

    HOSTKEY_ED25519 = paramiko.Ed25519Key(filename="keys/host_key")

    t.add_server_key(HOSTKEY_ED25519)

    # Starts the server and negotiates a new session as server
    server = Server()
    t.start_server(server=server)


    chan = t.accept()
    if chan is None:
        print("[Server] No channel opened.")
        t.close()
        return

    print(f"[Server] Channel opened successfully:")
    # function for retrieving username, part of paramiko
    print(t.get_username())

    # run shell environment
    shell_env(server, chan, t)

    chan.close()
    t.close()