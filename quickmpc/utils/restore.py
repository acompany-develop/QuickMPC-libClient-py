import ast
import json
import glob
from ..share import Share
from .if_present import if_present
from natsort import natsorted
from typing import Any
from decimal import Decimal


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
