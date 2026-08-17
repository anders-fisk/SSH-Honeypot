from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import load_ssh_private_key

import os
# add terminal confirmations for this method

def generate_host_key() :
    directory_name = "keys"
    key_path = "keys/host_key"

    # checks for multiple possible directory errors
    try :
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        pass
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            host_key = load_ssh_private_key(f.read(), password=None)

    else:
        # generates the ed251 private host key
        host_key = ed25519.Ed25519PrivateKey.generate()
        # serialises the key with no password
        pem = (host_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            encryption_algorithm=serialization.NoEncryption()
        ))

        # writes the key to the file
        with open(key_path, "wb") as f:
            f.write(pem)
