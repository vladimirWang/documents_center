from datetime import datetime, timedelta
from hashlib import md5
from pathlib import Path
from typing import BinaryIO


def calc_file_md5(source: str | Path | BinaryIO, chunk_size: int = 8192) -> str:
    """计算文件 MD5，支持文件路径或二进制流（如 UploadFile.file）。"""
    hasher = md5()

    if isinstance(source, (str, Path)):
        with open(source, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hasher.update(chunk)
    else:
        pos = source.tell()
        try:
            source.seek(0)
            for chunk in iter(lambda: source.read(chunk_size), b""):
                hasher.update(chunk)
        finally:
            source.seek(pos)

    return hasher.hexdigest()


def get_local_file_bytes(filepath: str) -> bytes:
    """获取本地文件的二进制数据"""
    with open(filepath, "rb") as f:
        return f.read()

def get_local_file(filepath: str) -> str:
    """获取本地文件的二进制数据"""
    with open(filepath, "r") as f:
        return f.read()