"""Example main.py file for illustrating a simulator workflow"""
# stdlib
import sys
import os
import argparse
import logging
from typing import Any
from logging.handlers import RotatingFileHandler

# external imports
import numpy as np

# elfpy core repo
import elfpy

# elfpy core classes
from elfpy.agent import Agent
from elfpy.simulators import Simulator
from elfpy.markets import Market
from elfpy.pricing_models import PricingModel

# elfpy utils
from elfpy.utils import sim_utils  # utilities for setting up a simulation
import elfpy.utils.parse_config as config_utils
from elfpy.utils.data import format_trades


class CustomShorter(Agent):
    """
    Agent that is trying to optimize on a rising vault APR via shorts
    """

    def __init__(self, wallet_address: int, budget: int = 10_000) -> None:
        """Add custom stuff then call basic policy init"""
        self.pt_to_short = 1_000
        super().__init__(wallet_address, budget)

    def action(self, market: Market, pricing_model: PricingModel) -> list[Any]:
        """Implement a custom user strategy"""
        block_position_list = list(self.wallet.token_in_protocol.values())
        has_opened_short = bool(any((x < -1 for x in block_position_list)))
        can_open_short = self.get_max_pt_short(market, pricing_model) >= self.pt_to_short
        vault_apy = market.share_price * 365 / market.init_share_price
        action_list = []
        if can_open_short:
            if vault_apy > market.get_rate(pricing_model):
                action_list.append(self.create_agent_action(action_type="open_short", trade_amount=self.pt_to_short))
            elif vault_apy < market.get_rate(pricing_model):
                if has_opened_short:
                    action_list.append(
                        self.create_agent_action(action_type="close_short", trade_amount=self.pt_to_short)
                    )
        return action_list


def setup_logging(filename: str, max_bytes: int, log_level: int) -> None:
    """Setup logging"""
    if filename is None:
        handler = logging.StreamHandler(sys.stdout)
    else:
        log_dir = os.path.dirname(filename)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        handler = RotatingFileHandler(filename, mode="a", maxBytes=max_bytes, backupCount=100)
    logging.getLogger().setLevel(log_level)  # events of this level and above will be tracked
    handler.setFormatter(logging.Formatter(elfpy.DEFAULT_LOG_FORMATTER, elfpy.DEFAULT_LOG_DATETIME))
    logging.getLogger().handlers = [
        handler,
    ]


def get_example_agents(
    num_new_agents: int,
    agents: dict[int, Agent] = None,
) -> dict[int, Agent]:
    """Instantiate a set of custom agents"""
    if agents is None:
        agents = {}
    num_existing_agents = len(agents)
    for wallet_address in range(
        num_existing_agents, num_new_agents + num_existing_agents
    ):  # save wallet_address=0 for init_lp_agent
        agent = CustomShorter(wallet_address)
        agent.log_status_report()
        agents.update({agent.wallet_address: agent})
    return agents


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ElfMain",
        description="Example execution script for running simulations using Elfpy",
        epilog="See the README on https://github.com/element-fi/elf-simulations/ for more implementation details",
    )
    parser.add_argument("--output", help="Optional output filename for logging", default=None, type=str)
    parser.add_argument(
        "--max_bytes",
        help="Maximum log file output size, in bytes. Default is 2e6 bytes (2MB). More than 100 files (200MB) will cause overwrites.",
        default=2e6,
        type=int,
    )
    parser.add_argument(
        "--log_level",
        help='Logging level, should be in ["DEBUG", "INFO", "WARNING"]. Default uses the config.',
        default=None,
        type=str,
    )
    parser.add_argument(
        "--config", help="Config file. Default uses the example config.", default="config/example_config.toml", type=str
    )
    parser.add_argument(
        "--num_agents", help="Integer specifying how many agents you want to simulate.", default=1, type=int
    )
    parser.add_argument(
        "--pricing_model", help="Pricing model to be used in the simulation", default="Hyperdrive", type=str
    )
    parser.add_argument("--trading_days", help="Number of simulated trading days", default=None, type=int)
    parser.add_argument("--blocks_per_day", help="Number of simulated trading blocks per day", default=None, type=int)
    return parser


if __name__ == "__main__":
    # define & parse script args
    args = get_argparser().parse_args()
    # override any particular simulation arguments
    override_dict = {}
    if args.trading_days is not None:
        override_dict["num_trading_days"] = args.trading_days
    if args.blocks_per_day is not None:
        override_dict["num_blocks_per_day"] = args.blocks_per_day
    # get config & logging level
    config = sim_utils.override_config_variables(config_utils.load_and_parse_config_file(args.config), override_dict)
    if args.log_level is not None:
        config.simulator.logging_level = config_utils.text_to_logging_level(args.log_level)
    # define root logging parameters
    setup_logging(filename=args.output, max_bytes=args.max_bytes, log_level=config.simulator.logging_level)
    # instantiate random number generator
    rng = np.random.default_rng(config.simulator.random_seed)
    # run random number generators to get random simulation arguments
    random_sim_vars = sim_utils.override_random_variables(sim_utils.get_random_variables(config, rng), override_dict)
    # instantiate the pricing model
    sim_pricing_model = sim_utils.get_pricing_model(model_name=args.pricing_model)
    # instantiate the market
    sim_market = sim_utils.get_market(
        sim_pricing_model,
        random_sim_vars.target_pool_apy,
        random_sim_vars.fee_percent,
        config.simulator.token_duration,
        random_sim_vars.init_share_price,
    )
    # instantiate the init_lp agent
    init_agents = {
        0: sim_utils.get_init_lp_agent(
            config,
            sim_market,
            sim_pricing_model,
            random_sim_vars.target_liquidity,
            random_sim_vars.target_pool_apy,
            random_sim_vars.fee_percent,
        )
    }
    # set up simulator with only the init_lp_agent
    simulator = Simulator(
        config=config,
        pricing_model=sim_pricing_model,
        market=sim_market,
        agents=init_agents,
        rng=rng,
        random_simulation_variables=random_sim_vars,
    )
    # initialize the market using the LP agent
    simulator.collect_and_execute_trades()
    # get trading agent list
    simulator.agents = get_example_agents(num_new_agents=args.num_agents, agents=init_agents)
    simulator.run_simulation()
