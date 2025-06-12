from fastapi import WebSocket
from typing import Dict
from uuid import UUID

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, WebSocket] = {}

    async def connect(self, user_id: UUID, websocket: WebSocket):
        print(f"🔗 Registering user_id: {user_id}")
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: UUID):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_private_message(self, user_id: UUID, message: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)
        else:
            print(f"⚠️ User {user_id} not connected")
