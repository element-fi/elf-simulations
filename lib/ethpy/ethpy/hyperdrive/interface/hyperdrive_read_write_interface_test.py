"""Tests for hyperdrive/api.py."""
from __future__ import annotations

import os
from copy import deepcopy
from dataclasses import fields
from typing import cast

from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_utils.conversions import to_bytes
from eth_utils.crypto import keccak
from eth_utils.curried import text_if_str
from ethpy.base import set_anvil_account_balance
from fixedpointmath import FixedPoint
from hypertypes.fixedpoint_types import FeesFP
from hypertypes.types import Checkpoint, PoolConfig
from hypertypes.utilities.conversions import (
    checkpoint_to_fixedpoint,
    pool_config_to_fixedpoint,
    pool_info_to_fixedpoint,
)
from web3 import Web3

from .hyperdrive_read_write_interface import HyperdriveReadWriteInterface

# we need to use the outer name for fixtures
# pylint: disable=redefined-outer-name


class TestHyperdriveReadWriteInterface:
    """Tests for the HyperdriveReadWriteInterface api class."""

    def test_set_variable_rate(self, web3: Web3, hyperdrive_read_write_interface: HyperdriveReadWriteInterface):
        variable_rate = hyperdrive_read_write_interface.get_variable_rate()
        new_rate = variable_rate * 0.1
        # TODO: Setup a fixture to create a funded local account
        extra_key_bytes = text_if_str(to_bytes, "extra_entropy")
        key_bytes = keccak(os.urandom(32) + extra_key_bytes)
        private_key = Account()._parsePrivateKey(key_bytes)  # pylint: disable=protected-access
        sender: LocalAccount = Account().from_key(private_key)
        set_anvil_account_balance(web3, sender.address, 10**19)
        hyperdrive_read_write_interface.set_variable_rate(sender, new_rate)
        assert hyperdrive_read_write_interface.get_variable_rate() == new_rate
