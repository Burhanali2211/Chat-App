import socket
import threading
import sys
import json
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit, QLabel

HOST = '127.0.0.1'  # Server address
PORT = 55555  # Port to connect to


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chat Client")
        self.setGeometry(500, 200, 400, 400)

        layout = QVBoxLayout()
        self.label = QLabel("Enter your name:")
        self.name_input = QLineEdit()
        self.join_button = QPushButton("Join Chat")
        self.join_button.clicked.connect(self.connect_to_server)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.message_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.users_button = QPushButton("Get Active Users")
        self.users_button.clicked.connect(self.get_users)

        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.join_button)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.users_button)

        self.setLayout(layout)
        self.message_input.setDisabled(True)
        self.send_button.setDisabled(True)
        self.users_button.setDisabled(True)

    def connect_to_server(self):
        try:
            self.client_socket.connect((HOST, PORT))
            self.username = self.name_input.text().strip()
            if not self.username:
                self.chat_display.append("⚠️ Please enter a valid name.")
                return

            self.client_socket.send(self.username.encode('utf-8'))
            self.chat_display.append(f"✅ Connected as {self.username}")
            self.name_input.setDisabled(True)
            self.join_button.setDisabled(True)
            self.message_input.setDisabled(False)
            self.send_button.setDisabled(False)
            self.users_button.setDisabled(False)

            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.chat_display.append(f"❌ Connection failed: {e}")

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if msg == "{quit}":
                    self.client_socket.close()
                    break
                self.chat_display.append(msg)
                self.save_message(msg)
            except Exception as e:
                self.chat_display.append(f"⚠️ Error receiving message: {e}")
                break

    def send_message(self):
        msg = self.message_input.text().strip()
        if msg:
            self.client_socket.send(msg.encode('utf-8'))
            self.message_input.clear()

    def get_users(self):
        self.client_socket.send("{get_users}".encode('utf-8'))

    def save_message(self, msg):
        chat_filename = f"chat_{datetime.now().strftime('%Y-%m-%d')}.json"
        try:
            with open(chat_filename, 'a') as file:
                json.dump(
                    {"message": msg, "timestamp": datetime.now().isoformat()}, file)
                file.write('\n')
        except Exception as e:
            self.chat_display.append(f"⚠️ Error saving message: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_gui = ChatClient()
    client_gui.show()
    sys.exit(app.exec())
