from typing import Any, Dict

import pytest

from quickmpc.qmpc_server import QMPCServer


class TestQMPC:
    qmpc: QMPCServer = QMPCServer(
        ["http://localhost:9001",
         "http://localhost:9002",
         "http://localhost:9003"],
        "token_demo"
    )

    @pytest.mark.parametrize(
        ("secrets"), [([[1, 2, 3]]), ([[1], [2], [3]]), ]
    )
    def test_send_shares(self, secrets, run_server1, run_server2, run_server3):
        """ serverにシェアを送れるかのTest"""
        response: Dict[str, Any] = self.qmpc.send_share(
            secrets, [], 1, 1000)
        assert (response["is_ok"])

    def test_delete_shares(self, run_server1, run_server2, run_server3):
        """ serverにシェア削除要求を送れるかのTest"""
        response: Dict[str, Any] = self.qmpc.delete_share([])
        assert (response["is_ok"])

    def test_execute_computation(self, run_server1, run_server2, run_server3):
        """ serverに計算リクエストを送れるかのTest"""
        for method_id in range(1, 3):
            response: Dict[str, Any] = self.qmpc.execute_computation(
                method_id,
                [["id1", "id2"], [0], [1, 1]], [[0, 1], []])
            assert (response["is_ok"])

    def test_get_computation_resultRequest(self, run_server1,
                                           run_server2, run_server3):
        """ serverから結果を得られるかのTest """
        job_uuid: str = "uuid"
        response: Dict[str, Any] = self.qmpc.get_computation_result(job_uuid)
        assert (response["is_ok"])

    def test_send_model_params(self, run_server1, run_server2, run_server3):
        """ serverにモデルパラメータを送れるかのTest"""
        res: Dict[str, Any] = self.qmpc.send_model_params(
            [[1, 2, 3]], 1000)
        assert (res["is_ok"])

    def test_predict(self, run_server1, run_server2, run_server3):
        """ serverにモデル値予測リクエストを送れるかのTest """
        model_param_job_uuid: str = "uuid"
        model_id: int = 1
        response: Dict[str, Any] = self.qmpc.predict(
            model_param_job_uuid, model_id,
            [["id1", "id2"], [0], [1, 1]], [0, 1])
        assert (response["is_ok"])

    def test_get_data_list(self, run_server1, run_server2, run_server3):
        """ serverにシェアを送れるかのTest"""
        response: Dict[str, Any] = self.qmpc.get_data_list()
        assert (response["is_ok"])
