"""Helper script to generate a random private key."""
import argparse
import json

import numpy as np
from agent0.base.make_key import make_private_key
from agent0.hyperdrive.config import get_eth_bots_config


def main() -> str:
    """Primary execution pipeline"""
    parser = argparse.ArgumentParser(
        prog="populate_env",
        description="Script for generating a .env file for eth_bots.",
        epilog=(
            "Run the script with a user's private key as argument to include it in the output."
            "See the README on https://github.com/delvtech/elf-simulations/eth_bots/ for more implementation details"
        ),
    )
    parser.add_argument("user_key", nargs="?", help="The user's private key for funding bots.")
    args = parser.parse_args()
    environment_config, agent_config = get_eth_bots_config()
    rng = np.random.default_rng(environment_config.random_seed)
    agent_private_keys = []
    agent_base_budgets = []
    agent_eth_budgets = []
    for agent_info in agent_config:
        for _ in range(agent_info.number_of_agents):
            agent_private_keys.append(make_private_key())
            agent_base_budgets.append(agent_info.base_budget.sample_budget(rng).scaled_value)
            agent_eth_budgets.append(agent_info.eth_budget.sample_budget(rng).scaled_value)
    env_str = ""
    if args.user_key is not None:
        env_str += "export USER_KEY='" + str(parser.parse_args().user_key) + "'" + "\n"
    env_str += "export AGENT_KEYS='" + json.dumps(agent_private_keys) + "'" + "\n"
    env_str += "export AGENT_BASE_BUDGETS='" + json.dumps(agent_base_budgets) + "'" + "\n"
    env_str += "export AGENT_ETH_BUDGETS='" + json.dumps(agent_eth_budgets) + "'" + "\n"
    return env_str


if __name__ == "__main__":
    print_str = main()
    print(print_str)
