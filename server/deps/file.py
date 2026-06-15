from pathlib import Path

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import File as FileModel
from database.session import get_db


def check_file(file_id: int, db: Session = Depends(get_db)) -> FileModel:
    """校验数据是否存在，是否为文件"""
    stmt = select(FileModel).where(FileModel.id == file_id)
    db_file = db.scalar(stmt)
    if db_file is None:
        raise HTTPException(
            status_code=400, detail=f"文件id为 {file_id} 对应的数据不存在"
        )
    file = Path(db_file.filepath)
    if not file.is_file():
        raise HTTPException(
            status_code=400, detail=f"{db_file.original_filename}不是文件"
        )
    return db_file
