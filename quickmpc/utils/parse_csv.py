import csv
import logging
from hashlib import sha512
from typing import List, Tuple, Dict, Union

from ..proto.common_types.common_types_pb2 import ShareValueTypeEnum

import numpy as np

logger = logging.getLogger(__name__)

ProtobufEnumType = int

SUPPORT_TYPES: Dict[str, ProtobufEnumType] = {
    'float': ShareValueTypeEnum.Value('SHARE_VALUE_TYPE_FIXED_POINT'),
    'str':
        ShareValueTypeEnum.Value(
            'SHARE_VALUE_TYPE_UTF_8_INTEGER_REPRESENTATION'
    ),
}

ShareValueType = Union[float, int]

ColumnSchema = Tuple[str, ProtobufEnumType]


def format_check(secrets: List[List[ShareValueType]],
                 schema: List[ColumnSchema]) -> bool:
    # 存在チェック
    if not (schema and secrets):
        logger.error("Schema or secrets table are not exists.")
        return False
    # 重複チェック
    if len(schema) != len(set(schema)):
        logger.error("Duplicate schema name.")
        return False
    # サイズチェック
    if np.any([len(s) != len(schema) for s in secrets]):
        logger.error("schema size and table colummn size are different.")
        return False
    return True


def to_float(val: str) -> float:
    """ If val is a float, convert as is; if it is a string, hash it. """
    try:
        return float(val)
    except ValueError:
        # k,m are constants used in the comparison operation
        # Due to the limitation of comparison operation,
        # k bits are taken out and divided by 2^m.
        k: int = 48
        m: int = 20
        hs: str = sha512(val.encode()).hexdigest()
        val_int: int = int(hs[:(k >> 2)], 16)
        val_float: float = val_int / pow(2, m)
        return val_float


def to_int(val: str, encoding='utf-8') -> int:
    encoded = val.encode(encoding)
    return int.from_bytes(encoded, byteorder='big')


def find_type(col_schema: str) -> int:
    type_str, *_ = col_schema.split(':')

    if type_str in SUPPORT_TYPES:
        return SUPPORT_TYPES[type_str]

    return ShareValueTypeEnum.Value('SHARE_VALUE_TYPE_FIXED_POINT')


def find_types(schema: List[str]) -> List[ProtobufEnumType]:
    return [find_type(col) for col in schema]


def convert(element: str, type_info: ProtobufEnumType) -> ShareValueType:
    if type_info == ShareValueTypeEnum.Value('SHARE_VALUE_TYPE_FIXED_POINT'):
        return to_float(element)
    if type_info == ShareValueTypeEnum.Value(
            'SHARE_VALUE_TYPE_UTF_8_INTEGER_REPRESENTATION'):
        return to_int(element)
    return to_float(element)


def parse(data: List[List[str]]) \
        -> Tuple[List[List[ShareValueType]], List[ColumnSchema]]:
    schema: List[str] = data[0]
    types = find_types(schema)
    secrets: List[List[ShareValueType]] = [
        [convert(x, t) for x, t in zip(row, types)] for row in data[1:]]

    if not format_check(secrets, schema):
        raise RuntimeError("規定されたフォーマットでないデータです．")

    return secrets, list(zip(schema, types))


def parse_to_bitvector(data: List[List[str]], exclude: List[int] = []) \
        -> Tuple[List[List[ShareValueType]], List[ColumnSchema]]:
    secrets, schema = parse(data)

    secrets_bitbevtor: List[List[float]] = []
    schema_bitvector: List[ColumnSchema] = []
    for col, (sec, sch) in enumerate(zip(np.transpose(secrets), schema)):
        # 列が除外リストに含まれていたらそのままappend
        if col in exclude:
            secrets_bitbevtor.append(sec)
            schema_bitvector.append((sch[0] + "#0", sch[1]))
            continue

        # 座標圧縮
        position: dict = {}
        it: int = 0
        for key in sec:
            if key not in position:
                position[key] = it
                it += 1

        # bitvector化
        for key, val in position.items():
            bitvector: list = [1 if (key == k) else 0 for k in sec]
            sch_val: str = sch[0] + "#" + str(val)
            secrets_bitbevtor.append(bitvector)
            schema_bitvector.append(
                (sch_val,
                 ShareValueTypeEnum.Value('SHARE_VALUE_TYPE_FIXED_POINT')))

    return np.transpose(secrets_bitbevtor).tolist(), schema_bitvector


def parse_csv(
        filename: str) -> Tuple[List[List[ShareValueType]], List[ColumnSchema]]:
    with open(filename) as f:
        reader = csv.reader(f)
        text: List[List[str]] = [row for row in reader]
        return parse(text)


def parse_csv_to_bitvector(filename: str, exclude: List[int] = []) ->  \
        Tuple[List[List[ShareValueType]], List[ColumnSchema]]:
    with open(filename) as f:
        reader = csv.reader(f)
        text: List[List[str]] = [row for row in reader]
        return parse_to_bitvector(text, exclude)
