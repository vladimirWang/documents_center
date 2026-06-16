import json
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import Depends, FastAPI, Header, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from config import UPLOAD_DIR
from grpc_server.server import DEFAULT_HOST, DEFAULT_PORT, create_server
from module_chat.chat_controller import chat_router
from module_client.client_controller import client_router
from module_file.file_controller import file_router
from module_product.product_controller import product_router
from module_user.user_controller import user_router
from module_order.order_controller import order_router

try:
    # 自动保证目录一定存在
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    print(f"创建目录成功: {UPLOAD_DIR}")
except Exception as e:
    print(f"创建目录失败: {e}")
    raise HTTPException(status_code=500, detail=f"创建目录失败: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    host = os.environ.get("GRPC_HOST", DEFAULT_HOST)
    port = int(os.environ.get("GRPC_PORT", DEFAULT_PORT))
    grpc_server = create_server(host, port)
    grpc_server.start()
    print(f"gRPC server listening on {host}:{port}")
    yield
    grpc_server.stop(grace=5)


app = FastAPI(lifespan=lifespan)

# @app.middleware("http")
# async def global_exception_middleware(request: Request, call_next):
#     try:
#         response = await call_next(request)
#         return response
#     except Exception as e:
#         print(f"全局异常: {e}")
#         return JSONResponse(status_code=500, content={"message": "服务器内部错误"})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"全局异常: {exc}")
    return JSONResponse(status_code=500, content={"message": "服务器内部错误"})
@app.get("/")
def root():
    return {"message": "Hello World222"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/response")
def response():
    return Response(status_code=201, content=json.dumps({"success": "ok"}))


app.include_router(user_router)
app.include_router(file_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(chat_router)
app.include_router(order_router)
# 在创建 app 和 include_router 之后添加
app.mount("/statics", StaticFiles(directory="statics"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
