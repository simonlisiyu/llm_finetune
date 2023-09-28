import websockets.server
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# WebSocket route
@app.websocket("/logs")
async def websocket_endpoint(websocket: websockets.server.WebSocketServerProtocol):
    while True:
        # Read log data from file or any other source
        # For this example, let's assume logs is a list of log messages
        logs = ["Log message 1", "Log message 2", "Log message 3"]

        # Send logs to the WebSocket client
        await websocket.send("\n".join(logs))

        # Wait for some time before sending the next update
        await asyncio.sleep(1)

# Main route
@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
