import threading
import websocket
import sys
import json
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from websocket import WebSocketConnectionClosedException

# 🌍 MongoDB connection (update this for Render)
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["chatRoom"]["chatRoomUsers"]

# ⚙️ Handle new or existing user
async def get_user():
    while True:
        choice = input("1️⃣  New user\n2️⃣  Existing user\nChoose (1/2): ").strip()

        if choice == "1":
            # new user creation
            while True:
                name = input("Enter a new username: ").strip()
                if await db.find_one({"username": name}):
                    print("❌ Username already exists. Try another.")
                else:
                    await db.insert_one({"username": name, "online": "True"})
                    print("✅ Account created and logged in.")
                    return name

        elif choice == "2":
            # existing user login
            while True:
                name = input("Enter your username (or type 'back' to go back): ").strip()
                if name.lower() == "back":
                    break  # go back to main menu
                if await db.find_one({"username": name}):
                    await db.update_one({"username": name}, {"$set": {"online": "True"}})
                    print(f"✅ Welcome back, {name}!")
                    return name
                else:
                    print("❌ Username not found. Try again or type 'back' to return.")

        else:
            print("Please enter 1 or 2.")

# 🔒 Lock for thread-safe console output
lock = threading.Lock()

# 📥 Receive messages from WebSocket
def receive(ws, username):
    while True:
        try:
            msg = ws.recv()
        except WebSocketConnectionClosedException:
            print("\n[⚠️ Server disconnected]")
            break

        data = json.loads(msg)
        sender = data.get("username")
        text = data.get("message")

        if sender != username:
            with lock:
                sys.stdout.write(f"\r{sender}: {text}\nYou: ")
                sys.stdout.flush()

# 🚀 Main chat function
def main(username):
    # replace with your deployed Render URL
    WS_URL = os.getenv("WS_URL", "wss://your-render-app.onrender.com/wss")

    ws = websocket.WebSocket()
    ws.connect(WS_URL)
    print("✅ Connected! Start chatting...")

    # notify server user joined
    ws.send(json.dumps({"type": "join", "username": username}))

    print("You: ", end="", flush=True)
    threading.Thread(target=receive, args=(ws, username), daemon=True).start()

    try:
        while True:
            msg = input()
            payload = json.dumps({"username": username, "message": msg})
            ws.send(payload)
            print("You: ", end="", flush=True)
    except KeyboardInterrupt:
        asyncio.run(db.update_one({"username": username}, {"$set": {"online": "False"}}))
        ws.close()
        print("\n[👋 You left the chat]")

# 🧠 Entry point
if __name__ == "__main__":
    username = asyncio.run(get_user())
    main(username)

