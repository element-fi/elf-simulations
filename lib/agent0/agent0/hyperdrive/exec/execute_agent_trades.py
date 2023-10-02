"""Main script for running agents on Hyperdrive."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, NoReturn

from agent0.base import Quantity, TokenType
from agent0.hyperdrive.state import (
    HyperdriveActionType,
    HyperdriveMarketAction,
    HyperdriveWalletDeltas,
    Long,
    Short,
    TradeResult,
    TradeStatus,
)
from elfpy import types
from ethpy.hyperdrive import HyperdriveInterface
from fixedpointmath import FixedPoint

if TYPE_CHECKING:
    from agent0.hyperdrive.agents import HyperdriveAgent


def assert_never(arg: NoReturn) -> NoReturn:
    """Helper function for exhaustive matching on ENUMS.

    .. note::
        This ensures that all ENUM values are checked, via an exhaustive match:
        https://github.com/microsoft/pyright/issues/2569
    """
    assert False, f"Unhandled type: {type(arg).__name__}"


async def async_execute_single_agent_trade(
    agent: HyperdriveAgent,
    hyperdrive: HyperdriveInterface,
) -> list[TradeResult]:
    """Executes a single agent's trade. This function is async as
    `match_contract_call_to_trade` waits for a transaction receipt.

    Arguments
    ---------
    agent: HyperdriveAgent
        The HyperdriveAgent that is conducting the trade
    hyperdrive : HyperdriveInterface
        The Hyperdrive API interface object

    Returns
    -------
    """
    trades: list[types.Trade[HyperdriveMarketAction]] = agent.get_trades(interface=hyperdrive)

    # Make trades async for this agent. This way, an agent can submit multiple trades for a single block
    # This unblocks any other agents running here as well, as previously, an agent would take one block per trade
    # which blocks all other agents from making trades until all trades are finished.

    # TODO preliminary search shows async tasks has very low overhead:
    # https://stackoverflow.com/questions/55761652/what-is-the-overhead-of-an-asyncio-task
    # However, should probably test what the limit number of trades an agent can make in one block
    wallet_deltas_or_exception: list[HyperdriveWalletDeltas | Exception] = await asyncio.gather(
        *[async_match_contract_call_to_trade(agent, hyperdrive, trade_object) for trade_object in trades],
        # Instead of throwing exception, return the exception to the caller here
        return_exceptions=True,
    )

    # TODO Here, gather returns results based on original order of trades, but this order isn't guaranteed
    # because of async. Ideally, we should return results based on the order of trades. Can we use nonce here
    # to see order?

    # Sanity check
    assert len(wallet_deltas_or_exception) == len(trades)

    # The wallet update after should be fine, since we can see what trades went through
    # and only apply those wallet deltas. Wallet deltas are also invariant to order
    # as long as the transaction went through.
    trade_results = []
    for result, trade_object in zip(wallet_deltas_or_exception, trades):
        if isinstance(result, HyperdriveWalletDeltas):
            agent.wallet.update(result)
            trade_result = TradeResult(status=TradeStatus.SUCCESS, exception=None, agent=agent, trade=trade_object)
        elif isinstance(result, Exception):
            trade_result = TradeResult(status=TradeStatus.FAIL, exception=result, agent=agent, trade=trade_object)
        else:
            # Should never get here
            # TODO this function was originally used for types
            # Is this okay to use here?
            assert_never(result)
        trade_results.append(trade_result)

    return trade_results


async def async_execute_agent_trades(
    hyperdrive: HyperdriveInterface,
    agents: list[HyperdriveAgent],
) -> None:
    """Hyperdrive forever into the sunset.

    Arguments
    ---------
    hyperdrive : HyperdriveInterface
        The Hyperdrive API interface object
    agents : list[HyperdriveAgent]
        A list of HyperdriveAgent that are conducting the trades
    """
    # Make calls per agent to execute_single_agent_trade
    # Await all trades to finish before continuing
    await asyncio.gather(*[async_execute_single_agent_trade(agent, hyperdrive) for agent in agents])


async def async_match_contract_call_to_trade(
    agent: HyperdriveAgent,
    hyperdrive: HyperdriveInterface,
    trade_envelope: types.Trade[HyperdriveMarketAction],
) -> HyperdriveWalletDeltas:
    """Match statement that executes the smart contract trade based on the provided type.

    Arguments
    ---------
    agent : HyperdriveAgent
        Object containing a wallet address and Elfpy Agent for determining trades
    hyperdrive : HyperdriveInterface
        The Hyperdrive API interface object
    trade_object : Trade
        A specific trade requested by the given agent

    Returns
    -------
    HyperdriveWalletDeltas
        Deltas to be applied to the agent's wallet

    """
    # TODO: figure out fees paid
    trade = trade_envelope.market_action
    match trade.action_type:
        case HyperdriveActionType.INITIALIZE_MARKET:
            raise ValueError(f"{trade.action_type} not supported!")

        case HyperdriveActionType.OPEN_LONG:
            trade_result = await hyperdrive.async_open_long(agent, trade.trade_amount, trade.slippage_tolerance)
            wallet_deltas = HyperdriveWalletDeltas(
                balance=Quantity(
                    amount=-trade_result.base_amount,
                    unit=TokenType.BASE,
                ),
                longs={trade_result.maturity_time_seconds: Long(trade_result.bond_amount)},
            )

        case HyperdriveActionType.CLOSE_LONG:
            if not trade.maturity_time:
                raise ValueError("Maturity time was not provided, can't close long position.")
            trade_result = await hyperdrive.async_close_long(
                agent, trade.trade_amount, trade.maturity_time, trade.slippage_tolerance
            )
            wallet_deltas = HyperdriveWalletDeltas(
                balance=Quantity(
                    amount=trade_result.base_amount,
                    unit=TokenType.BASE,
                ),
                longs={trade.maturity_time: Long(-trade_result.bond_amount)},
            )

        case HyperdriveActionType.OPEN_SHORT:
            trade_result = await hyperdrive.async_open_short(agent, trade.trade_amount, trade.slippage_tolerance)
            wallet_deltas = HyperdriveWalletDeltas(
                balance=Quantity(
                    amount=-trade_result.base_amount,
                    unit=TokenType.BASE,
                ),
                shorts={trade_result.maturity_time_seconds: Short(balance=trade_result.bond_amount)},
            )

        case HyperdriveActionType.CLOSE_SHORT:
            if not trade.maturity_time:
                raise ValueError("Maturity time was not provided, can't close long position.")
            trade_result = await hyperdrive.async_close_short(
                agent, trade.trade_amount, trade.maturity_time, trade.slippage_tolerance
            )
            wallet_deltas = HyperdriveWalletDeltas(
                balance=Quantity(
                    amount=trade_result.base_amount,
                    unit=TokenType.BASE,
                ),
                shorts={trade.maturity_time: Short(balance=-trade_result.bond_amount)},
            )

        case HyperdriveActionType.ADD_LIQUIDITY:
            # TODO: The following variables are hard coded for now, but should be specified in the trade spec
            min_apr = FixedPoint(scaled_value=1)  # 1e-18
            max_apr = FixedPoint(1)  # 1.0
            trade_result = await hyperdrive.async_add_liquidity(agent, trade.trade_amount, min_apr, max_apr)
            wallet_deltas = HyperdriveWalletDeltas(
                balance=Quantity(
                    amount=-trade_result.base_amount,
                    unit=TokenType.BASE,
                ),
                lp_tokens=trade_result.lp_amount,
            )

        case HyperdriveActionType.REMOVE_LIQUIDITY:
            trade_result = await hyperdrive.async_remove_liquidity(agent, trade.trade_amount)
            wallet_deltas = HyperdriveWalletDeltas(
                balance=Quantity(
                    amount=trade_result.base_amount,
                    unit=TokenType.BASE,
                ),
                lp_tokens=-trade_result.lp_amount,
                withdraw_shares=trade_result.withdrawal_share_amount,
            )

        case HyperdriveActionType.REDEEM_WITHDRAW_SHARE:
            trade_result = await hyperdrive.async_redeem_withdraw_shares(agent, trade.trade_amount)
            wallet_deltas = HyperdriveWalletDeltas(
                balance=Quantity(
                    amount=trade_result.base_amount,
                    unit=TokenType.BASE,
                ),
                withdraw_shares=-trade_result.withdrawal_share_amount,
            )

        case _:
            assert_never(trade.action_type)
    return wallet_deltas
