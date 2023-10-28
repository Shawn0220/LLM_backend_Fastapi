import json
from typing import Dict, List, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str: List[WebSocket]] = {}

    async def connect(self, *, user: str, websocket: WebSocket) -> bool:
        await websocket.accept()
        status = True
        other_websocket = None
        if user in self.active_connections:
            other_websocket = self.active_connections[user]
            status = False
        self.active_connections[user] = websocket
        if other_websocket is not None:
            try:
                await other_websocket.close()
            except RuntimeError:
                print(f'关闭用户{user}旧WebSocket链接')
                pass
        return status

    async def disconnect(self, *, user: str, websocket: WebSocket) -> bool:
        if user in self.active_connections:
            _websocket: WebSocket = self.active_connections[user]
            if websocket == _websocket:
                cond1 = websocket.application_state != WebSocketState.DISCONNECTED
                cond2 = websocket.client_state != WebSocketState.DISCONNECTED
                if cond1 and cond2:
                    await websocket.close()
                del self.active_connections[user]
                return True
        return False

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket:
            cond1 = websocket.application_state != WebSocketState.DISCONNECTED
            cond2 = websocket.client_state != WebSocketState.DISCONNECTED
            if cond1 and cond2:
                await websocket.send_text(message)
        else:
            raise WebSocketDisconnect()

    async def send_json(self, data: Any, websocket: WebSocket):
        if websocket:
            cond1 = websocket.application_state != WebSocketState.DISCONNECTED
            cond2 = websocket.client_state != WebSocketState.DISCONNECTED
            if cond1 and cond2:
                await websocket.send_text(json.dumps(data, ensure_ascii=False))
        else:
            raise WebSocketDisconnect()

    async def broadcast(self, data: dict):
        for user, connection in self.active_connections.items():
            await connection.send_json(data)

    async def user_send_json(self, user_id, data: Any):
        if user_id in self.active_connections:
            _websocket: WebSocket = self.active_connections[user_id]
            await self.send_json(data, _websocket)
