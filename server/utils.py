from datetime import datetime, timedelta
from hashlib import md5
from pathlib import Path
from typing import BinaryIO
import secrets

import jwt
from fastapi import HTTPException

# 1. 密钥（线上请存环境变量，禁止写死代码）
SECRET_KEY = "your_strong_secret_key_123456"
ALGORITHM = "HS256"
# Token 有效期 2小时
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def create_access_token(data: dict):
    # 拷贝载荷，避免修改原字典
    to_encode = data.copy()
    # 设置过期时间
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # 生成 jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 解析token
def decode_token(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"verify_exp": True},  # 自动校验过期时间exp
    )

    return payload


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


def gen_random_filename(original_filename: str) -> str:
    """结合原始文件名后缀，生成随机存储文件名。"""
    suffix = Path(original_filename).suffix
    return f"{original_filename}_{secrets.token_hex(16)}{suffix}"
