import functools
import operator
from dataclasses import dataclass
from typing import List

from.overload_tools import ArgmentError, Dim1, Dim2, methoddispatch


@dataclass(frozen=True)
class MakePiece:

    @methoddispatch(is_static_method=True)
    @staticmethod
    def __get_byte(p): ...

    @__get_byte.register(float)
    @__get_byte.register(int)
    @staticmethod
    def __get_byte_number(f):
        # 扱う数値は64bitなので8byte
        return 8

    @__get_byte.register(str)
    @staticmethod
    def __get_byte_str(s: str):
        return len(s)

    @methoddispatch(is_static_method=True)
    @staticmethod
    def make_pieces(_, __):
        raise ArgmentError("不正な引数が与えられています．")

    @make_pieces.register(Dim1)
    @staticmethod
    def __make_pieces_1d(src: List[str], _) -> List[List[str]]:
        return [src]

    @make_pieces.register(Dim2)
    @staticmethod
    def __make_pieces_2d(src: List[List[str]],
                         max_size: int
                         ) -> List[List[List[str]]]:
        cur_size = 0
        index = 0
        dst: List[List[List[str]]] = [[]]
        for row in src:
            row_size = functools.reduce(
                operator.add, map(MakePiece.__get_byte, row), 0)
            if row_size > max_size:
                raise RuntimeError(
                    f"line size ({row_size}) is over "
                    f"specified limit size ({max_size})"
                )
            cur_size += row_size

            if cur_size > max_size:
                cur_size = row_size
                index += 1
                dst.append([])

            dst[index].append(row)

        return dst

    @make_pieces.register(str)
    @staticmethod
    def __make_pieces_str(src: str, max_size: int) -> List[str]:
        dst: List[str] = []
        current: str = ""
        for ch in src:
            current += ch

            if len(current) == max_size:
                dst.append(current)
                current = ""
        if current:
            dst.append(current)
        return dst
