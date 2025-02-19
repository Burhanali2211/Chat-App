import socket
import threading
import json
import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit

HOST = '127.0.0.1'  # Server IP
PORT = 55555  # Server Port


class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_ui()
        self.username = None
        self.chat_log = []
        self.chat_filename = f"chat_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

    def init_ui(self):
        self.setWindowTitle('Chat Client')
        self.setGeometry(500, 200, 400, 400)

        layout = QVBoxLayout()
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.msg_input = QLineEdit()
        self.send_btn = QPushButton('Send')
        self.send_btn.clicked.connect(self.send_message)
        self.connect_btn = QPushButton('Connect')
        self.connect_btn.clicked.connect(self.connect_to_server)

        layout.addWidget(self.chat_area)
        layout.addWidget(self.msg_input)
        layout.addWidget(self.send_btn)
        layout.addWidget(self.connect_btn)
        self.setLayout(layout)

    def connect_to_server(self):
        try:
            self.client.connect((HOST, PORT))
            # Generate a unique username
            self.username = "User" + str(datetime.now().timestamp())[:5]
            self.client.send(self.username.encode('utf-8'))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.chat_area.append(f"Connected as {self.username}")
        except Exception as e:
            self.chat_area.append(f"❌ Connection failed: {e}")

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode('utf-8')
                self.chat_area.append(msg)
                self.save_message(msg)
            except Exception as e:
                self.chat_area.append(f"Error receiving message: {e}")
                break

    def send_message(self):
        msg = self.msg_input.text()
        if msg:
            try:
                self.client.send(msg.encode('utf-8'))
                self.msg_input.clear()
            except:
                self.chat_area.append("❌ Failed to send message")

    def save_message(self, msg):
        self.chat_log.append(msg)
        with open(self.chat_filename, 'w') as file:
            json.dump(self.chat_log, file, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_gui = ClientGUI()
    client_gui.show()
    sys.exit(app.exec())
