import logging
from dataclasses import dataclass
from typing import ClassVar, List, Tuple

import numpy as np

from .utils.overload_tools import (ArgmentError, DictList, DictList2,
                                   Dim1, Dim2, Dim3, methoddispatch)
from .utils.random import ChaCha20, RandomInterface

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Share:
    __share_random_range: ClassVar[Tuple[float, float]] = (-20000.0, 20000.0)

    @methoddispatch(is_static_method=True)
    @staticmethod
    def sharize(_, __):
        logger.critical("Invalid argument on sharize.")
        raise ArgmentError("不正な引数が与えられています．")

    @methoddispatch(is_static_method=True)
    @staticmethod
    def recons(_):
        logger.critical("Invalid argument on recons.")
        raise ArgmentError("不正な引数が与えられています．")

    @sharize.register(int)
    @sharize.register(float)
    @staticmethod
    def __sharize_scalar(secrets: float, party_size: int = 3) -> List[str]:
        """ スカラ値のシェア化 """
        rnd: RandomInterface = ChaCha20()
        shares: List[int] = rnd.get_list(
            *Share.__share_random_range, party_size)
        shares[0] += secrets - np.sum(shares)
        shares_str: List[str] = [str(n) for n in shares]
        return shares_str

    @sharize.register(Dim1)
    @staticmethod
    def __sharize_1dimension(secrets: List[float], party_size: int = 3) \
            -> List[List[str]]:
        """ 1次元リストのシェア化 """
        rnd: RandomInterface = ChaCha20()
        secrets_size: int = len(secrets)
        shares: np.ndarray = np.array([
            rnd.get_list(*Share.__share_random_range, secrets_size)
            for __ in range(party_size - 1)])
        s1: np.ndarray = np.subtract(np.array(secrets), np.sum(shares, axis=0))
        shares_str: List[List[str]] = np.vectorize(str)([s1, *shares]).tolist()
        return shares_str

    @sharize.register(Dim2)
    @staticmethod
    def __sharize_2dimension(secrets: List[List[float]],
                             party_size: int = 3) -> List[List[List[str]]]:
        """ 2次元リストのシェア化 """
        rnd: RandomInterface = ChaCha20()
        secrets_size: int = len(secrets)
        secrets_size2: int = len(secrets[0])
        shares: np.ndarray = np.array([
            [rnd.get_list(*Share.__share_random_range, secrets_size2)
             for __ in range(secrets_size)]
            for ___ in range(party_size - 1)
        ])
        s1: np.ndarray = np.subtract(np.array(secrets, dtype=float),
                                     np.sum(shares, axis=0))
        shares_str: List[List[List[str]]] = \
            np.vectorize(str)([s1, *shares]).tolist()
        return shares_str

    @sharize.register(dict)
    @staticmethod
    def __sharize_dict(secrets: dict, party_size: int = 3) -> List[dict]:
        """ 辞書型のシェア化 """
        shares_str: List[dict] = [dict() for _ in range(party_size)]
        for key, val in secrets.items():
            for i, share_val in enumerate(Share.sharize(val, party_size)):
                shares_str[i][key] = share_val
        return shares_str

    @sharize.register(DictList)
    @staticmethod
    def __sharize_dictlist(secrets: dict, party_size: int = 3) \
            -> List[List[dict]]:
        """ 辞書型配列のシェア化 """
        shares_str: List[List[dict]] = [[] for _ in range(party_size)]
        for secret_dict in secrets:
            share_dict: List[dict] = Share.sharize(secret_dict, party_size)
            for ss, sd in zip(shares_str, share_dict):
                ss.append(sd)
        return shares_str

    @recons.register(Dim1)
    @staticmethod
    def __recons_list1(shares: List):
        """ 1次元リストのシェアを復元 """
        try:
            return sum([float(x) for x in shares])
        except ValueError:
            return shares[0]

    @recons.register(Dim2)
    @recons.register(Dim3)
    @staticmethod
    def __recons_list(shares: List[List]) -> List:
        """ リストのシェアを復元 """
        secrets: List = [
            Share.recons([shares_pi[i] for shares_pi in shares])
            for i in range(len(shares[0]))
        ]
        return secrets

    @recons.register(DictList)
    @staticmethod
    def __recons_dictlist(shares: List[dict]) -> dict:
        """ 辞書型を復元 """
        secrets: dict = dict()
        for key in shares[0].keys():
            val = []
            for s in shares:
                val.append(s[key])
            secrets[key] = Share.recons(val)
        return secrets

    @recons.register(DictList2)
    @staticmethod
    def __recons_dictlist2(shares: List[List[dict]]) -> list:
        """ 辞書型配列を復元 """
        secrets: list = list()
        for i in range(len(shares[0])):
            val = []
            for s in shares:
                val.append(s[i])
            secrets.append(Share.recons(val))
        return secrets
