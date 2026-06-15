from datetime import datetime, timedelta
from hashlib import md5
from pathlib import Path
from typing import BinaryIO
import re
from urllib.parse import urlparse

import httpx


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

def read_filepath_bytes_sync(filepath: str) -> bytes:
    """支持 http(s) URL 或本地文件路径（同步，供 gRPC 等非 async 上下文使用）。"""
    if filepath.startswith(("http://", "https://")):
        try:
            with httpx.Client(timeout=30.0) as client:
                r = client.get(filepath)
                r.raise_for_status()
                return r.content
        except httpx.HTTPError as e:
            raise OSError(f"拉取远程文件失败: {e}") from e
    path = Path(filepath)
    if not path.is_file():
        raise ValueError("本地文件不存在或不是文件")
    return path.read_bytes()