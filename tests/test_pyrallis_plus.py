#!/usr/bin/env python3

from dataclasses import dataclass, field

import pyrallis_plus


@dataclass
class TrainConfig:
    """Training config for Machine Learning"""

    # The number of workers for training
    workers: int = field(default=8, metadata={"alias": ["-#"]})
    # The experiment name
    exp_name: str = pyrallis_plus.field(default="default_exp", alias=["--name"])


def test_help():
    try:
        pyrallis_plus.parse(config_class=TrainConfig, args=["-h"])
    except SystemExit as e:
        assert e.code == 0


def test_alias():
    cfg = pyrallis_plus.parse(config_class=TrainConfig, args=["-#", "16"])
    assert cfg.workers == 16


def test_field():
    exp_name = "abc"
    cfg = pyrallis_plus.parse(config_class=TrainConfig, args=["--name", exp_name])
    assert cfg.exp_name == exp_name
