import json
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, Header, HTTPException, Response
from pydantic import BaseModel, Field

from module_user.user_controller import user_router
from module_file.file_controller import file_router
from pathlib import Path

from config import UPLOAD_DIR

try:
    # 自动保证目录一定存在
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    print(f"创建目录成功: {UPLOAD_DIR}")
except Exception as e:
    print(f"创建目录失败: {e}")
    raise HTTPException(status_code=500, detail=f"创建目录失败: {e}")

app = FastAPI()


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
