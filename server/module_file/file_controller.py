from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
import mimetypes

from agent.knowledge_base import KnowledgeBase
from common.resp import BaseResp
from config import UPLOAD_DIR
from database.models import File as FileModel
from database.session import get_db
from deps.file import check_file
from deps.verify_token import verify_token
from utils.file import calc_file_md5, get_local_file, get_local_file_bytes
from utils.util import gen_random_filename
import os

file_router = APIRouter(
    prefix="/file",
    tags=["文件管理"],
    dependencies=[Depends(verify_token)],
)

SERVER_URL = os.getenv("SERVER_URL")

def check_file_existed_by_md5(file: UploadFile, db: Session) -> (str | None, str, str):
    md5_hash = calc_file_md5(file.file)
    stmt = select(FileModel).where(FileModel.md5 == md5_hash)
    db_file = db.scalar(stmt)
    if db_file is not None:
        return db_file.filepath, md5_hash
    return None, md5_hash


@file_router.post("/upload")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    existed_path, md5_hash = check_file_existed_by_md5(file, db)
    if existed_path is not None:
        return BaseResp.success(
            data={"filepath": existed_path},
            msg="文件已存在",
        )

    random_filename = gen_random_filename(file.filename)
    save_path = Path(UPLOAD_DIR) / random_filename

    content = file.file.read()
    save_path.write_bytes(content)
    mimetype, _ = mimetypes.guess_type(file.filename)

    new_file = FileModel(
        md5=md5_hash,
        original_filename=file.filename,
        filepath=str(save_path),
        filesize=len(content),
        mimetype=mimetype,
    )
    db.add(new_file)
    db.commit()
    return BaseResp.success(
        data={"filepath": new_file.filepath},
        msg="文件上传成功",
    )


@file_router.get("/")
def file_list(db: Session = Depends(get_db)):
    stmt = select(FileModel)
    files = db.scalars(stmt).all()
    data = [
        {
            "id": f.id,
            "md5": f.md5,
            "original_filename": f.original_filename,
            "filepath": f.filepath,
            "filesize": f.filesize,
            "mimetype": f.mimetype,
            "created_at": f.created_at,
            "updated_at": f.updated_at,
            "vectorized": f.vectorized,
        }
        for f in files
    ]
    return BaseResp.success(data=data)


@file_router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    stmt = select(FileModel).where(FileModel.id == file_id)
    db_file = db.scalar(stmt)
    if db_file is None:
        return BaseResp.fail(msg="文件不存在")

    file_path = Path(db_file.filepath)
    if file_path.is_file():
        file_path.unlink()

    db.delete(db_file)
    db.commit()
    return BaseResp.success(msg="文件删除成功")


@file_router.post("/vectorize/{file_id}")
def create_file_vector(
    db_file: FileModel = Depends(check_file),
    user_info: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    print("user_info: ", user_info, db_file.filepath)
    kb = KnowledgeBase()
    full_filepath = f"{SERVER_URL}/{db_file.filepath}"

    result = kb.add_knowledge(full_filepath, db_file.id, user_info["user_id"])
    db_file.vectorized = True
    db.commit()
    # print("file_bytes is ", file_content)
    msg = (
        f"重新向量化成功，替换 {result['deleted_count']} 条，新增 {result["addleted_count"]} 条"
        if result["is_update"]
        else f"向量化成功，共 {result["added_count"]} 个片段"
    )
    return BaseResp.success(
        data={
            "file_id": db_file.id,
            "original_filename": db_file.original_filename,
            "file_size": db_file.filesize,
        },
        # data={"file_id": 1, "original_filename": "tt.txt", "file_size": 123},
        msg=msg,
    )
