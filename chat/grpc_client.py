import config  # noqa: F401 — 初始化环境变量与 server 模块路径

import os

import grpc

from grpc_generated import chat_pb2, chat_pb2_grpc, client_pb2, client_pb2_grpc

DEFAULT_GRPC_HOST = "127.0.0.1"
DEFAULT_GRPC_PORT = "50051"


def _get_target() -> str:
    host = os.environ.get("GRPC_HOST", DEFAULT_GRPC_HOST)
    port = os.environ.get("GRPC_PORT", DEFAULT_GRPC_PORT)
    return f"{host}:{port}"


def ask_chat(question: str) -> str:
    with grpc.insecure_channel(_get_target()) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        try:
            response = stub.Ask(
                chat_pb2.ChatRequest(question=question),
                timeout=120,
            )
        except grpc.RpcError as exc:
            detail = exc.details() or "聊天服务不可用"
            raise RuntimeError(detail) from exc

        if response.code != 200:
            raise RuntimeError(response.message or "聊天失败")

        return response.answer


def register_client(email: str, password: str) -> dict:
    with grpc.insecure_channel(_get_target()) as channel:
        stub = client_pb2_grpc.ClientServiceStub(channel)
        try:
            response = stub.Register(
                client_pb2.RegisterRequest(email=email, password=password),
                timeout=10,
            )
        except grpc.RpcError as exc:
            detail = exc.details() or "注册失败"
            raise RuntimeError(detail) from exc

        if response.code != 200:
            raise RuntimeError(response.message or "注册失败")

        return {
            "id": response.client.id,
            "email": response.client.email,
            "mobile": response.client.mobile,
            "created_at": response.client.created_at,
            "updated_at": response.client.updated_at,
        }
