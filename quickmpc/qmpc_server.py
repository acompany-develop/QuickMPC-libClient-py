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
from typing import Dict, Iterable, List, Tuple
from urllib.parse import urlparse

import grpc
import tqdm  # type: ignore

from .proto.common_types.common_types_pb2 import JobStatus
from .proto.libc_to_manage_pb2 import (DeleteSharesRequest,
                                       ExecuteComputationRequest,
                                       GetComputationResultRequest,
                                       GetDataListRequest, Input, JoinOrder,
                                       PredictRequest, SendModelParamRequest,
                                       SendSharesRequest,
                                       GetElapsedTimeRequest)
from .proto.libc_to_manage_pb2_grpc import LibcToManageStub
from .share import Share
from .utils.if_present import if_present
from .utils.make_pieces import MakePiece
from .utils.overload_tools import ArgmentError, Dim2, Dim3, methoddispatch

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
            # insecureなchannelを作成
            channel = grpc.insecure_channel(o.netloc)
        elif o.scheme == 'https':
            # secureなchannelを作成
            credential: grpc.ChannelCredentials \
                = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel(o.netloc, credential)
        else:
            logger.error(f'仕様を満たさない形式のendpointが渡された: {endpoint}')
            raise ArgmentError(
                "endpointsにサポートされてないプロトコルが指定されています．http/httpsのいずれかを指定してください．")

        return channel

    @staticmethod
    def __futures_result(
            futures: Iterable, enable_progress_bar=True) -> Tuple[bool, List]:
        """ エラーチェックしてfutureのresultを得る """
        is_ok: bool = True
        response: List = []
        try:
            if enable_progress_bar:
                futures = tqdm.tqdm(futures, desc='receive')
            response = [f.result() for f in futures]
        except grpc.RpcError as e:
            is_ok = False
            logger.error(f'{e.details()} ({e.code()})')
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
    def __stream_result(stream: Iterable) -> Dict:
        """ エラーチェックしてstreamのresultを得る """
        is_ok: bool = True
        res_list = []
        for res in stream:
            is_ok &= res.is_ok
            res_list.append(res)
        res_dict: Dict = {"is_ok": is_ok, "responses": res_list}
        return res_dict

    @methoddispatch()
    def send_share(self, _):
        raise ArgmentError("不正な引数が与えられています．")

    @send_share.register(Dim2)
    @send_share.register(Dim3)
    def __send_share_impl(self, secrets: List, schema: List[str],
                          matching_column: int,
                          piece_size: int) -> Dict:
        """ Shareをコンテナに送信 """
        sorted_secrets = sorted(
            secrets, key=lambda row: row[matching_column - 1])
        # pieceに分けてシェア化
        pieces: list = MakePiece.make_pieces(
            sorted_secrets, int(piece_size / 10))
        data_id: str = hashlib.sha256(
            str(sorted_secrets).encode() + struct.pack('d', time.time())
        ).hexdigest()
        shares = [Share.sharize(s, self.__party_size)
                  for s in tqdm.tqdm(pieces, desc='sharize')]
        sent_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # リクエストパラメータを設定して非同期にリクエスト送信
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.SendShares,
                                   SendSharesRequest(
                                       data_id=data_id,
                                       shares=json.dumps(s),
                                       schema=schema,
                                       piece_id=piece_id,
                                       sent_at=sent_at,
                                       token=self.token))
                   for piece_id, share_piece in enumerate(shares)
                   for stub, s in zip(self.__client_stubs, share_piece)
                   ]
        is_ok, _ = QMPCServer.__futures_result(futures)
        return {"is_ok": is_ok, "data_id": data_id}

    def delete_share(self, data_ids: List[str]) -> Dict:
        """ Shareを削除 """
        req = DeleteSharesRequest(dataIds=data_ids, token=self.token)
        # 非同期にリクエスト送信
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.DeleteShares, req)
                   for stub in self.__client_stubs]
        is_ok, _ = QMPCServer.__futures_result(futures)
        return {"is_ok": is_ok}

    def execute_computation(self, method_id: int,
                            join_order: Tuple[List, List, List],
                            inp: Tuple[List, List]) -> Dict:
        """ 計算リクエストを送信 """
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

        # 非同期にリクエスト送信
        executor = ThreadPoolExecutor()
        # JobidをMCから貰う関係で単一MC（現在はSP（ID=0）のみ対応）にリクエストを送る
        futures = [executor.submit(
            self.__client_stubs[0].ExecuteComputation, req)]

        is_ok, response = QMPCServer.__futures_result(futures)
        job_uuid = response[0].job_uuid if is_ok else None

        return {"is_ok": is_ok, "job_uuid": job_uuid}

    def get_computation_result(self, job_uuid: str) -> Dict:
        """ コンテナから結果を取得 """
        # リクエストパラメータを設定
        req = GetComputationResultRequest(
            job_uuid=job_uuid,
            token=self.token
        )
        # 非同期にリクエスト送信
        executor = ThreadPoolExecutor()
        futures = [executor.submit(QMPCServer.__stream_result,
                                   stub.GetComputationResult(req))
                   for stub in self.__client_stubs]
        is_ok, response = QMPCServer.__futures_result(
            futures, enable_progress_bar=False)

        results_sorted = [sorted(res["responses"], key=lambda r: r.piece_id)
                          for res in response]

        # NOTE: statusは0番目(piece_id=1)の要素にのみ含まれている
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

        # piece_id順にresultを結合
        results_str = ["".join(map(lambda r: r.result, res))
                       for res in results_sorted]
        results = [eval(eval(r))
                   for r in results_str] if all_completed else None

        # reconsして返す
        results = if_present(results, Share.recons)
        return {"is_ok": is_ok, "statuses": statuses,
                "results": results, "progresses": progresses}

    def send_model_params(self, params: list,
                          piece_size: int) -> Dict:
        """ モデルパラメータをコンテナに送信 """
        # リクエストパラメータを設定
        job_uuid: str = str(uuid.uuid4())
        params_share: list = Share.sharize(params, self.__party_size)

        params_share_pieces: list = [MakePiece.make_pieces(
            json.dumps(p), piece_size) for p in params_share]

        # 非同期にリクエスト送信
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
        """ モデルから予測値を取得 """
        # リクエストパラメータを設定
        job_uuid: str = str(uuid.uuid4())
        req = PredictRequest(job_uuid=job_uuid,
                             model_param_job_uuid=model_param_job_uuid,
                             model_id=model_id,
                             table=JoinOrder(dataIds=join_order[0],
                                             join=join_order[1],
                                             index=join_order[2]),
                             src=src,
                             token=self.token)

        # 非同期にリクエスト送信
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.Predict, req)
                   for stub in self.__client_stubs]
        is_ok, response = QMPCServer.__futures_result(futures)

        return {"is_ok": is_ok, "job_uuid": job_uuid}

    def get_data_list(self) -> Dict:
        # 非同期にリクエスト送信
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.GetDataList,
                                   GetDataListRequest(token=self.token))
                   for stub in self.__client_stubs]
        is_ok, response = QMPCServer.__futures_result(futures)
        results = [eval(r.result) for r in response] if is_ok else None

        return {"is_ok": is_ok, "results": results}

    def get_elapsed_time(self, job_uuid: str) -> Dict:
        # リクエストパラメータを設定
        req = GetElapsedTimeRequest(
            job_uuid=job_uuid,
            token=self.token
        )
        # 非同期にリクエスト送信
        executor = ThreadPoolExecutor()
        futures = [executor.submit(stub.GetElapsedTime,
                                   req)
                   for stub in self.__client_stubs]
        is_ok, response = QMPCServer.__futures_result(futures)
        elapsed_time = max([res.elapsed_time
                            for res in response]) if is_ok else None
        return {"is_ok": is_ok, "elapsed_time": elapsed_time}
