from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.utils.auth import verify_access_token_for_ws
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.websockets.manager import ConnectionManager
import json
from uuid import UUID

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, db: Session = Depends(get_db)):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        user = verify_access_token_for_ws(token, db)
    except HTTPException:
        await websocket.close(code=1008)
        return

    user_id = user.id
    await manager.connect(user_id, websocket)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
                to = UUID(data.get("to"))
                message = data.get("message")
                if to and message:
                    await manager.send_private_message(to, message)
            except json.JSONDecodeError:
                await websocket.send_text("Invalid message format.")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
