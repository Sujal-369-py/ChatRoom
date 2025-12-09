# 🔵 Realtime Chat Application (FastAPI + WebSockets + MongoDB)

A fully functional realtime chat application built from scratch using FastAPI, WebSockets, and MongoDB.  
Includes authentication, realtime messaging, system notifications, and a responsive modern UI.

## 🚀 Features
- User Signup & Login
- MongoDB for credential storage
- Realtime chat with WebSockets
- Broadcast messages to all users
- System join/leave notifications
- Enter-to-send messages
- Auto-scroll chat window
- Modern dark UI, mobile responsive

## 🛠️ Tech Stack
- FastAPI
- WebSockets (FastAPI native)
- MongoDB + Motor
- HTML, CSS, JavaScript
- Render (Deployment)

## 🧠 Architecture Overview

### Active WebSocket Connections

```python
connections = {
    "username": websocket
}
```

Used for:
- Identifying online users  
- Broadcasting messages  
- Sending join/leave system events  

### Message Flow
User → WebSocket → FastAPI → Broadcast → Frontend UI updates

### Example Chat Message
```json
{
  "type": "chat",
  "username": "Sujal",
  "message": "Hello!"
}
```

### Example System Event
```json
{
  "type": "system",
  "message": "Sujal joined the chat"
}
```

## 📂 Project Structure
```
/chatRoom
│── main.py
│── requirements.txt
│── index.html
│── style.css
│── script.js
```

## ⚙️ Running Locally

### Clone repo
```bash
git clone https://github.com/YOUR-USERNAME/ChatRoom.git
cd ChatRoom
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set MongoDB connection
Windows:
```powershell
setx MONGO_URL "your_mongodb_connection_string"
```
Linux/Mac:
```bash
export MONGO_URL="your_mongodb_connection_string"
```

### Start backend
```bash
uvicorn main:app --reload
```

### Open app
```
http://localhost:8000
```

## 🌐 Deployment (Render)

Environment variable:
```
MONGO_URL = your_connection_string
```

Start command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📌 Future Enhancements
- Chat history (MongoDB)
- Message timestamps
- Typing indicator
- Left/right chat bubbles
- Online users list
- Private messages (DMs)
- Chat rooms
- JWT authentication
- User avatars

## 📝 Why I Built This
"I built this to understand how realtime chat systems like WhatsApp work internally.  
This project taught me WebSockets, async programming, broadcasting, and frontend-backend sync."

## 🙌 Author
**Sujal **  
GitHub: https://github.com/Sujal-369-py
