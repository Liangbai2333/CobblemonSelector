import os
import threading

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_path = os.getcwd()

# 捕获前端路由请求，返回index.html
@app.get("/{full_path:path}")
async def serve_index(full_path: str):
    # 如果请求有扩展名(如.js、.css等)，尝试提供此文件
    if "." in full_path:
        file_path = os.path.join(root_path, "templates", full_path)
        if os.path.exists(file_path):
            return FileResponse(file_path)

    # 没有扩展名的路径(前端路由)或找不到的文件，返回index.html
    return FileResponse(os.path.join(root_path, "templates", "index.html"))


def run_server(port: int):
    """在后台线程中运行uvicorn服务器"""
    uvicorn.run("plugins.server.server:app", host="localhost", port=port)


def bootstrap(port: int):
    """非阻塞地启动服务器"""
    # 创建线程并启动
    thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    thread.start()

    return thread

