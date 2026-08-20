from flask import Flask, render_template
from pyngrok import ngrok
import socket
import threading
import time

app = Flask(__name__)

latest_data = []
data_lock = threading.Lock()

ngrok.set_auth_token("XXXX")
tcp_tunnel = ngrok.connect(4999, "tcp")

print(f"Public Ngrok Address: {tcp_tunnel.public_url}")



def get_ip_address():
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind(("localhost", 4999))
    local_socket.listen(1)
    while True:
        print("Waiting for data from cloud server...")
        connection, client_address = local_socket.accept()

        data = connection.recv(1024).decode()
        print(f"Received message: {data}")

        with data_lock:
            latest_data.append(data)

        time.sleep(1)  # however often it updates


@app.route('/')
def index():
    return render_template('index.html')

#db = DatabaseModel()
# add data to database
# db.insert_data(ip)
# show all data
# print(db.show_all_data())