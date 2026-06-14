import json
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, Header, HTTPException, Response
from pydantic import BaseModel, Field

from module_user.user_controller import user_router
from utils import create_access_token, decode_token

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
