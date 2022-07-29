from dataclasses import dataclass, field, InitVar
from typing import Dict, List, Tuple

from google.protobuf.internal import enum_type_wrapper

from .proto.common_types import common_types_pb2
from .qmpc_server import QMPCServer
from .share import Share
from .utils.parse_csv import (parse, parse_csv, parse_csv_to_bitvector,
                              parse_to_bitvector)

# qmpc.JobStatus でアクセスできるようにエイリアスを設定する
JobStatus: enum_type_wrapper.EnumTypeWrapper \
    = common_types_pb2.JobStatus
ComputationMethod: enum_type_wrapper.EnumTypeWrapper \
    = common_types_pb2.ComputationMethod
PredictMethod: enum_type_wrapper.EnumTypeWrapper \
    = common_types_pb2.PredictMethod


@dataclass(frozen=True)
class QMPC:
    endpoints: InitVar[List[str]]
    # tokenがちゃんと使用されるようになったらデフォルト値を外す
    token: InitVar[str] = "token_demo"

    __qmpc_server: QMPCServer = field(init=False)
    __party_size: int = field(init=False)

    def __post_init__(self, endpoints: List[str],
                      token: str):
        object.__setattr__(self, "_QMPC__qmpc_server", QMPCServer(
            endpoints, token))
        object.__setattr__(self, "_QMPC__party_size", len(endpoints))

    def parse_csv_file(self, filename: str) \
            -> Tuple[List[List[float]], List[str]]:
        return parse_csv(filename)

    def parse_csv_file_to_bitvector(self, filename: str,
                                    exclude: List[int] = []) \
            -> Tuple[List[List[float]], List[str]]:
        return parse_csv_to_bitvector(filename, exclude)

    def parse_csv_data(self, data: List[List[str]]) \
            -> Tuple[List[List[float]], List[str]]:
        return parse(data)

    def parse_csv_data_to_bitvector(self, data: List[List[str]],
                                    exclude: List[int] = []) \
            -> Tuple[List[List[float]], List[str]]:
        return parse_to_bitvector(data, exclude)

    def send_share(self, secrets: List, schema: List[str],
                   matching_column: int = 1,
                   piece_size: int = 1_000_000) -> Dict:
        return self.__qmpc_server.send_share(
            secrets, schema, matching_column, piece_size)

    def delete_share(self, data_ids: List[str]) -> Dict:
        return self.__qmpc_server.delete_share(data_ids)

    def mean(self, join_order: Tuple[List, List, List],
             src: List) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_MEAN"),
            join_order, (src, []))

    def variance(self, join_order: Tuple[List, List, List],
                 src: List) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_VARIANCE"),
            join_order, (src, []))

    def sum(self, join_order: Tuple[List, List, List], src: List) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_SUM"),
            join_order, (src, []))

    def correl(self, join_order: Tuple[List, List, List],
               inp: Tuple[List, List]) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_CORREL"),
            join_order, inp)

    def linear_regression(self, join_order: Tuple[List, List, List],
                          inp: Tuple[List, List]) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_LINEAR_REGRESSION"),
            join_order, inp)

    def logistic_regression(self, join_order: Tuple[List, List, List],
                            inp: Tuple[List, List]) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_LOGISTIC_REGRESSION"),
            join_order, inp)

    def meshcode(self, join_order: Tuple[List, List, List],
                 src: List) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_MESH_CODE"),
            join_order, (src, []))

    def decision_tree(self, join_order: Tuple[List, List, List],
                      inp: Tuple[List, List]) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_DECISION_TREE"),
            join_order, inp)

    def get_join_table(self, join_order: Tuple[List, List, List]) -> Dict:
        return self.__qmpc_server.execute_computation(
            ComputationMethod.Value("COMPUTATION_METHOD_JOIN_TABLE"),
            join_order, (join_order[2], []))

    def get_computation_result(self, job_id: str) -> Dict:
        return self.__qmpc_server.get_computation_result(job_id)

    def send_model_params(self, params: list) -> Dict:
        return self.__qmpc_server.send_model_params(params)

    def linear_regression_predict(self,
                                  model_param_job_uuid: str,
                                  join_order: Tuple[List, List, List],
                                  src: List[int]) -> Dict:
        return self.__qmpc_server.predict(
            model_param_job_uuid,
            PredictMethod.Value("PREDICT_METHOD_LINEAR_REGRESSION"),
            join_order, src)

    def logistic_regression_predict(self,
                                    model_param_job_uuid: str,
                                    join_order: Tuple[List, List, List],
                                    src: List[int]) -> Dict:
        return self.__qmpc_server.predict(
            model_param_job_uuid,
            PredictMethod.Value("PREDICT_METHOD_LOGISTIC_REGRESSION"),
            join_order, src)

    def decision_tree_predict(self,
                              model_param_job_uuid: str,
                              join_order: Tuple[List, List, List],
                              src: List[int]) -> Dict:
        return self.__qmpc_server.predict(
            model_param_job_uuid,
            PredictMethod.Value("PREDICT_METHOD_DECISION_TREE"),
            join_order, src)

    def sid3_tree_predict(self,
                          model_param_job_id: str,
                          join_order: Tuple[List, List, List],
                          src: List[int]) -> Dict:
        return self.__qmpc_server.predict(
            model_param_job_id,
            PredictMethod.Value("PREDICT_METHOD_SID3_TREE"),
            join_order, src)

    def get_data_list(self) \
            -> Dict:
        return self.__qmpc_server.get_data_list()

    def demo_sharize(self, secrets: List) -> Dict:
        share = Share.sharize(secrets, self.__party_size)
        return {'is_ok': True, 'results': share}
