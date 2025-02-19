# Chat Application (GUI-based)

## 📌 Overview
This is a **real-time chat application** with a modern **GUI interface** for both **server** and **client** using `PyQt6`. Each chat session is stored in a JSON file for record-keeping.

## 🚀 Features
✅ **Server GUI:** 
- Starts the chat server and listens for incoming connections.
- Displays the chat log and allows clearing logs.
- Broadcasts messages to all connected clients.
- Saves chat messages in a JSON file.

✅ **Client GUI:**
- Allows users to connect to the server.
- Sends and receives messages in real time.
- Displays chat history in a text area.
- Saves each conversation in a separate JSON file.

## 🛠️ Installation
### 1️⃣ Install Dependencies
```bash
pip install PyQt6
```

### 2️⃣ Run the Server
```bash
python my_server.py
```

### 3️⃣ Run the Client
```bash
python client.py
```

## ⚡ Usage
1. Start the **server** first.
2. Open the **client**, enter a name, and connect.
3. Start chatting! Messages will be sent and received in real time.

## 📂 Chat Log Storage
- All messages are saved in a **chat log JSON file** (`chat_YYYY-MM-DD_HH-MM-SS.json`).
- Each chat session creates a **new file** automatically.

## 🛠️ Customization
You can **modify UI elements** and **add features** like:
- **Emojis & attachments** 📎
- **User authentication** 🔒
- **Group chats** 🗨️

## 🤝 Contributing
Pull requests are welcome! Feel free to **improve UI, optimize code, or add features.**

## 📜 License
This project is open-source. Modify and use it freely! 🚀
