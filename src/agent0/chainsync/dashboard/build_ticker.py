"""Builds the ticker for the dashboard."""

import pandas as pd

from .usernames import abbreviate_address, map_addresses


def build_pool_ticker(
    trade_events: pd.DataFrame, user_map: pd.DataFrame, block_to_timestamp: pd.DataFrame
) -> pd.DataFrame:
    """Show recent trades wrt a pool.

    Arguments
    ---------
    trade_events: pd.DataFrame
        The dataframe resulting from `get_trade_events`.
    user_map: pd.DataFrame
        A dataframe with 4 columns (address, abbr_address, username, format_name).
        This is the output of :meth:`chainsync.dashboard.build_user_mapping`.

    Returns
    -------
    pd.DataFrame
        The filtered transaction data based on what we want to view in the ticker.
    """
    # Gather other information from other tables
    mapped_addrs = map_addresses(trade_events["wallet_address"], user_map)

    trade_events = trade_events.copy()
    trade_events["username"] = mapped_addrs["username"]

    # Look up block to timestamp
    trade_events = trade_events.merge(block_to_timestamp, how="left", on="block_number")

    rename_dict = {
        "timestamp": "Timestamp",
        "block_number": "Block Number",
        "username": "User",
        "wallet_address": "Wallet",
        "event_type": "Trade",
        "token_id": "Token",
        "token_delta": "Token Change",
        "base_delta": "Base Change",
        "as_base": "As Base",
    }
    trade_events = trade_events[list(rename_dict.keys())].rename(columns=rename_dict)

    # Shorten wallet address string
    trade_events["Wallet"] = mapped_addrs["abbr_address"]

    # Sort latest first
    return trade_events


def build_wallet_ticker(
    trade_events: pd.DataFrame,
    user_map: pd.DataFrame,
    hyperdrive_addr_map: pd.DataFrame,
    block_to_timestamp: pd.DataFrame,
) -> pd.DataFrame:
    """Show recent trades wrt a wallet.

    Arguments
    ---------
    trade_events: pd.DataFrame
        The dataframe resulting from `get_trade_events`.
    hyperdrive_addr_map: pd.DataFrame
        A dataframe with 2 columns (address, abbr_address, username, format_name).
        This is the output of :meth:`chainsync.dashboard.build_user_mapping`.

    Returns
    -------
    pd.DataFrame
        The filtered transaction data based on what we want to view in the ticker.
    """

    mapped_addrs = map_addresses(trade_events["wallet_address"], user_map)
    trade_events = trade_events.copy()
    trade_events["username"] = mapped_addrs["username"]

    # Do lookup from address to name
    hyperdrive_name = (
        trade_events["hyperdrive_address"]
        .to_frame()
        .merge(hyperdrive_addr_map, how="left", left_on="hyperdrive_address", right_on="hyperdrive_address")
    )["name"]

    trade_events["hyperdrive_name"] = hyperdrive_name

    # Look up block to timestamp
    trade_events = trade_events.merge(block_to_timestamp, how="left", on="block_number")

    rename_dict = {
        "timestamp": "Timestamp",
        "block_number": "Block Number",
        "hyperdrive_name": "Hyperdrive Name",
        "hyperdrive_address": "Hyperdrive Address",
        "username": "User",
        "wallet_address": "Wallet",
        "event_type": "Trade",
        "token_id": "Token",
        "token_delta": "Token Change",
        "base_delta": "Base Change",
        "as_base": "As Base",
    }
    trade_events = trade_events[list(rename_dict.keys())].rename(columns=rename_dict)

    # Shorten wallet address string
    trade_events["Wallet"] = mapped_addrs["abbr_address"]
    trade_events["Hyperdrive Address"] = abbreviate_address(trade_events["Hyperdrive Address"])

    # Sort latest first
    return trade_events
