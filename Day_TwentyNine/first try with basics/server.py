import socket
import threading
import time

HOST = '127.0.0.1'  # Localhost
PORT = 55555        # Port to listen on

clients = {}
addresses = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


def accept_incoming_connections():
    """Handles new client connections"""
    while True:
        try:
            client, client_address = server.accept()
            print(f"{client_address} has connected.")
            addresses[client] = client_address
            threading.Thread(target=handle_client, args=(
                client,), daemon=True).start()
        except Exception as e:
            print(f"Error accepting connection: {e}")


def handle_client(client):
    """Handles a single client connection."""

    name = client.recv(1024).decode('ascii')
    clients[client] = name

    welcome = f'Welcome {name}! If you ever want to quit, type {{quit}} to exit.'
    client.send(bytes(welcome, 'ascii'))
    broadcast(f"{name} has joined the chat!")

    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == "{quit}":
                client.send(bytes("{quit}", "ascii"))
                client.close()
                del clients[client]
                broadcast(f"{name} has left the chat.")
                break
            elif msg == "{get_users}":
                handle_user_list_request(client)
            else:
                print(f"Broadcasting message: {msg}")  # Debug print
                broadcast(f"{name}: {msg}", client)
        except Exception as e:
            print(f"Error in client {name}: {e}")
            client.close()
            del clients[client]
            broadcast(f"{name} has left the chat.")
            break


def handle_user_list_request(client):
    """Sends the list of connected users to the requesting client."""
    user_list = ','.join(clients.values())
    try:
        client.send(bytes(user_list, 'ascii'))
    except Exception as e:
        print(f"Error sending user list to {clients[client]}: {e}")


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients except the sender."""
    for sock in list(clients.keys()):
        try:
            if clients[sock] != msg.split(':')[0]:  # Don't send to sender
                sock.send(bytes(prefix + msg, 'ascii'))
        except Exception as e:
            print(f"Error broadcasting to {clients[sock]}: {e}")


if __name__ == "__main__":
    print("Waiting for connection...")
    ACCEPT_THREAD = threading.Thread(
        target=accept_incoming_connections, daemon=True)
    ACCEPT_THREAD.start()
    try:
        ACCEPT_THREAD.join()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        for client in clients:
            client.close()
        server.close()
