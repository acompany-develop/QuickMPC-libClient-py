import ast
import json
import glob
from ..share import Share
from .if_present import if_present
from natsort import natsorted


def restore(job_uuid: str, path: str, party_size: int):
    results_str = []
    for party in range(party_size):
        res = ""
        for file in natsorted(glob.glob(f"{path}/{job_uuid}-{party}*")):
            with open(file, 'r') as f:
                res += f.read()

        results_str.append(json.loads(ast.literal_eval(res)))

    results = if_present(results_str, Share.recons)
    return results
