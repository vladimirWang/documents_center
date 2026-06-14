import jwt
from fastapi import Header, HTTPException

from utils import decode_token


# token认证
def verify_token(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="缺少Token")
    # 2. 分割 Bearer 前缀，标准格式：Bearer xxx.xxx.xxx
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token格式错误")
    token = parts[1]
    # print(f"token is {token}")
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token已过期，请重新登录")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="非法无效Token")
    if not payload.get("user_id"):
        raise HTTPException(status_code=401, detail="Token载荷缺失用户信息")
    return payload
