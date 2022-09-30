import pytest

from quickmpc.utils.random import ChaCha20, RandomInterface


class TestCsprng:
    rnd: RandomInterface = ChaCha20()

    @pytest.mark.parametrize(
        ("lower", "upper"),
        [
            (0, 10),  # 正のみ
            (-5, 5),  # 正負
            (-10, 0),  # 負のみ
            (0, 1),   # 範囲が1
            (-(1 << 63), -(1 << 63) + 1),  # 64bit最小値
            ((1 << 63) - 1, (1 << 63) + 1)  # 64bit最大値
        ]
    )
    def test_csprng_int_interval(self, lower: int, upper: int):
        """ 半開区間内で生成されるかのtest """
        exist_lower: bool = False
        exist_upper_1: bool = False
        for _ in range(1000):
            x: int = self.rnd.get(lower, upper)
            assert (lower <= x and x < upper)
            assert (isinstance(x, int))
            exist_lower |= (x == lower)
            exist_upper_1 |= (x == upper - 1)
        for x in self.rnd.get_list(lower, upper, 1000):
            assert (lower <= x and x < upper)
            assert (isinstance(x, int))
            exist_lower |= (x == lower)
            exist_upper_1 |= (x == upper - 1)
        assert (exist_lower)
        assert (exist_upper_1)

    @pytest.mark.parametrize(
        ("lower", "upper"),
        [
            (0.0, 10.0),  # 正のみ
            (-5.0, 5.0),  # 正負
            (-10.0, 0.0),  # 負のみ
            (0.0, 1.0),   # 範囲が1
        ]
    )
    def test_csprng_float_interval(self, lower: float, upper: float):
        """ 半開区間内で生成されるかのtest """
        for _ in range(1000):
            x: int = self.rnd.get(lower, upper)
            assert (lower <= x and x < upper)
            assert (isinstance(x, float))
        for x in self.rnd.get_list(lower, upper, 1000):
            assert (lower <= x and x < upper)
            assert (isinstance(x, float))

    @pytest.mark.parametrize(
        ("lower", "upper"),
        [
            (0, 0),
            (10, 0),
            (0, 1.2),
            (0.0, 1),
            ("hoge", "huga"),
        ]
    )
    def test_csprng_errorhandring(self, lower, upper):
        """ 異常値を与えてエラーが出るかtest """
        with pytest.raises(Exception):
            self.rnd.get(lower, upper)
