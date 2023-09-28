import os
import json
from dataclasses import dataclass


@dataclass
class HyperParams:
    r"""
    Simple wrapper to store hyperparameters for Python-based rewriting methods.
    """

    @classmethod
    def from_json(cls, fpath: os.PathLike):
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(**data)
