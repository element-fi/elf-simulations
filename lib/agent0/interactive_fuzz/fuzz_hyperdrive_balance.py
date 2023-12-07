"""Fuzz test to verify that if all of the funds are removed from Hyperdrive, there is no base left in the contract."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict
from typing import NamedTuple, Sequence

import numpy as np
from fixedpointmath import FixedPoint
from hyperlogs import ExtendedJSONEncoder, setup_logging
from numpy.random._generator import Generator

from agent0.hyperdrive.interactive import InteractiveHyperdrive, LocalChain
from agent0.hyperdrive.interactive.event_types import OpenLong, OpenShort
from agent0.hyperdrive.interactive.interactive_hyperdrive_agent import InteractiveHyperdriveAgent
from agent0.hyperdrive.state.hyperdrive_actions import HyperdriveActionType

# Variables by themselves print out dataframes in a nice format in interactive mode
# pylint: disable=pointless-statement
# pylint: disable=invalid-name

# Set global defaults
FAILED = False


def main(argv: Sequence[str] | None = None):
    """Primary entrypoint.

    Arguments
    ---------
    argv: Sequence[str]
        The argv values returned from argparser.
    """
    # Setup the environment
    parsed_args, log_filename, chain, random_seed, rng, interactive_hyperdrive = setup_fuzz(argv)

    # Get initial vault shares
    pool_state = interactive_hyperdrive.hyperdrive_interface.get_hyperdrive_state()
    initial_vault_shares = pool_state.vault_shares

    # Generate a list of agents that execute random trades
    trade_list = generate_trade_list(parsed_args.num_trades, rng, interactive_hyperdrive)

    # Open some trades
    trade_events = open_trades(chain, rng, interactive_hyperdrive, trade_list)

    # Close the trades
    close_random_trades(trade_events, rng)

    # Check the reserve amounts; they should be unchanged now that all of the trades are closed
    if invariant_check_failed(initial_vault_shares, random_seed, interactive_hyperdrive):
        raise AssertionError(f"Testing failed; see logs in {log_filename}")


class Args(NamedTuple):
    """Command line arguments for the invariant checker."""

    num_trades: int


def namespace_to_args(namespace: argparse.Namespace) -> Args:
    """Converts argprase.Namespace to Args.

    Arguments
    ---------
    namespace: argparse.Namespace
        Object for storing arg attributes.

    Returns
    -------
    Args
        Formatted arguments
    """
    return Args(
        num_trades=namespace.num_trades,
    )


def parse_arguments(argv: Sequence[str] | None = None) -> Args:
    """Parses input arguments.

    Arguments
    ---------
    argv: Sequence[str]
        The argv values returned from argparser.

    Returns
    -------
    Args
        Formatted arguments
    """
    parser = argparse.ArgumentParser(description="Runs a loop to check Hyperdrive invariants at each block.")
    parser.add_argument(
        "--num_trades",
        type=int,
        default=5,
        help="The number of random trades to open.",
    )
    # Use system arguments if none were passed
    if argv is None:
        argv = sys.argv
    # If no arguments were passed, display the help message and exit
    if len(argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return namespace_to_args(parser.parse_args())


def setup_fuzz(
    argv: Sequence[str] | None,
) -> tuple[Args, str, LocalChain, int, Generator, InteractiveHyperdrive]:
    """Setup the fuzz experiment.

    Arguments
    ---------
    argv: Sequence[str]
        A sequnce containing the uri to the database server and the test epsilon.

    Returns
    -------
    tuple[Args, str, LocalChain, int, Generator, InteractiveHyperdrive, FixedPoint]
        A tuple containing:
            parsed_args: Args
                A dataclass containing the parsed command line arguments.
            log_filename: str
                Where the log files are stored.
            chain: LocalChain
                An instantiated LocalChain.
            random_seed: int
                The random seed used to construct the Generator.
            rng: `Generator <https://numpy.org/doc/stable/reference/random/generator.html>`_
                The numpy Generator provides access to a wide range of distributions, and stores the random state.
            interactive_hyperdrive: InteractiveHyperdrive
                An instantiated InteractiveHyperdrive object.
    """
    parsed_args = parse_arguments(argv)
    log_filename = ".logging/fuzz_hyperdrive_balance.log"
    setup_logging(
        log_filename=log_filename,
        delete_previous_logs=True,
        log_stdout=False,
    )

    # Setup local chain
    chain_config = LocalChain.Config()
    chain = LocalChain(config=chain_config)
    random_seed = np.random.randint(
        low=1, high=99999999
    )  # No seed, we want this to be random every time it is executed
    rng = np.random.default_rng(random_seed)

    # Parameters for pool initialization.
    initial_pool_config = InteractiveHyperdrive.Config(preview_before_trade=True)
    interactive_hyperdrive = InteractiveHyperdrive(chain, initial_pool_config)

    return parsed_args, log_filename, chain, random_seed, rng, interactive_hyperdrive


def generate_trade_list(
    num_trades: int, rng: Generator, interactive_hyperdrive: InteractiveHyperdrive
) -> list[tuple[InteractiveHyperdriveAgent, HyperdriveActionType, FixedPoint]]:
    """Generate a list of agents that execute random trades.

    Arguments
    ---------
    num_trades: int
        The number of trades to execute.
    rng: `Generator <https://numpy.org/doc/stable/reference/random/generator.html>`_
        The numpy Generator provides access to a wide range of distributions, and stores the random state.
    interactive_hyperdrive: InteractiveHyperdrive
        An instantiated InteractiveHyperdrive object.

    Returns
    -------
    list[tuple[InteractiveHyperdriveAgent, HyperdriveActionType, FixedPoint]]
        Each element in the returned list is a tuple containing
            - an agent
            - a trade for that agent
            - the trade amount in base
    """
    available_actions = np.array([HyperdriveActionType.OPEN_LONG, HyperdriveActionType.OPEN_SHORT])
    min_trade = interactive_hyperdrive.hyperdrive_interface.pool_config.minimum_transaction_amount
    trade_list: list[tuple[InteractiveHyperdriveAgent, HyperdriveActionType, FixedPoint]] = []
    for _ in range(num_trades):  # 1 agent per trade
        budget = FixedPoint(
            scaled_value=int(np.floor(rng.uniform(low=min_trade.scaled_value * 10, high=int(1e23))))
        )  # Give a little extra money to account for fees
        agent = interactive_hyperdrive.init_agent(base=budget, eth=FixedPoint(100))
        trade_type = rng.choice(available_actions, size=1)[0]
        trade_amount_base = FixedPoint(
            scaled_value=int(
                rng.uniform(
                    low=min_trade.scaled_value,
                    high=int(
                        budget.scaled_value / 2
                    ),  # Don't trade all of their money, to make sure they have enough for fees
                )
            )
        )
        trade_list.append((agent, trade_type, trade_amount_base))
    return trade_list


def open_trades(
    trade_list: list[tuple[InteractiveHyperdriveAgent, HyperdriveActionType, FixedPoint]],
    chain: LocalChain,
    rng: Generator,
    interactive_hyperdrive: InteractiveHyperdrive,
) -> list[tuple[InteractiveHyperdriveAgent, OpenLong | OpenShort]]:
    """Open some trades specified by the trade list.

    Arguments
    ---------
    trade_list: list[tuple[InteractiveHyperdriveAgent, HyperdriveActionType, FixedPoint]]
        Each element in the returned list is a tuple containing
            - an agent
            - a trade for that agent
            - the trade amount in base
    chain: LocalChain
        An instantiated LocalChain.
    rng: `Generator <https://numpy.org/doc/stable/reference/random/generator.html>`_
        The numpy Generator provides access to a wide range of distributions, and stores the random state.
    interactive_hyperdrive: InteractiveHyperdrive
        An instantiated InteractiveHyperdrive object.

    Returns
    -------
    list[tuple[InteractiveHyperdriveAgent, OpenLong | OpenShort]]
        A list with an entry per trade, containing a tuple with:
            - the agent executing the trade
            - either the OpenLong or OpenShort trade event
    """
    trade_events: list[tuple[InteractiveHyperdriveAgent, OpenLong | OpenShort]] = []
    for trade in trade_list:
        agent, trade_type, trade_amount = trade
        if trade_type == HyperdriveActionType.OPEN_LONG:
            trade_event = agent.open_long(base=trade_amount)
        elif trade_type == HyperdriveActionType.OPEN_SHORT:
            trade_event = agent.open_short(bonds=trade_amount)
        else:
            raise AssertionError(f"{trade_type=} is not supported.")
        trade_events.append((agent, trade_event))
    # Advance a random amount of time after all trades have completed
    chain.advance_time(
        rng.integers(low=0, high=interactive_hyperdrive.hyperdrive_interface.pool_config.position_duration - 1),
        create_checkpoints=True,
    )
    return trade_events


def close_random_trades(
    trade_events: list[tuple[InteractiveHyperdriveAgent, OpenLong | OpenShort]], rng: Generator
) -> None:
    """Close trades provided in a random order.

    Arguments
    ---------
    trade_events: list[tuple[InteractiveHyperdriveAgent, OpenLong | OpenShort]]
        A list with an entry per trade, containing a tuple with:
            - the agent executing the trade
            - either the OpenLong or OpenShort trade event
    rng: `Generator <https://numpy.org/doc/stable/reference/random/generator.html>`_
        The numpy Generator provides access to a wide range of distributions, and stores the random state.
    """
    for trade_index in rng.permuted(list(range(len(trade_events)))):
        agent, trade = trade_events[int(trade_index)]
        if isinstance(trade, OpenLong):
            agent.close_long(maturity_time=trade.maturity_time, bonds=trade.bond_amount)
        if isinstance(trade, OpenShort):
            agent.close_short(maturity_time=trade.maturity_time, bonds=trade.bond_amount)


def invariant_check_failed(
    initial_vault_shares: FixedPoint,
    random_seed: int,
    interactive_hyperdrive: InteractiveHyperdrive,
) -> bool:
    """Check the pool state invariants.

    Arguments
    ---------
    initial_vault_shares: FixedPoint
        The number of vault shares owned by the Hyperdrive pool when it was deployed.
    random_seed: int
        Random seed used to run the experiment.
    interactive_hyperdrive: InteractiveHyperdrive
        An instantiated InteractiveHyperdrive object.

    Returns
    -------
    bool
        If true, at least one of the checks failed.
    """
    failed = False
    pool_state = interactive_hyperdrive.hyperdrive_interface.get_hyperdrive_state()
    if pool_state.vault_shares != initial_vault_shares:
        logging.critical("vault_shares=%s != initial_vault_shares=%s", pool_state.vault_shares, initial_vault_shares)
        failed = True
    if pool_state.pool_info.share_reserves < pool_state.pool_config.minimum_share_reserves:
        logging.critical(
            "share_reserves=%s < minimum_share_reserves=%s",
            pool_state.pool_info.share_reserves,
            pool_state.pool_config.minimum_share_reserves,
        )
        failed = True

    if failed:
        logging.info(
            "random_seed = %s\npool_config = %s\n\npool_info = %s\n\nlatest_checkpoint = %s\n\nadditional_info = %s",
            random_seed,
            json.dumps(asdict(pool_state.pool_config), indent=2, cls=ExtendedJSONEncoder),
            json.dumps(asdict(pool_state.pool_info), indent=2, cls=ExtendedJSONEncoder),
            json.dumps(asdict(pool_state.checkpoint), indent=2, cls=ExtendedJSONEncoder),
            json.dumps(
                {
                    "hyperdrive_address": interactive_hyperdrive.hyperdrive_interface.hyperdrive_contract.address,
                    "base_token_address": interactive_hyperdrive.hyperdrive_interface.base_token_contract.address,
                    "spot_price": interactive_hyperdrive.hyperdrive_interface.calc_spot_price(pool_state),
                    "fixed_rate": interactive_hyperdrive.hyperdrive_interface.calc_fixed_rate(pool_state),
                    "variable_rate": pool_state.variable_rate,
                    "vault_shares": pool_state.vault_shares,
                },
                indent=2,
                cls=ExtendedJSONEncoder,
            ),
        )
    return failed


if __name__ == "__main__":
    main()
