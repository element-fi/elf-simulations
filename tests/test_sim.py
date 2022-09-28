# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=attribute-defined-outside-init
# pylint: disable=wrong-import-position
# pylint: disable=too-many-instance-attributes 

import os
import sys

import unittest
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from sim import YieldSimulator, ElementPricingModel, YieldSpacev2PricingModel

class TestUtils(unittest.TestCase):
    def setup_test_vars(self):
        # fixed variables
        random_seed = 123
        simulator_rng = np.random.default_rng(random_seed)
        self.config = {
            'min_fee': 0.5,
            'max_fee': 0.5,
            'floor_fee': 0,
            't_min': 0.1,
            't_max': 0.1,
            'base_asset_price': 2500., # aka market price
            'min_target_liquidity': 100000.,
            'max_target_liquidity': 100000.,
            'min_target_volume': 2e5,
            'max_target_volume': 2e5,
            'min_pool_apy': 0.5,
            'max_pool_apy': 50,
            'min_vault_age': 0.,
            'max_vault_age': 2,
            'min_vault_apy': 0.,
            'max_vault_apy': 10.,
            'precision': None,
            'pricing_model_name': 'YieldSpacev2',
            'tokens': ['base', 'fyt'],
            'trade_direction': 'out',
            'pool_duration': 180,
            'num_trading_days': 180, # should be <= days_until_maturity
            'rng': simulator_rng,
        }
        self.pricing_models = [ElementPricingModel(), YieldSpacev2PricingModel()]
        # random variables
        self.test_rng = np.random.default_rng(random_seed)
        self.target_liquidity = self.test_rng.uniform(low=1e5, high=1e6)
        self.base_asset_price = self.test_rng.uniform(low=2e3, high=3e3)
        self.init_share_price = self.test_rng.uniform(low=1., high=2.)

    #def test_calc_apy(self):
    #    self.setup_test_vars()
    #    random_apy = self.test_rng.normal(loc=10, scale=0.1)
    #    days_remaining = 180
    #    for pricing_model in self.pricing_models:
    #        time_stretch = pricing_model.calc_time_stretch(random_apy)
    #        (base_asset_reserves, token_asset_reserves) = pricing_model.calc_liquidity(
    #            self.target_liquidity,
    #            self.base_asset_price,
    #            random_apy,
    #            days_remaining,
    #            time_stretch,
    #            self.init_share_price,
    #            self.init_share_price)[:2]
    #        total_supply = base_asset_reserves + token_asset_reserves
    #        time_remaining = pricing_model.days_to_time_remaining(days_remaining, time_stretch)
    #        calculated_apy = pricing_model.calc_apy_from_reserves(
    #            base_asset_reserves, token_asset_reserves, total_supply, time_remaining,
    #            time_stretch, self.init_share_price, self.init_share_price)
    #        np.testing.assert_allclose(random_apy, calculated_apy)

    #def test_calc_spot_price(self):
    #    self.setup_test_vars()
    #    pool_apy = self.test_rng.normal(loc=10, scale=0.1)
    #    days_remaining = 180
    #    for pricing_model in self.pricing_models:
    #        # Shared calculations
    #        time_stretch = pricing_model.calc_time_stretch(pool_apy)
    #        (base_asset_reserves, token_asset_reserves) = pricing_model.calc_liquidity(
    #            self.target_liquidity,
    #            self.base_asset_price,
    #            pool_apy,
    #            days_remaining,
    #            time_stretch,
    #            self.init_share_price,
    #            self.init_share_price)[:2]
    #        total_supply = base_asset_reserves + token_asset_reserves
    #        time_remaining = pricing_model.days_to_time_remaining(days_remaining, time_stretch)
    #        # Version 1
    #        spot_price_from_reserves = pricing_model.calc_spot_price(
    #            base_asset_reserves, token_asset_reserves,
    #            total_supply, time_remaining, self.init_share_price,
    #            self.init_share_price)
    #        # Version 2
    #        apy = pricing_model.apy(spot_price_from_reserves, days_remaining)
    #        spot_price_from_apy = pricing_model.calc_spot_price_from_apy(
    #            apy, days_remaining)
    #        # Test
    #        np.testing.assert_allclose(spot_price_from_reserves, spot_price_from_apy)

    def test_get_days_remaining(self):
        self.setup_test_vars()
        simulator = YieldSimulator(**self.config)
        simulator.set_random_variables()
        num_trading_days_list = [1, 5, 10]
        for num_trading_days in num_trading_days_list:
            override_dict = {'num_trading_days': num_trading_days}
            simulator.setup_pricing_and_market(override_dict)
            for day in range(num_trading_days):
                days_remaining = simulator.get_days_remaining()
                test_days_remaining = self.config['pool_duration'] - day
                np.testing.assert_allclose(days_remaining, test_days_remaining)
                simulator.market.tick(simulator.step_size)

    def test_pool_length_normalization(self):
        self.setup_test_vars()
        for pricing_model in self.pricing_models:
            for normalizing_constant in self.test_rng.uniform(low=0, high=365, size=10):
                for time_stretch in self.test_rng.normal(loc=10, scale=0.1, size=10):
                    for days_remaining in self.test_rng.integers(low=0, high=180, size=10):
                        time_remaining = pricing_model.days_to_time_remaining(
                            days_remaining, time_stretch, normalizing_constant)
                        new_days_remaining = pricing_model.time_to_days_remaining(
                            time_remaining, time_stretch, normalizing_constant)
                        np.testing.assert_allclose(days_remaining, new_days_remaining)

