import os
from concurrent import futures

import grpc

from grpc_generated import client_pb2_grpc
from grpc_server.client_servicer import ClientServicer

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 50051


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_pb2_grpc.add_ClientServiceServicer_to_server(ClientServicer(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print(f"gRPC server listening on {host}:{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve(
        host=os.environ.get("GRPC_HOST", DEFAULT_HOST),
        port=int(os.environ.get("GRPC_PORT", DEFAULT_PORT)),
    )
