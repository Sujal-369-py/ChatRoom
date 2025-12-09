from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import json
import uvicorn
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/static",StaticFiles(directory="frontend"),name="static")
@app.get("/") 
def home(): 
    return FileResponse("frontend/index.html")

# Mongo connection
db = AsyncIOMotorClient("mongodb+srv://UserXts_db_user:6UOSD2hon4O9dnz5@cluster0.znfwoni.mongodb.net/")["chatRoom"]
users = db["chatRoomUsers"]


connections = {}


async def broadcast(data: dict):
    """Send JSON to all clients"""
    msg = json.dumps(data)
    for ws in connections.values():
        try:
            await ws.send_text(msg)
        except:
            pass


class AddUser(BaseModel):
    username: str
    password: str


@app.post("/register")
async def register(user: AddUser):
    data = dict(user)

    if await users.find_one({"username": data["username"]}):
        return {"ok": False, "msg": "Username already exists"}

    await users.insert_one(data)
    return {"ok": True, "msg": "Account created"}


@app.post("/login")
async def login(data: dict):
    user = await users.find_one(data)
    if not user:
        return {"ok": False, "msg": "Invalid username or password"}

    return {"ok": True, "msg": "Login successful"}


@app.websocket("/ws")
async def chat_socket(ws: WebSocket):
    await ws.accept()

    # first message contains username
    init_raw = await ws.receive_text()
    init = json.loads(init_raw)
    username = init["username"]

    # close old connection if user already connected
    if username in connections:
        try:
            await connections[username].close()
        except:
            pass

    connections[username] = ws

    # announce join
    await broadcast({
        "type": "system",
        "message": f"{username} joined the chat"
    })

    try:
        while True:
            raw = await ws.receive_text()
            data = json.loads(raw)

            await broadcast({
                "type": "chat",
                "username": username,
                "message": data["message"]
            })

    except WebSocketDisconnect:
        # user left
        connections.pop(username, None)

        await broadcast({
            "type": "system",
            "message": f"{username} left the chat"
        })


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
