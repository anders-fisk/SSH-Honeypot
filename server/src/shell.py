import logging

# different variables for different keys in byte form
UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = b'\x7f'

def shell_env(server,chan, username, ip_address):
    try:
        chan.send(b"Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-128-generic x86_64)\r\n\r\n")
        run = True
        packet_count = 0

        while run:
            # makes sure bash symbol doesn't get erased
            cursor_count = 0
            # implement packet limit

            chan.send(b"$ ")
            command = ""
            while not command.endswith("\r"):
                # byte form
                received_bytes = chan.recv(1024)
                print("{}@{} ".format(username, ip_address) + "- received:", received_bytes)
                # handles backspace character and end charactetr erasing
                if packet_count > 500 :
                    print('MAXIMUM PACKET LIMIT REACHED')
                    raise Exception("MAXIMUM PACKET REACHED")

                elif BACK_KEY in received_bytes and cursor_count > 0:
                    cursor_count -= 1
                    chan.send(b"\x08 \x08")
                    command = command[:-1]

                elif (
                        received_bytes != UP_KEY
                        and received_bytes != DOWN_KEY
                        and received_bytes != LEFT_KEY
                        and received_bytes != RIGHT_KEY
                        and BACK_KEY not in received_bytes
                ):
                    cursor_count += 1
                    packet_count += 1

                    chan.send(received_bytes)
                    # error checking for b''
                    decoded_bytes = received_bytes.decode("utf-8")
                    if decoded_bytes == b'' :
                        run = False
                        break
                    else :
                        command += decoded_bytes

            # puts curson at start of line
            chan.send(b"\r\n")
            # remoces any endspace characteres
            command = command.rstrip()
            logging.info('Command receied ({}): {}'.format("PLACEHOLDER_IP", command))

            if "exit" == command.split(' ')[0]:
                print("Connection closed (via exit command): " + "PLACEHOLDER_IP" + "\n")
                run = False

            elif "echo" == command.split(' ')[0]:
                server.echo(chan, command)

            elif "whoami" in command.split(' ')[0]:
                server.whoami(chan, command)

    except Exception as err:
        print('!!! Exception: {}: {}'.format(err.__class__, err))
    finally:
        try:
            chan.close()
        except Exception:
            pass