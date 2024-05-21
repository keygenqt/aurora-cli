from dataclasses import dataclass
from pathlib import Path

import click


@dataclass
class SignPackageModel:
    """Class device."""
    name: str
    key: Path
    cert: Path

    @staticmethod
    def get_model(name: str, key: Path, cert: Path):
        return SignPackageModel(name, key, cert)

    @staticmethod
    def get_model_select(select: bool, index: int):
        devices = SignPackageModel.get_lists_keys()
        print(devices)
        return None

    # @todo
    @staticmethod
    @click.pass_context
    def get_lists_keys(ctx: {}) -> []:
        return ctx.obj.conf_new.get_keys()
