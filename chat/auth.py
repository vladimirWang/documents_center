import json
import os
import urllib.error
import urllib.request

import streamlit as st

AUTH_USER_KEY = "auth_user"
SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:8000").rstrip("/")
API_PREFIX = "/api"


def _read_error(exc: urllib.error.HTTPError) -> str:
    raw = exc.read().decode()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw or str(exc)
    detail = payload.get("detail") or payload.get("message") or str(exc)
    if isinstance(detail, list):
        return "；".join(str(item.get("msg", item)) for item in detail)
    return str(detail)


def _request(
    method: str,
    path: str,
    body: dict | None = None,
    token: str | None = None,
) -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"{SERVER_URL}{API_PREFIX}{path}",
        data=data,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(_read_error(exc)) from exc


def login(email: str, password: str) -> dict:
    resp = _request("POST", "/user/login", {"email": email, "password": password})
    if resp.get("code") != 200:
        raise RuntimeError(resp.get("message") or "登录失败")

    token = resp["data"]
    user_info = _request("GET", "/user/user_info", token=token)
    user = {
        "user_id": user_info["user_id"],
        "username": user_info.get("username") or email,
        "email": email,
        "token": token,
    }
    st.session_state[AUTH_USER_KEY] = user
    return user


def register(email: str, password: str) -> None:
    resp = _request("POST", "/user/register", {"email": email, "password": password})
    if resp.get("code") != 200:
        raise RuntimeError(resp.get("message") or "注册失败")


def logout() -> None:
    st.session_state.pop(AUTH_USER_KEY, None)


def get_current_user() -> dict | None:
    return st.session_state.get(AUTH_USER_KEY)


def require_login() -> dict:
    user = get_current_user()
    if user:
        return user

    st.warning("请先登录后再使用智能客服")
    link_col1, link_col2 = st.columns(2)
    with link_col1:
        st.page_link("pages/login.py", label="前往登录", icon="🔐")
    with link_col2:
        st.page_link("pages/register.py", label="注册账号", icon="📝")
    st.stop()
