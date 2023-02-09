"""Testing for the ElfPy package modules"""
from __future__ import annotations  # types are strings by default in 3.11

import unittest
import logging

import utils_for_tests as test_utils  # utilities for testing

import elfpy.utils.outputs as output_utils  # utilities for file outputs


class BaseParameterTest(unittest.TestCase):
    """Generic Parameter Test class"""

    def run_base_trade_test(
        self,
        agent_policies,
        config_file="config/example_config.toml",
        delete_logs=True,
    ):
        """Assigns member variables that are useful for many tests"""
        output_utils.setup_logging(log_filename=".logging/test_parameters.log", log_level=logging.DEBUG)
        override_dict = {
            "num_trading_days": 3,  # sim 3 days to keep it fast for testing
            "num_blocks_per_day": 3,  # 3 block a day, keep it fast for testing
            "num_position_days": 90,
        }
        simulator = test_utils.setup_simulation_entities(
            config_file=config_file, override_dict=override_dict, agent_policies=agent_policies
        )
        simulator.run_simulation()
        output_utils.close_logging(delete_logs=delete_logs)
        return simulator


class GetMaxShortTests(BaseParameterTest):
    """Tests of custom parameters"""

    def test_max_short(self):
        """set up a short that will attempt to trade more than possible"""
        agent_policies = ["single_lp:amount_to_lp=200", "single_short:amount_to_trade=500"]
        self.run_base_trade_test(agent_policies=agent_policies, delete_logs=True)
