"""The Hyperdrive pricing model"""
from __future__ import annotations  # types will be strings by default in 3.11

from typing import TYPE_CHECKING

from elfpy.pricing_models.yieldspace import YieldspacePricingModel
import elfpy.markets.hyperdrive.hyperdrive_actions as hyperdrive_actions
import elfpy.pricing_models.trades as trades
import elfpy.time as time
from elfpy.agents.agent import AgentTradeResult
import elfpy.types as types

if TYPE_CHECKING:
    import elfpy.markets.hyperdrive.hyperdrive_market as hyperdrive_market


class HyperdrivePricingModel(YieldspacePricingModel):
    """
    Hyperdrive Pricing Model

    This pricing model uses a combination of the Constant Sum and Yield Space
    invariants with modifications to the Yield Space invariant that enable the
    base reserves to be deposited into yield bearing vaults
    """

    def model_name(self) -> str:
        return "Hyperdrive"

    def model_type(self) -> str:
        return "hyperdrive"

    def calc_in_given_out(
        self,
        out: types.Quantity,
        market_state: hyperdrive_market.MarketState,
        time_remaining: time.StretchedTime,
    ) -> trades.TradeResult:
        r"""
        Calculates the amount of an asset that must be provided to receive a
        specified amount of the other asset given the current AMM reserves.

        The input is calculated as:

        .. math::
            \begin{align*}
            & s \;\;\;\; = \;\;\;\; \text{total_supply}\\
            & p \;\;\;\; = \;\;\;\; \Bigg(\dfrac{y + s}{\mu z}\Bigg)^{-\tau}
            \\\\
            & in' \;\;\:  = \;\;\:
            \begin{cases}
            \\
            \text{ if $token\_in$ = "base", }\\
            \quad\quad\quad c \big(\mu^{-1} \big(\mu \cdot c^{-1}
            \big(k - \big(y + s - \Delta y \cdot t\big)
            ^{1-\tau}\big)\big)
            ^ {\tfrac{1}{1-\tau}} - z\big) + \Delta y \cdot\big(1 - \tau\big)
            \\\\
            \text{ if $token\_in$ = "pt", }\\
            \quad\quad\quad (k - \big(
            c \cdot \mu^{-1} \cdot\big(\mu \cdot
            \big(z - \Delta z \cdot t\big)\big)^{1 - \tau} \big))
            ^{\tfrac{1}{1 - \tau}} - \big(y + s\big)
            + c \cdot \Delta z \cdot\big(1 - \tau\big)
            \\\\
            \end{cases}
            \\\\
            & f \;\;\;\; = \;\;\;\;
            \begin{cases}
            \\
            \text{ if $token\_in$ = "base", }\\\\
            \quad\quad\quad (1 - p) \phi\;\; \Delta y
            \\\\
            \text{ if $token\_in$ = "pt", }\\\\
            \quad\quad\quad (p^{-1} - 1) \enspace \phi \enspace (c \cdot \Delta z)
            \\\\
            \end{cases}
            \\\\\\
            & in = in' + f
            \\
            \end{align*}

        .. note::
           The pool total supply is a function of the base and bond reserves, and is modified in
           :func:`calc_lp_in_given_tokens_out
           <elfpy.pricing_models.yieldspace.YieldSpacePricingModel.calc_lp_in_given_tokens_out>`,
           :func:`calc_tokens_out_given_lp_in
           <elfpy.pricing_models.yieldspace.YieldSpacePricingModel.calc_tokens_out_given_lp_in>`,
           and :func:`calc_lp_out_given_tokens_in
           <elfpy.pricing_models.yieldspace.YieldSpacePricingModel.calc_lp_out_given_tokens_in>`.

           It can be approximated as :math:`s \approx y + cz`.

        Parameters
        ----------
        out : Quantity
            The quantity of tokens that the user wants to receive (the amount
            and the unit of the tokens).
        market_state : MarketState
            The state of the AMM's reserves and share prices.
        time_remaining : StretchedTime
            The time remaining for the asset (incorporates time stretch).

        Returns
        -------
        TradeResult
            The result of performing the trade
        """

        # Calculate some common values up front
        out_amount = out.amount
        normalized_time = time_remaining.normalized_time
        share_price = market_state.share_price
        d_bonds = out_amount * (1 - normalized_time)
        d_shares = d_bonds / share_price

        market_state = market_state.copy()

        # TODO: This is somewhat strange since these updates never actually hit the reserves.
        # Redeem the matured bonds 1:1 and simulate these updates hitting the reserves.
        if out.unit == types.TokenType.BASE:
            market_state.share_reserves -= d_shares
            market_state.bond_reserves += d_bonds
        elif out.unit == types.TokenType.PT:
            market_state.share_reserves += d_shares
            market_state.bond_reserves -= d_bonds
        else:
            raise AssertionError(
                "pricing_models.calc_in_given_out: ERROR: "
                f"Expected out.unit to be {types.TokenType.BASE} or {types.TokenType.PT}, not {out.unit}!"
            )
        # Trade the bonds that haven't matured on the YieldSpace curve.
        curve = super().calc_in_given_out(
            out=types.Quantity(amount=out_amount * normalized_time, unit=out.unit),
            market_state=market_state,
            time_remaining=time.StretchedTime(  # time remaining is always fixed to the full term for flat+curve
                days=time_remaining.normalizing_constant,  # position duration is the normalizing constant
                time_stretch=time_remaining.time_stretch,
                normalizing_constant=time_remaining.normalizing_constant,
            ),
        )

        # Compute flat part with fee
        flat_without_fee = out_amount * (1 - normalized_time)
        redemption_fee = flat_without_fee * market_state.redemption_fee_percent
        flat_with_fee = flat_without_fee + redemption_fee

        # Compute the user's trade result including both the flat and the curve parts of the trade.
        if out.unit == types.TokenType.BASE:
            user_result = AgentTradeResult(
                d_base=out.amount,
                d_bonds=-flat_with_fee + curve.user_result.d_bonds,
            )
            market_result = hyperdrive_actions.MarketActionResult(
                d_base=-out.amount,
                d_bonds=curve.market_result.d_bonds,
            )
        elif out.unit == types.TokenType.PT:
            user_result = AgentTradeResult(
                d_base=-flat_with_fee + curve.user_result.d_base,
                d_bonds=out.amount,
            )
            market_result = hyperdrive_actions.MarketActionResult(
                d_base=flat_with_fee + curve.market_result.d_base,
                d_bonds=curve.market_result.d_bonds,
            )
        else:
            raise AssertionError(
                f"ERROR: Expected out.unit to be {types.TokenType.BASE} or {types.TokenType.PT}, not {out.unit}!"
            )

        return trades.TradeResult(
            user_result=user_result,
            market_result=market_result,
            breakdown=trades.TradeBreakdown(
                without_fee_or_slippage=flat_without_fee + curve.breakdown.without_fee_or_slippage,
                without_fee=flat_without_fee + curve.breakdown.without_fee,
                fee=redemption_fee + curve.breakdown.fee,
                with_fee=flat_with_fee + curve.breakdown.with_fee,
            ),
        )

    # TODO: The high slippage tests in tests/test_pricing_model.py should
    # arguably have much higher slippage. This is something we should
    # consider more when thinking about the use of a time stretch parameter.
    def calc_out_given_in(
        self,
        in_: types.Quantity,
        market_state: hyperdrive_market.MarketState,
        time_remaining: time.StretchedTime,
    ) -> trades.TradeResult:
        r"""
        Calculates the amount of an asset that must be provided to receive a specified amount of the
        other asset given the current AMM reserves.

        The output is calculated as:

        .. math::
            \begin{align*}
            & s \;\;\;\; = \;\;\;\; \text{total_supply}\\
            & p \;\;\;\; = \;\;\;\; \Bigg(\dfrac{y + s}{\mu z}\Bigg)^{-\tau}
            \\\\
            & out'\;\; = \;\;
            \begin{cases}
            \\
            \text{ if $token\_out$ = "base", }\\
            \quad\quad\quad c \big(z - \mu^{-1}
            \big(c \cdot \mu^{-1} \big(k - \big(y + s + \Delta y \cdot t\big)
            ^{1 - \tau}\big)\big)
            ^{\tfrac{1}{1 - \tau}}\big) + \Delta y \cdot (1 - \tau)
            \\\\
            \text{ if $token\_out$ = "pt", }\\
            \quad\quad\quad y + s - (k - c \cdot \mu^{-1} \cdot
            (\mu (z + \Delta z \cdot t))^{1 - \tau})
            ^{\tfrac{1}{1 - \tau}} + c \cdot \Delta z \cdot (1 - \tau)
            \\\\
            \end{cases}
            \\\\
            & f \;\;\;\; = \;\;\;\;
            \begin{cases}
            \\
            \text{ if $token\_out$ = "base", }\\\\
            \quad\quad\quad (1 - p) \phi\;\; \Delta y
            \\\\
            \text{ if $token\_out$ = "pt", }\\\\
            \quad\quad\quad (p^{-1} - 1) \enspace \phi \enspace (c \cdot \Delta z)
            \\\\
            \end{cases}
            \\\\\\
            & out = out' + f
            \\
            \end{align*}

        .. note::
           The pool total supply is a function of the base and bond reserves, and is modified in
           :func:`calc_lp_in_given_tokens_out
           <elfpy.pricing_models.yieldspace.YieldSpacePricingModel.calc_lp_in_given_tokens_out>`,
           :func:`calc_tokens_out_given_lp_in
           <elfpy.pricing_models.yieldspace.YieldSpacePricingModel.calc_tokens_out_given_lp_in>`,
           and :func:`calc_lp_out_given_tokens_in
           <elfpy.pricing_models.yieldspace.YieldSpacePricingModel.calc_lp_out_given_tokens_in>`.

           It can be approximated as :math:`s \approx y + cz`.

        Parameters
        ----------
        in_ : Quantity
            The quantity of tokens that the user wants to pay (the amount
            and the unit of the tokens).
        market_state : MarketState
            The state of the AMM's reserves and share prices.
        time_remaining : StretchedTime
            The time remaining for the asset (incorporates time stretch).

        Returns
        -------
        TradeResult
            The result of performing the trade.
        """
        # Calculate some common values up front
        in_amount = in_.amount
        normalized_time = time_remaining.normalized_time
        share_price = market_state.share_price
        d_bonds = in_amount * (1 - normalized_time)
        d_shares = d_bonds / share_price
        # Redeem the matured bonds 1:1 and simulate these updates hitting the reserves.
        market_state = market_state.copy()  # don't want to modify the actual market state
        if in_.unit == types.TokenType.BASE:
            market_state.share_reserves += d_shares
            market_state.bond_reserves -= d_bonds
        elif in_.unit == types.TokenType.PT:
            market_state.share_reserves -= d_shares
            market_state.bond_reserves += d_bonds
        else:
            raise AssertionError(
                "pricing_models.calc_out_given_in: ERROR: "
                f"Expected in_.unit to be {types.TokenType.BASE} or {types.TokenType.PT}, not {in_.unit}!"
            )
        # Trade the bonds that haven't matured on the YieldSpace curve.
        curve = super().calc_out_given_in(
            in_=types.Quantity(amount=in_amount * normalized_time, unit=in_.unit),
            market_state=market_state,
            time_remaining=time.StretchedTime(  # time remaining is always fixed to the full term for the curve
                days=time_remaining.normalizing_constant,  # position duration is the normalizing constant
                time_stretch=time_remaining.time_stretch,
                normalizing_constant=time_remaining.normalizing_constant,
            ),
        )
        # Compute flat part with fee
        flat_without_fee = in_amount * (1 - normalized_time)
        redemption_fee = flat_without_fee * market_state.redemption_fee_percent
        flat_with_fee = flat_without_fee - redemption_fee
        # Compute the user's trade result including both the flat and the curve parts of the trade.
        if in_.unit == types.TokenType.BASE:
            user_result = AgentTradeResult(
                d_base=-in_.amount,
                d_bonds=flat_with_fee + curve.user_result.d_bonds,
            )
            market_result = hyperdrive_actions.MarketActionResult(
                d_base=in_.amount,
                d_bonds=curve.market_result.d_bonds,
            )
        elif in_.unit == types.TokenType.PT:
            user_result = AgentTradeResult(
                d_base=flat_with_fee + curve.user_result.d_base,
                d_bonds=-in_.amount,
            )
            market_result = hyperdrive_actions.MarketActionResult(
                d_base=-flat_with_fee + curve.market_result.d_base,
                d_bonds=curve.market_result.d_bonds,
            )
        else:
            raise AssertionError(
                "pricing_models.calc_out_given_in: ERROR: "
                f"Expected in_.unit to be {types.TokenType.BASE} or {types.TokenType.PT}, not {in_.unit}!"
            )
        return trades.TradeResult(
            user_result=user_result,
            market_result=market_result,
            breakdown=trades.TradeBreakdown(
                without_fee_or_slippage=flat_without_fee + curve.breakdown.without_fee_or_slippage,
                without_fee=flat_without_fee + curve.breakdown.without_fee,
                fee=curve.breakdown.fee + redemption_fee,
                with_fee=flat_with_fee + curve.breakdown.with_fee,
            ),
        )
