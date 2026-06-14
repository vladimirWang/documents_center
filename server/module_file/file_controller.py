from pathlib import Path

from fastapi import APIRouter, File, UploadFile, Depends
from database.session import get_db
from utils import calc_file_md5, gen_random_filename
from database.models import File as FileModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from common.resp import BaseResp
from config import UPLOAD_DIR

file_router = APIRouter(
    prefix="/file",
    tags=["文件管理"],
)


def check_file_existed_by_md5(file: UploadFile, db: Session) -> (str | None, str):
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

    random_filename = gen_random_filename(file.filename or "file")
    save_path = Path(UPLOAD_DIR) / random_filename

    content = file.file.read()
    save_path.write_bytes(content)

    new_file = FileModel(
        md5=md5_hash,
        original_filename=file.filename,
        filepath=str(save_path),
        filesize=len(content),
        filetype=file.content_type or "",
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
            "filetype": f.filetype,
            "created_at": f.created_at,
            "updated_at": f.updated_at,
        }
        for f in files
    ]
    return BaseResp.success(data=data)