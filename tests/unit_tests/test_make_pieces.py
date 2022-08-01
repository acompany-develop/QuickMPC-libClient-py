from typing import List

import pytest
from quickmpc.utils.make_pieces import MakePiece
from quickmpc.utils.overload_tools import ArgmentError


class TestQMPC:

    MATRIX: List[List[str]] = [[str(i) * i for i in range(1, 6)]] * 5

    @pytest.mark.parametrize(
        ("matrix, size, expected"),
        [
            (MATRIX, 75, [MATRIX]),
            (MATRIX, 30, [MATRIX[:2], MATRIX[2:4], MATRIX[4:]]),
            (MATRIX[0], 15, [MATRIX[0]])
        ]
    )
    def test_make_pieces(self, matrix, size, expected):
        actual = MakePiece.make_pieces(matrix, size)
        assert(actual == expected)

    @pytest.mark.parametrize(
        ("args, error"),
        [
            ([MATRIX, 0], RuntimeError),    # サイズが小さい場合
            ([0, 0], ArgmentError),         # 引数タイプが無効な場合: 0 次元
            ([[MATRIX], 0], ArgmentError),  # 引数タイプが無効な場合: 3 次元
        ]
    )
    def test_make_pieces_errorhandring(self, args, error):
        """ 異常値を与えてエラーが出るかTest """
        with pytest.raises(error):
            MakePiece.make_pieces(*args)
