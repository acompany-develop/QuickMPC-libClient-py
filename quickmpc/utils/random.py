from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, List

from nacl.utils import random, randombytes_deterministic

from .overload_tools import ArgmentError, methoddispatch


# 乱数生成のインタフェース
class RandomInterface(ABC):
    @abstractmethod
    def get(self, a, b) -> int:
        ...

    @abstractmethod
    def get_list(self, a, b, size: int) -> List[int]:
        ...


@dataclass(frozen=True)
class ChaCha20(RandomInterface):

    # 64bit符号付き整数最大，最小値
    mx: ClassVar[int] = (1 << 63)-1
    mn: ClassVar[int] = -(1 << 63)

    @methoddispatch()
    def get(self, a, b):
        raise ArgmentError(
            "乱数の閾値はどちらもintもしくはfloatでなければなりません．"
            f"a is {type(a)}, b is {type(b)}")

    @get.register(int)
    def __get_int(self, a: int, b: int) -> int:
        # TRNGで32byte(256bit)生成->先頭の64bitを取り出す
        self.__exception_check(a, b)
        byte_val: bytes = self.__get_32byte()
        int8byte: int = memoryview(byte_val).cast('Q')[0]
        return int8byte % (b-a)+a

    @get.register(float)
    def __get_float(self, a: float, b: float) -> float:
        # 64bit整数を取り出して[a,b]に正規化する
        self.__exception_check(a, b)
        val: int = self.get(self.mn, self.mx)
        return (val-self.mn)/(self.mx-self.mn)*(b-a)+a

    @methoddispatch()
    def get_list(self, a, b, size: int):
        raise ArgmentError(
            "乱数の閾値はどちらもintもしくはfloatでなければなりません．"
            f"a is {type(a)}, b is {type(b)}")

    @get_list.register(int)
    def __get_list_int(self, a: int, b: int, size: int) -> List[int]:
        # TRNGの32byteをseedとしてCSPRNGでsize分生成
        self.__exception_check(a, b)
        seed: bytes = self.__get_32byte()
        bytes_list: bytes = randombytes_deterministic(size*8, seed)
        mv = memoryview(bytes_list).cast('Q')
        return [x % (b-a)+a for x in mv]

    @get_list.register(float)
    def __get_list_float(self, a: float, b: float, size: int) -> List[float]:
        # 64bit整数を取り出して[a,b]に正規化する
        self.__exception_check(a, b)
        valList: List[int] = self.get_list(self.mn, self.mx, size)
        return [(val-self.mn)/(self.mx-self.mn)*(b-a)+a for val in valList]

    def __get_32byte(self) -> bytes:
        return random()

    def __exception_check(self, a, b) -> None:
        if a >= b:
            raise ArgmentError(
                "乱数の下限は上限より小さい必要があります．"
                f"{a} < {b}")
        if type(a) != type(b):
            raise ArgmentError(
                "乱数の下限と上限の型は一致させる必要があります．"
                f"{type(a)} != {type(b)}")
