import ast
import json
import glob
import csv
from ..share import Share
from .if_present import if_present
from natsort import natsorted
from typing import Any
from decimal import Decimal
import numpy as np


def get_res(job_uuid, path, party):
    schema = []
    result = [[]]
    for file_name in natsorted(glob.glob(f"{path}/schema-{job_uuid}-{party}-*")):
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                for val in row:
                    schema.append(val)

    tmp = 0
    for file_name in natsorted(glob.glob(f"{path}/result-{job_uuid}-{party}-*")):
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            row = next(reader)
            row_number = int(row[0])
            for row in reader:
                for val in row:
                    if tmp >= row_number:
                        result.append([])
                        tmp = 0
                    result[-1].append(Decimal(val))
                    tmp += 1

    return schema, result


def restore_test(job_uuid: str, path: str, party_size: int):
    schema, result = get_res(job_uuid, path, 0)
    row_number = 0
    is_dim2 = 0
    for party in range(1, party_size):
        tmp = 0
        row_num = 0
        for file_name in natsorted(glob.glob(f"{path}/result-{job_uuid}-{party}-*")):
            with open(file_name, 'r') as f:
                reader = csv.reader(f)
                row = next(reader)
                row_number = int(row[0])
                is_dim2 = int(row[1])
                for row in reader:
                    for val in row:
                        if tmp >= row_number:
                            tmp = 0
                            row_num += 1
                        result[row_num][tmp] += Decimal(val)
                        tmp += 1
    result = np.vectorize(float)(result).tolist()
    result = result if is_dim2 else result[0]
    res = result if len(schema) == 0 else \
        {"schema": schema, "table": result}
    return res


def restore(job_uuid: str, path: str, party_size: int):
    results: Any
    for party in range(party_size):
        res = ""
        for file in natsorted(glob.glob(f"{path}/{job_uuid}-{party}*")):
            with open(file, 'r') as f:
                res += f.read()

        if party == 0:
            results = json.loads(ast.literal_eval(res))
        elif party == party_size-1:
            results = if_present([results, json.loads(
                ast.literal_eval(res))], Share.recons)
        else:
            results = if_present([results, json.loads(
                ast.literal_eval(res))], Share.recons, Decimal)
    return results
