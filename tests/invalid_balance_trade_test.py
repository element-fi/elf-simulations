"""Test for invalid trades due to balance."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from fixedpointmath import FixedPoint
from pypechain.core import PypechainCallException
from utils import expect_failure_with_funded_bot, expect_failure_with_non_funded_bot  # type: ignore
from web3.exceptions import ContractCustomError, ContractPanicError

from agent0.core.base import Trade
from agent0.core.hyperdrive import HyperdriveMarketAction, HyperdriveWallet
from agent0.core.hyperdrive.agent import (
    add_liquidity_trade,
    close_long_trade,
    close_short_trade,
    open_long_trade,
    open_short_trade,
    remove_liquidity_trade,
)
from agent0.core.hyperdrive.interactive import LocalHyperdrive
from agent0.core.hyperdrive.policies import HyperdriveBasePolicy

if TYPE_CHECKING:
    from agent0.ethpy.hyperdrive import HyperdriveReadInterface

# ruff: noqa: PLR2004 (magic values used for counter)


# Start by defining policies for failed trades
# One policy per failed trade
# Starting with empty wallet, catching any closing trades.

# TODO clean up this test by not using policies and instead executing trades directly


class InvalidAddLiquidity(HyperdriveBasePolicy):
    """An agent that submits a remove liquidity with a zero wallet."""

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Remove liquidity.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        action_list = []
        # Adding liquidity more base than what I have
        action_list.append(add_liquidity_trade(FixedPoint(20_000)))
        return action_list, True


class InvalidOpenLong(HyperdriveBasePolicy):
    """An agent that submits a remove liquidity with a zero wallet."""

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Remove liquidity.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        action_list = []
        # Opening a long for more base than what I have
        action_list.append(open_long_trade(FixedPoint(500)))
        return action_list, True


class InvalidOpenShort(HyperdriveBasePolicy):
    """An agent that submits a remove liquidity with a zero wallet."""

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Remove liquidity.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        action_list = []
        # Opening a short for bonds for more than what I have
        action_list.append(open_short_trade(FixedPoint(50)))
        return action_list, True


class InvalidRemoveLiquidityFromZero(HyperdriveBasePolicy):
    """An agent that submits a remove liquidity with a zero wallet."""

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Remove liquidity.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        action_list = []
        # Remove non-existing Liquidity
        action_list.append(remove_liquidity_trade(FixedPoint(20_000)))
        return action_list, True


class InvalidCloseLongFromZero(HyperdriveBasePolicy):
    """An agent that submits a close long with a zero wallet."""

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Close long.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        # Closing non-existent long
        action_list = [
            close_long_trade(FixedPoint(20_000), maturity_time=1699561146, slippage_tolerance=self.slippage_tolerance)
        ]
        return action_list, True


class InvalidCloseShortFromZero(HyperdriveBasePolicy):
    """An agent that submits a close short with a zero wallet."""

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Close short.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        # Closing non-existent short
        action_list = [
            close_short_trade(FixedPoint(20_000), maturity_time=1699561146, slippage_tolerance=self.slippage_tolerance)
        ]
        return action_list, True


class InvalidRemoveLiquidityFromNonZero(HyperdriveBasePolicy):
    """An agent that submits an invalid remove liquidity share with a non-zero wallet."""

    counter = 0

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Alternate between adding and removing liquidity.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        action_list = []
        done_trading = False
        if self.counter == 0:
            # Add liquidity
            action_list.append(add_liquidity_trade(FixedPoint(10_000)))
        elif self.counter == 1:
            # Remove Liquidity for more than I have
            action_list.append(remove_liquidity_trade(FixedPoint(20_000)))
            done_trading = True
        self.counter += 1
        return action_list, done_trading


class InvalidCloseLongFromNonZero(HyperdriveBasePolicy):
    """An agent that submits an invalid close long with a non-zero wallet."""

    counter = 0

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Alternate between open and close long.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        action_list = []
        done_trading = False
        if self.counter == 0:
            # Add liquidity, as we need liquidity in the pool for the other trades
            action_list.append(add_liquidity_trade(FixedPoint(100_000)))
        elif self.counter == 1:
            # Open Long
            action_list.append(open_long_trade(FixedPoint(10_000), self.slippage_tolerance))
        elif self.counter == 2:
            # Closing existent long for more than I have
            assert len(wallet.longs) == 1
            for long_time in wallet.longs.keys():
                action_list.append(close_long_trade(FixedPoint(20_000), long_time, self.slippage_tolerance))
            done_trading = True
        self.counter += 1
        return action_list, done_trading


class InvalidCloseShortFromNonZero(HyperdriveBasePolicy):
    """An agent that submits an invalid close short with a non-zero wallet."""

    counter = 0

    def action(
        self, interface: HyperdriveReadInterface, wallet: HyperdriveWallet
    ) -> tuple[list[Trade[HyperdriveMarketAction]], bool]:
        """Alternate between open and close short.

        Arguments
        ---------
        interface: HyperdriveReadInterface
            The trading market interface.
        wallet: HyperdriveWallet
            The agent's wallet.

        Returns
        -------
        tuple[list[HyperdriveMarketAction], bool]
            A tuple where the first element is a list of actions,
            and the second element defines if the agent is done trading
        """
        # pylint: disable=unused-argument
        action_list = []
        done_trading = False
        if self.counter == 0:
            # Add liquidity, as we need liquidity in the pool for the other trades
            action_list.append(add_liquidity_trade(FixedPoint(100_000)))
        if self.counter == 1:
            # Open Short
            action_list.append(open_short_trade(FixedPoint(10_000), self.slippage_tolerance))
        elif self.counter == 2:
            # Closing existent short for more than I have
            assert len(wallet.shorts) == 1
            for short_time in wallet.shorts.keys():
                action_list.append(close_short_trade(FixedPoint(20_000), short_time, self.slippage_tolerance))
            done_trading = True
        self.counter += 1
        return action_list, done_trading


class TestInvalidTrades:
    """Test pipeline from bots making trades to viewing the trades in the db."""

    @pytest.mark.anvil
    def test_invalid_add_liquidity(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Tests when making a trade with not enough base in wallet."""
        try:
            expect_failure_with_non_funded_bot(fast_hyperdrive_fixture, InvalidAddLiquidity)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            # Fails on add liquidity
            assert exc.function_name == "addLiquidity"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractPanicError)
            assert (
                exc.orig_exception.args[0] == "Panic error 0x11: Arithmetic operation results in underflow or overflow."
            )

    @pytest.mark.anvil
    def test_invalid_open_long(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Tests when making a trade with not enough base in wallet."""
        try:
            expect_failure_with_non_funded_bot(fast_hyperdrive_fixture, InvalidOpenLong)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            # Fails on open long
            assert exc.function_name == "openLong"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractPanicError)
            assert (
                exc.orig_exception.args[0] == "Panic error 0x11: Arithmetic operation results in underflow or overflow."
            )

    @pytest.mark.anvil
    def test_invalid_open_short(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Tests when making a trade with not enough base in wallet."""
        try:
            expect_failure_with_non_funded_bot(fast_hyperdrive_fixture, InvalidOpenShort)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            # Fails on open short
            assert exc.function_name == "openShort"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractPanicError)
            assert (
                exc.orig_exception.args[0] == "Panic error 0x11: Arithmetic operation results in underflow or overflow."
            )

    @pytest.mark.anvil
    def test_invalid_remove_liquidity_from_zero(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Test making a invalid remove liquidity with zero lp tokens."""
        try:
            expect_failure_with_funded_bot(fast_hyperdrive_fixture, InvalidRemoveLiquidityFromZero)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            # Fails on remove liquidity
            assert exc.function_name == "removeLiquidity"
            assert exc.decoded_error == "InsufficientBalance()"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractCustomError)

    @pytest.mark.anvil
    def test_invalid_close_long_from_zero(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Test making a invalid close long with zero long tokens."""
        try:
            expect_failure_with_funded_bot(fast_hyperdrive_fixture, InvalidCloseLongFromZero)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            assert "long token not found in wallet" in exc.args[0]
            # Fails on close long
            assert exc.function_name == "closeLong"
            assert exc.decoded_error == "InsufficientBalance()"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractCustomError)

    @pytest.mark.anvil
    def test_invalid_close_short_from_zero(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Test making a invalid close long with zero long tokens."""
        try:
            expect_failure_with_funded_bot(fast_hyperdrive_fixture, InvalidCloseShortFromZero)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            assert "short token not found in wallet" in exc.args[0]
            # Fails on close long
            assert exc.function_name == "closeShort"
            assert exc.decoded_error == "InsufficientBalance()"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractCustomError)

    @pytest.mark.anvil
    def test_invalid_remove_liquidity_from_nonzero(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Test making a invalid remove liquidity trade with nonzero lp tokens."""
        try:
            expect_failure_with_funded_bot(fast_hyperdrive_fixture, InvalidRemoveLiquidityFromNonZero)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            # Fails on remove liquidity
            assert exc.function_name == "removeLiquidity"
            assert exc.decoded_error == "InsufficientBalance()"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractCustomError)

    @pytest.mark.anvil
    def test_invalid_close_long_from_nonzero(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Test when making a invalid close long with nonzero long tokens."""
        try:
            expect_failure_with_funded_bot(fast_hyperdrive_fixture, InvalidCloseLongFromNonZero)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            # Fails on closeLong
            assert exc.function_name == "closeLong"
            assert exc.decoded_error == "InsufficientBalance()"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractCustomError)

    @pytest.mark.anvil
    def test_invalid_close_short_from_nonzero(
        self,
        fast_hyperdrive_fixture: LocalHyperdrive,
    ):
        """Test making a invalid close short with nonzero short tokens."""
        try:
            expect_failure_with_funded_bot(fast_hyperdrive_fixture, InvalidCloseShortFromNonZero)
        except PypechainCallException as exc:
            # Expected error due to illegal trade
            # We do add an argument for invalid balance to the args, so check for that here
            assert "Invalid balance:" in exc.args[0]
            # Fails on closeShort
            assert exc.function_name == "closeShort"
            assert exc.decoded_error == "InsufficientBalance()"
            assert exc.orig_exception is not None
            assert isinstance(exc.orig_exception, ContractCustomError)
