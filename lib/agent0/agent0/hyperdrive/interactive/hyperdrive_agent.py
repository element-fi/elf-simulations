"""The hyperdrive agent object that encapsulates an agent."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fixedpointmath import FixedPoint

if TYPE_CHECKING:
    from typing import Type

    from eth_typing import ChecksumAddress

    from agent0.hyperdrive import HyperdriveWallet
    from agent0.hyperdrive.policies import HyperdriveBasePolicy

    from .event_types import (
        AddLiquidity,
        CloseLong,
        CloseShort,
        OpenLong,
        OpenShort,
        RedeemWithdrawalShares,
        RemoveLiquidity,
    )
    from .hyperdrive import Hyperdrive


class InteractiveHyperdriveAgent:
    def __init__(
        self,
        pool: Hyperdrive,
        policy: Type[HyperdriveBasePolicy] | None,
        policy_config: HyperdriveBasePolicy.Config | None,
        private_key: str,
    ) -> None:
        """Constructor for the interactive hyperdrive agent.
        NOTE: this constructor shouldn't be called directly, but rather from Hyperdrive's
        `init_agent` method.

        Arguments
        ---------
        pool: Hyperdrive
            The pool object that this agent belongs to.
        policy: Type[HyperdriveBasePolicy] | None
            An optional policy to attach to this agent.
        policy_config: HyperdriveBasePolicy.Config | None,
            The configuration for the attached policy.
        private_key: str | None, optional
            The private key of the associated account. Default is auto-generated.
        """
        self._pool = pool
        self.agent = self._pool._init_agent(policy, policy_config, private_key)

    @property
    def wallet(self) -> HyperdriveWallet:
        """Returns the agent's current wallet.

        Returns
        -------
        HyperdriveWallet
            The agent's current wallet.
        """
        return self.agent.wallet

    @property
    def checksum_address(self) -> ChecksumAddress:
        """Return the checksum address of the account."""
        return self.agent.checksum_address

    def open_long(self, base: FixedPoint) -> OpenLong:
        """Opens a long for this agent.

        Arguments
        ---------
        base: FixedPoint
            The amount of longs to open in units of base.

        Returns
        -------
        OpenLong
            The emitted event of the open long call.
        """
        return self._pool._open_long(self.agent, base)

    def close_long(self, maturity_time: int, bonds: FixedPoint) -> CloseLong:
        """Closes a long for this agent.

        Arguments
        ---------
        maturity_time: int
            The maturity time of the bonds to close. This is the identifier of the long tokens.
        bonds: FixedPoint
            The amount of longs to close in units of bonds.

        Returns
        -------
        CloseLong
            The emitted event of the close long call.
        """
        return self._pool._close_long(self.agent, maturity_time, bonds)

    def open_short(self, bonds: FixedPoint) -> OpenShort:
        """Opens a short for this agent.

        Arguments
        ---------
        bonds: FixedPoint
            The amount of shorts to open in units of bonds.

        Returns
        -------
        OpenShort
            The emitted event of the open short call.
        """
        return self._pool._open_short(self.agent, bonds)

    def close_short(self, maturity_time: int, bonds: FixedPoint) -> CloseShort:
        """Closes a short for this agent.

        Arguments
        ---------
        maturity_time: int
            The maturity time of the bonds to close. This is the identifier of the short tokens.
        bonds: FixedPoint
            The amount of shorts to close in units of bonds.

        Returns
        -------
        CloseShort
            The emitted event of the close short call.
        """
        return self._pool._close_short(self.agent, maturity_time, bonds)

    def add_liquidity(self, base: FixedPoint) -> AddLiquidity:
        """Adds liquidity for this agent.

        Arguments
        ---------
        base: FixedPoint
            The amount of liquidity to add in units of base.

        Returns
        -------
        AddLiquidity
            The emitted event of the add liquidity call.
        """
        return self._pool._add_liquidity(self.agent, base)

    def remove_liquidity(self, shares: FixedPoint) -> RemoveLiquidity:
        """Removes liquidity for this agent.

        Arguments
        ---------
        shares: FixedPoint
            The amount of liquidity to remove in units of shares.

        Returns
        -------
        RemoveLiquidity
            The emitted event of the remove liquidity call.
        """
        return self._pool._remove_liquidity(self.agent, shares)

    def redeem_withdraw_share(self, shares: FixedPoint) -> RedeemWithdrawalShares:
        """Redeems withdrawal shares for this agent.

        Arguments
        ---------
        shares: FixedPoint
            The amount of withdrawal shares to redeem in units of shares.

        Returns
        -------
        RedeemWithdrawalShares
            The emitted event of the redeem withdrawal shares call.
        """
        return self._pool._redeem_withdraw_share(self.agent, shares)

    def execute_policy_action(
        self,
    ) -> list[OpenLong | OpenShort | CloseLong | CloseShort | AddLiquidity | RemoveLiquidity | RedeemWithdrawalShares]:
        """Executes the underlying policy action (if set).

        Returns
        -------
        list[OpenLong | OpenShort | CloseLong | CloseShort | AddLiquidity | RemoveLiquidity | RedeemWithdrawalShares]
            Events of the executed actions.
        """
        return self._pool._execute_policy_action(self.agent)

    def liquidate(
        self, randomize: bool = False
    ) -> list[CloseLong | CloseShort | RemoveLiquidity | RedeemWithdrawalShares]:
        """Liquidate all of the agent's positions.

        Arguments
        ---------
        randomize: bool, optional
            Whether to randomize liquidation trades. Defaults to False.

        Returns
        -------
        list[CloseLong | CloseShort | RemoveLiquidity | RedeemWithdrawalShares]
            Events of the executed actions.
        """
        return self._pool._liquidate(self.agent, randomize)
