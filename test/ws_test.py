import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
import websockets.server

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 日志文件路径
log_file_path = "output.log"

# 存储已连接的 WebSocket 客户端
connected_clients = set()

# 异步任务：读取日志文件并发送到 WebSocket 客户端
async def read_log_file():
    while True:
        try:
            with open(log_file_path, "r") as file:
                log_content = file.read()

            # 发送日志内容给所有连接的客户端
            for client in connected_clients:
                await client.send(log_content)

            # 等待一段时间后继续读取日志文件
            await asyncio.sleep(1)
        except:
            pass

# WebSocket 路由：建立连接
@app.websocket("/logs")
async def websocket_endpoint(websocket: websockets.server.WebSocketServerProtocol):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        # 不断接收客户端消息并忽略
        while True:
            await websocket.receive()
    except websockets.exceptions.ConnectionClosed:
        connected_clients.remove(websocket)

# Web 页面路由：渲染模板
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 启动异步任务和 FastAPI 应用
if __name__ == "__main__":
    asyncio.create_task(read_log_file())
    uvicorn.run(app, host="0.0.0.0", port=8000)
