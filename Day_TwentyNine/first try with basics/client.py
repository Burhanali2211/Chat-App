import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, colorchooser
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 55555        # The port used by the server


class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("Chat Application")
        self.master.geometry("400x500")

        self.name = simpledialog.askstring(
            "Name", "Please enter your name:", parent=master)
        if not self.name:
            master.destroy()
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        self.client_socket.send(bytes(self.name, 'ascii'))

        self.chat_transcript_area = scrolledtext.ScrolledText(
            master, wrap=tk.WORD, width=40, height=20)
        self.chat_transcript_area.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5)

        self.message_entry = tk.Entry(master, width=30)
        self.message_entry.grid(row=1, column=0, padx=5, pady=5)
        self.send_button = tk.Button(
            master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        self.receive_thread = threading.Thread(
            target=self.receive, daemon=True)
        self.receive_thread.start()

        self.user_list = tk.Listbox(master, width=20)
        self.user_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.update_user_list_thread = threading.Thread(
            target=self.update_user_list, daemon=True)
        self.update_user_list_thread.start()

        self.emoticon_button = tk.Button(
            master, text="😊", command=self.insert_emoticon)
        self.emoticon_button.grid(row=3, column=0, padx=5, pady=5)

        self.clear_button = tk.Button(
            master, text="Clear Chat", command=self.clear_chat)
        self.clear_button.grid(row=3, column=1, padx=5, pady=5)

        self.font_size = 10
        self.font_size_button = tk.Button(
            master, text="Font Size", command=self.change_font_size)
        self.font_size_button.grid(row=4, column=0, padx=5, pady=5)

        self.color_button = tk.Button(
            master, text="Color", command=self.change_color)
        self.color_button.grid(row=4, column=1, padx=5, pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def send_message(self):
        message = f"{self.name}: {self.message_entry.get()}"
        print(f"Sending message: {message}")  # Debug print
        try:
            self.client_socket.send(bytes(message, 'ascii'))
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('ascii')
                print(f"Received message: {message}")  # Debug print
                if message == "{quit}":
                    self.client_socket.close()
                    self.master.quit()
                    break
                self.chat_transcript_area.insert(tk.END, message + "\n")
                self.chat_transcript_area.yview(tk.END)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def update_user_list(self):
        while True:
            time.sleep(5)  # Update every 5 seconds
            self.user_list.delete(0, tk.END)
            try:
                self.client_socket.send(bytes("{get_users}", 'ascii'))
                user_list = self.client_socket.recv(
                    1024).decode('ascii').split(',')
                for user in user_list:
                    self.user_list.insert(tk.END, user)
            except Exception as e:
                print(f"Error updating user list: {e}")
                break

    def insert_emoticon(self):
        self.message_entry.insert(tk.END, "😊")

    def clear_chat(self):
        self.chat_transcript_area.delete(1.0, tk.END)

    def change_font_size(self):
        self.font_size += 2
        self.chat_transcript_area.configure(font=("Arial", self.font_size))

    def change_color(self):
        color = colorchooser.askcolor(title="Choose color")[1]
        if color:
            self.chat_transcript_area.tag_config('color', foreground=color)
            self.chat_transcript_area.tag_add('color', '1.0', 'end')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.client_socket.send(bytes("{quit}", 'ascii'))
            except:
                pass  # If sending fails, we're probably already disconnected
            self.master.destroy()


root = tk.Tk()
client = ChatClient(root)
root.mainloop()
