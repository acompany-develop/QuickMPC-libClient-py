import ast
import datetime
import hashlib
import json
import logging
import os
import struct
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, InitVar
from typing import Dict, Iterable, List, Tuple, Optional
from urllib.parse import urlparse

import grpc
import tqdm  # type: ignore
from grpc_status import rpc_status  # type: ignore

from .proto.common_types.common_types_pb2 import JobStatus, JobErrorInfo
from .proto.libc_to_manage_pb2 import (DeleteSharesRequest,
                                       ExecuteComputationRequest,
                                       GetComputationResultRequest,
                                       GetDataListRequest, Input, JoinOrder,
                                       PredictRequest, SendModelParamRequest,
                                       SendSharesRequest,
                                       GetElapsedTimeRequest,
                                       GetComputationResultResponse)
from .proto.libc_to_manage_pb2_grpc import LibcToManageStub
from .share import Share
from .exception import ArgmentError, QMPCJobError, QMPCServerError
from .utils.if_present import if_present
from .utils.make_pieces import MakePiece
from .utils.overload_tools import Dim2, Dim3, methoddispatch
from .utils.parse_csv import format_check

abs_file = os.path.abspath(__file__)
base_dir = os.path.dirname(abs_file)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class QMPCServer:
    endpoints: InitVar[List[str]]
    __client_stubs: Tuple[LibcToManageStub] = field(init=False)
    __party_size: int = field(init=False)
    token: str

    def __post_init__(self, endpoints: List[str]) -> None:
        stubs = [LibcToManageStub(QMPCServer.__create_grpc_channel(ep))
                 for ep in endpoints]
        object.__setattr__(self, "_QMPCServer__client_stubs", stubs)
        object.__setattr__(self, "_QMPCServer__party_size", len(endpoints))

    @staticmethod
    def __create_grpc_channel(endpoint: str) -> grpc.Channel:
        channel: grpc.Channel = None
        o = urlparse(endpoint)
        if o.scheme == 'http':
            # insecure???channel?????????
            channel = grpc.insecure_channel(o.netloc)
        elif o.scheme == 'https':
            # secure???channel?????????
            credential: grpc.ChannelCredentials \
                = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel(o.netloc, credential)
        else:
            logger.error(f'?????????????????????????????????endpoint???????????????: {endpoint}')
            raise ArgmentError(
                "endpoints???????????????????????????????????????????????????????????????????????????http/https?????????????????????????????????????????????")

        return channel

    @staticmethod
    def _argument_check(join_order: Tuple[List, List, List]):
        if len(join_order[0])-1 != len(join_order[1]):
            logger.error(
                'the size of join must be one less than the size of dataIds')
            return False
        if len(join_order[0]) != len(join_order[2]):
            logger.error('the size of index must match the size of dataIds')
            return False
        # TODO join???enum?????????
        if not all([0 <= join <= 2 for join in join_order[1]]):
            logger.error('join value must be in the range of 0 to 2')
            return False
        return True

    @staticmethod
    def __futures_result(
            futures: Iterable, enable_progress_bar=True) -> Tuple[bool, List]:
        """ ???????????????????????????future???result????????? """
        is_ok: bool = True
        response: List = []
        try:
            if enable_progress_bar:
                futures = tqdm.tqdm(futures, desc='receive')
            response = [f.result() for f in futures]
        except grpc.RpcError as e:
            is_ok = False
            logger.error(f'{e.details()} ({e.code()})')

            # ??????????????????????????????????????????????????????
            status = rpc_status.from_call(e)
            if status is not None:
                for detail in status.details:
                    if detail.Is(
                        JobErrorInfo.DESCRIPTOR   # type: ignore[attr-defined]
                    ):
                        # CC ??? Job ????????????????????????????????????????????????
                        # ????????? rethrow ??????
                        err_info = JobErrorInfo()
                        detail.Unpack(err_info)
                        logger.error(f"job error information: {err_info}")

                        raise QMPCJobError(err_info) from e

            # MC ??? Internal Server Error ???????????????????????????
            # ????????? rethrow ??????
            if e.code() == grpc.StatusCode.UNKNOWN:
                raise QMPCServerError("backend server return error") from e
        except Exception as e:
            is_ok = False
            logger.error(e)

        for b in response:
            if hasattr(b, "is_ok"):
                is_ok &= b.is_ok
            else:
                is_ok &= b["is_ok"]
        return is_ok, response

    @staticmethod
    def __stream_result(stream: Iterable, job_uuid: str, party: int,
                        path: Optional[str]) -> Dict:
        """ ???????????????????????????stream???result????????? """
        is_ok: bool = True
        res_list = []
        for res in stream:
            is_ok &= res.is_ok
            if path is not None:
                file_path = f"{path}/{job_uuid}-{party}-{res.piece_id}"
                with open(file_path, mode='w') as f:
                    f.write(res.result)
                res.result = GetComputationResultResponse().result
            res_list.append(res)
        res_dict: Dict = {"is_ok": is_ok, "responses": res_list}
        return res_dict

    @methoddispatch()
    def send_share(self, _):
        raise ArgmentError("?????????????????????????????????????????????")

    @send_share.register(Dim2)
    @send_share.register(Dim3)
    def __send_share_impl(self, secrets: List, schema: List[str],
                          matching_column: int,
                          piece_size: int) -> Dict:
        if piece_size < 1000 or piece_size > 1_000_000:
            raise RuntimeError(
                "piece_size must be in the range of 1000 to 1000000")

        if matching_column <= 0 or matching_column > len(schema):
            raise RuntimeError(
                "matching_column must be in the "
                "range of 1 to the size of schema")

        # TODO parse_csv?????????send_share?????????????????????????????????????????????????????????
        if not format_check(secrets, schema):
            raise RuntimeError("????????????????????????????????????????????????????????????")

        """ Share???????????????????????? """
        sorted_secrets = sorted(
            secrets, key=lambda row: row[matching_column - 1])
        # piece????????????????????????
        pieces: list = MakePiece.make_pieces(
            sorted_secrets, int(piece_size / 10))
        data_id: str = hashlib.sha256(
            str(sorted_secrets).encode() + struct.pack('d', time.time())
        ).hexdigest()
        shares = [Share.sharize(s, self.__party_size)
                  for s in tqdm.tqdm(pieces, desc='sharize')]
        sent_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # ??????????????????????????????????????????????????????????????????????????????
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.SendShares,
                                   SendSharesRequest(
                                       data_id=data_id,
                                       shares=json.dumps(s),
                                       schema=schema,
                                       piece_id=piece_id,
                                       sent_at=sent_at,
                                       matching_column=matching_column,
                                       token=self.token))
                   for piece_id, share_piece in enumerate(shares)
                   for stub, s in zip(self.__client_stubs, share_piece)
                   ]
        is_ok, _ = QMPCServer.__futures_result(futures)
        return {"is_ok": is_ok, "data_id": data_id}

    def delete_share(self, data_ids: List[str]) -> Dict:
        """ Share????????? """
        req = DeleteSharesRequest(dataIds=data_ids, token=self.token)
        # ?????????????????????????????????
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.DeleteShares, req)
                   for stub in self.__client_stubs]
        is_ok, _ = QMPCServer.__futures_result(futures)
        return {"is_ok": is_ok}

    def execute_computation(self, method_id: int,
                            join_order: Tuple[List, List, List],
                            inp: Tuple[List, List]) -> Dict:
        if not self._argument_check(join_order):
            raise ArgmentError("????????????????????????????????????")

        """ ?????????????????????????????? """
        join_order_req = JoinOrder(
            dataIds=join_order[0],
            join=join_order[1],
            index=join_order[2])
        input_req = Input(
            src=inp[0],
            target=inp[1])
        req = ExecuteComputationRequest(
            method_id=method_id,
            token=self.token,
            table=join_order_req,
            arg=input_req,
        )

        # ?????????????????????????????????
        executor = ThreadPoolExecutor()
        # Jobid???MC???????????????????????????MC????????????SP???ID=0?????????????????????????????????????????????
        futures = [executor.submit(
            self.__client_stubs[0].ExecuteComputation, req)]

        is_ok, response = QMPCServer.__futures_result(futures)
        job_uuid = response[0].job_uuid if is_ok else None

        return {"is_ok": is_ok, "job_uuid": job_uuid}

    def get_computation_result(self, job_uuid: str,
                               path: Optional[str]) -> Dict:
        """ ????????????????????????????????? """
        # ???????????????????????????????????????
        req = GetComputationResultRequest(
            job_uuid=job_uuid,
            token=self.token
        )
        # ?????????????????????????????????
        executor = ThreadPoolExecutor()
        futures = [executor.submit(QMPCServer.__stream_result,
                                   stub.GetComputationResult(req),
                                   job_uuid, party, path)
                   for party, stub in enumerate(self.__client_stubs)]
        is_ok, response = QMPCServer.__futures_result(
            futures, enable_progress_bar=False)

        results_sorted = [sorted(res["responses"], key=lambda r: r.piece_id)
                          for res in response]

        # NOTE: status???0??????(piece_id=1)????????????????????????????????????
        statuses = [res[0].status for res in results_sorted] \
            if results_sorted else None
        all_completed = all([
            s == JobStatus.Value('COMPLETED') for s in statuses
        ]) if statuses is not None else False

        progresses = None
        if results_sorted is not None:
            progresses = [
                res[0].progress if res[0].HasField("progress") else None
                for res in results_sorted
            ]

        # piece_id??????result?????????
        results_str = ["".join(map(lambda r: r.result, res))
                       for res in results_sorted]
        results = [json.loads(ast.literal_eval(r))
                   for r in results_str
                   ] if all_completed and path is None else None

        # recons????????????
        results = if_present(results, Share.recons)
        return {"is_ok": is_ok, "statuses": statuses,
                "results": results, "progresses": progresses}

    def send_model_params(self, params: list,
                          piece_size: int) -> Dict:
        if piece_size < 1000 or piece_size > 1_000_000:
            raise RuntimeError(
                "piece_size must be in the range of 1000 to 1000000")

        """ ???????????????????????????????????????????????? """
        # ???????????????????????????????????????
        job_uuid: str = str(uuid.uuid4())
        params_share: list = Share.sharize(params, self.__party_size)

        params_share_pieces: list = [MakePiece.make_pieces(
            json.dumps(p), piece_size) for p in params_share]

        # ?????????????????????????????????
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.SendModelParam,
                                   SendModelParamRequest(job_uuid=job_uuid,
                                                         params=param,
                                                         piece_id=piece_id + 1,
                                                         token=self.token))
                   for pieces, stub in zip(params_share_pieces,
                                           self.__client_stubs)
                   for piece_id, param in enumerate(pieces)]
        is_ok, _ = QMPCServer.__futures_result(futures)

        return {"is_ok": is_ok, "job_uuid": job_uuid}

    def predict(self,
                model_param_job_uuid: str,
                model_id: int,
                join_order: Tuple[List, List, List],
                src: List[int]) -> Dict:
        if not self._argument_check(join_order):
            raise ArgmentError("????????????????????????????????????")

        """ ????????????????????????????????? """
        # ???????????????????????????????????????
        job_uuid: str = str(uuid.uuid4())
        req = PredictRequest(job_uuid=job_uuid,
                             model_param_job_uuid=model_param_job_uuid,
                             model_id=model_id,
                             table=JoinOrder(dataIds=join_order[0],
                                             join=join_order[1],
                                             index=join_order[2]),
                             src=src,
                             token=self.token)

        # ?????????????????????????????????
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.Predict, req)
                   for stub in self.__client_stubs]
        is_ok, response = QMPCServer.__futures_result(futures)

        return {"is_ok": is_ok, "job_uuid": job_uuid}

    def get_data_list(self) -> Dict:
        # ?????????????????????????????????
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.GetDataList,
                                   GetDataListRequest(token=self.token))
                   for stub in self.__client_stubs]
        is_ok, response = QMPCServer.__futures_result(futures)
        results = [eval(r.result) for r in response] if is_ok else None

        return {"is_ok": is_ok, "results": results}

    def get_elapsed_time(self, job_uuid: str) -> Dict:
        # ???????????????????????????????????????
        req = GetElapsedTimeRequest(
            job_uuid=job_uuid,
            token=self.token
        )
        # ?????????????????????????????????
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.GetElapsedTime,
                                   req)
                   for stub in self.__client_stubs]
        is_ok, response = QMPCServer.__futures_result(futures)
        elapsed_time = max([res.elapsed_time
                            for res in response]) if is_ok else None
        return {"is_ok": is_ok, "elapsed_time": elapsed_time}
