""" テスト用のgrpc server """
from concurrent import futures

import grpc

from quickmpc.proto import libc_to_manage_pb2, libc_to_manage_pb2_grpc


class LibToManageServiceServicer(libc_to_manage_pb2_grpc.LibcToManageServicer):

    def __init__(self): ...

    def SendShares(self, request, context):
        res = libc_to_manage_pb2.SendSharesResponse(
            message="ok",
            is_ok=True
        )
        return res

    def DeleteShares(self, request, context):
        res = libc_to_manage_pb2.DeleteSharesResponse(
            message="ok",
            is_ok=True
        )
        return res

    def ExecuteComputation(self, request, context):
        res = libc_to_manage_pb2.ExecuteComputationResponse(
            message="ok",
            is_ok=True,
            job_uuid="jobjobjob"
        )
        return res

    def GetComputationResult(self, request, context):
        yield libc_to_manage_pb2.GetComputationResultResponse(
            message="ok",
            is_ok=True,
            result="['1',",
            piece_id=1,
        )
        yield libc_to_manage_pb2.GetComputationResultResponse(
            message="ok",
            is_ok=True,
            result="'2']",
            piece_id=2,
        )

    def SendModelParam(self, request, context):
        res = libc_to_manage_pb2.GetComputationResultResponse(
            message="ok",
            is_ok=True,
        )
        return res

    def Predict(self, request, context):
        res = libc_to_manage_pb2.PredictResponse(
            message="ok",
            is_ok=True
        )
        return res

    def GetDataList(self, request, context):
        res = libc_to_manage_pb2.GetDataListResponse(
            is_ok=True,
            result="[]"
        )
        return res

    def GetJoinTable(self, request, context):
        res = libc_to_manage_pb2.GetJoinTableResponse(
            is_ok=True,
            result="['1']",
            schema=["s"]
        )
        return res


def serve(num: int):
    """ server setting """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    libc_to_manage_pb2_grpc.add_LibcToManageServicer_to_server(
        LibToManageServiceServicer(), server)
    server.add_insecure_port('localhost:900{}'.format(num))

    return server
