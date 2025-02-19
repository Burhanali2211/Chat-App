import socket
import threading
import json
import os
import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel

HOST = '127.0.0.1'  # Localhost
PORT = 55555  # Port to listen on
clients = {}
addresses = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

chat_log = []
chat_filename = f"chat_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"


def save_message(msg):
    global chat_log
    chat_log.append(msg)
    with open(chat_filename, 'w') as file:
        json.dump(chat_log, file, indent=4)


def accept_connections():
    while True:
        client, client_address = server.accept()
        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(
            client,), daemon=True).start()


def handle_client(client):
    try:
        name = client.recv(1024).decode('utf-8')
        clients[client] = name
        broadcast(f"{name} has joined the chat!")

        while True:
            msg = client.recv(1024).decode('utf-8')
            if msg == "{quit}":
                client.send("{quit}".encode('utf-8'))
                client.close()
                del clients[client]
                broadcast(f"{name} has left the chat.")
                break
            elif msg == "{get_users}":
                user_list = ', '.join(clients.values())
                client.send(user_list.encode('utf-8'))
            else:
                save_message(f"{name}: {msg}")
                broadcast(f"{name}: {msg}", client)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client.close()
        if client in clients:
            del clients[client]


def broadcast(msg, sender=None):
    for sock in list(clients.keys()):
        if sock != sender:
            try:
                sock.send(msg.encode('utf-8'))
            except:
                sock.close()
                del clients[sock]


class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Chat Server')
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()
        self.label = QLabel('Chat Server Running...')
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.clear_btn = QPushButton('Clear Log')
        self.clear_btn.clicked.connect(self.clear_log)

        layout.addWidget(self.label)
        layout.addWidget(self.log_area)
        layout.addWidget(self.clear_btn)
        self.setLayout(layout)

        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        self.log("Server started...")
        accept_thread = threading.Thread(
            target=accept_connections, daemon=True)
        accept_thread.start()
        accept_thread.join()

    def log(self, message):
        self.log_area.append(message)

    def clear_log(self):
        self.log_area.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    server_gui = ServerGUI()
    server_gui.show()
    sys.exit(app.exec())
