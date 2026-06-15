import config  # noqa: F401 — 加载 server/.env

import os
import re

import streamlit as st

from grpc_client import register_client

EMAIL_PATTERN = re.compile(r"^.+@.+\..+$")

st.set_page_config(page_title="客户注册", page_icon="📝", layout="centered")

st.title("📝 客户注册")
st.caption("注册后即可使用文档中心智能客服")

if st.session_state.get("registered_client"):
    client = st.session_state.registered_client
    st.success(f"已注册：{client['email']}（ID: {client['id']}）")
    if st.button("继续前往客服"):
        st.switch_page("app.py")
    st.stop()

with st.form("register_form"):
    email = st.text_input("邮箱", placeholder="name@example.com")
    password = st.text_input("密码", type="password", placeholder="至少 6 位")
    submitted = st.form_submit_button("注册", type="primary", use_container_width=True)

if submitted:
    if not EMAIL_PATTERN.match(email.strip()):
        st.error("请输入有效的邮箱地址")
    elif len(password) < 6:
        st.error("密码长度至少 6 位")
    else:
        with st.spinner("注册中..."):
            try:
                client = register_client(email.strip(), password)
                st.session_state.registered_client = client
                st.success("注册成功！")
                st.rerun()
            except RuntimeError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"注册失败：{exc}")

st.divider()
st.page_link("app.py", label="已有账号？前往智能客服", icon="💬")

grpc_target = f"{os.environ.get('GRPC_HOST', '127.0.0.1')}:{os.environ.get('GRPC_PORT', '50051')}"
st.caption(f"gRPC 服务地址：{grpc_target}")
