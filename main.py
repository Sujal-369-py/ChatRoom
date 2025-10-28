from fastapi import FastAPI, WebSocket
import json
import uvicorn

app = FastAPI()

clients = []               # all connected sockets
connected_users = {}       # map websocket → username


@app.get("/")
def home():
    return {"status": "✅ WebSocket chat server running"}


@app.websocket("/wss")
async def chat(websocket: WebSocket):
    await websocket.accept()

    # 🔹 first message from client (join event)
    data = await websocket.receive_text()
    msg = json.loads(data)

    if msg.get("type") == "join":
        username = msg["username"]
        connected_users[websocket] = username
        clients.append(websocket)
        print(f"{username} joined the chat")

        # 🔸 broadcast join notice
        join_notice = json.dumps({
            "username": "System",
            "message": f"{username} joined the chat"
        })
        for client in clients:
            if client != websocket:
                await client.send_text(join_notice)

    try:
        while True:
            data = await websocket.receive_text()
            # broadcast normal chat messages to others
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except:
        # 🔹 when someone disconnects
        if websocket in clients:
            clients.remove(websocket)
        user = connected_users.pop(websocket, None)
        if user:
            print(f"{user} left the chat")

            # 🔸 broadcast leave notice
            leave_notice = json.dumps({
                "username": "System",
                "message": f"{user} left the chat"
            })
            for client in clients:
                await client.send_text(leave_notice)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
