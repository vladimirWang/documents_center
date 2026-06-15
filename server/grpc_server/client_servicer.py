import grpc

from grpc_generated import client_pb2, client_pb2_grpc
from database.session import SessionLocal
from module_client.client_service import register_client


class ClientServicer(client_pb2_grpc.ClientServiceServicer):
    def Register(self, request, context):
        db = SessionLocal()
        try:
            db_client = register_client(db, request.email, request.password)
            return client_pb2.RegisterResponse(
                code=200,
                message="注册成功",
                client=client_pb2.ClientInfo(
                    id=db_client.id,
                    email=db_client.email,
                    mobile=db_client.mobile,
                    created_at=db_client.created_at.isoformat(),
                    updated_at=db_client.updated_at.isoformat(),
                ),
            )
        except ValueError as exc:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(str(exc))
            return client_pb2.RegisterResponse(code=400, message=str(exc))
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            return client_pb2.RegisterResponse(code=500, message="注册失败")
        finally:
            db.close()
