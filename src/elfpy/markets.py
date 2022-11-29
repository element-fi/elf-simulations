"""
Market simulators store state information when interfacing AMM pricing models with users

TODO: rewrite all functions to have typed inputs
"""

import time
from dataclasses import dataclass, field

import numpy as np

import elfpy.utils.time as time_utils
from elfpy.user import AgentWallet
from elfpy.utils.bcolors import bcolors
import elfpy.utils.price as price_utils
from elfpy.utils.float_to_string import float_to_string

# Currently many functions use >5 arguments.
# These should be packaged up into shared variables, e.g.
#     reserves = (in_reserves, out_reserves)
#     share_prices = (init_share_price, share_price)
# pylint: disable=too-many-arguments


@dataclass(frozen=False)
class MarketDeltas:
    """specifies changes to values in the market"""

    d_base_asset: float = 0
    d_token_asset: float = 0
    d_share_buffer: float = 0
    d_bond_buffer: float = 0
    d_liquidity_pool: float = 0
    d_liquidity_pool_history: list = field(default_factory=list)
    d_base_asset_slippage: float = 0
    d_token_asset_slippage: float = 0
    d_share_fee: float = 0
    d_share_fee_history: dict = field(default_factory=dict)
    d_token_fee: float = 0
    d_token_fee_history: dict = field(default_factory=dict)
    d_base_asset_orders: int = 0
    d_token_asset_orders: int = 0
    d_base_asset_volume: float = 0
    d_token_asset_volume: float = 0

    def __getitem__(self, key):
        getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __str__(self):
        output_string = ""
        for key, value in vars(self).items():
            if value:  #  check if object exists
                if value != 0:
                    output_string += f" {key}: "
                    if isinstance(value, float):
                        output_string += f"{float_to_string(value)}"
                    elif isinstance(value, list):
                        output_string += "[" + ", ".join([float_to_string(x) for x in value]) + "]"
                    elif isinstance(value, dict):
                        output_string += "{" + ", ".join([f"{k}: {float_to_string(v)}" for k, v in value.items()]) + "}"
                    else:
                        output_string += f"{value}"
        return output_string


class Market:
    """
    Holds state variables for market simulation and executes trades.

    The Market class executes trades by updating market variables according to the given pricing model.
    It also has some helper variables for assessing pricing model values given market conditions.
    """

    # TODO: set up member object that owns attributes instead of so many individual instance attributes
    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        fee_percent,
        token_duration,
        pricing_model,
        share_reserves=0,
        bond_reserves=0,
        liquidity_pool=0,
        time_stretch_constant=1,
        init_share_price=1,
        share_price=1,
        verbose=False,
    ):
        self.time = 0  # time in year fractions
        self.share_reserves = share_reserves  # z
        self.bond_reserves = bond_reserves  # y
        self.share_buffer = 0
        self.bond_buffer = 0
        self.liquidity_pool = liquidity_pool
        self.liquidity_pool_history = []  # list trades by user and time, initialize as empty list to allow appending
        self.fee_percent = fee_percent  # g
        self.time_stretch_constant = time_stretch_constant
        self.init_share_price = init_share_price  # u normalizing constant
        self.share_price = share_price  # c
        self.token_duration = token_duration  # how long does a token last before expiry
        self.pricing_model = pricing_model
        # TODO: It would be good to remove the tight coupling between pricing models and markets.
        #       For now, it makes sense to restrict the behavior at the market level since
        #       previous versions of Element didn't allow for shorting (despite the fact that
        #       their pricing models can support shorting).
<<<<<<< HEAD
        pricing_model_name = self.pricing_model.model_name()
        if pricing_model_name == "Element":
            self.allowed_actions = ["open_long",
                "close_long", 
                "add_liquidity",
                "remove_liquidity"]
        elif pricing_model_name == "Hyperdrive":
            self.allowed_actions = [
                "open_long",
                "close_long",
                "open_short",
                "close_short",
                "add_liquidity",
                "remove_liquidity",
            ]
        else:
            raise AssertionError(
                'markets.__init__: ERROR: self.pricing.model_name() should be "Element" or "Hyperdrive", not'
                f" {pricing_model_name}!"
            )
=======
        self.time_stretch_constant = time_stretch_constant
>>>>>>> 4225993 (implement suggestions part two)
        self.base_asset_orders = 0
        self.token_asset_orders = 0
        self.base_asset_volume = 0
        self.token_asset_volume = 0
        self.cum_token_asset_slippage = 0
        self.cum_base_asset_slippage = 0
        self.share_fees = 0
        self.share_fee_history = {}
        self.token_fees = 0
        self.token_fee_history = {}
        self.spot_price = None
        self.total_supply = self.share_reserves + self.bond_reserves
        self.verbose = verbose

    def trade_and_update(self, agent_action):
        """
        Execute a trade in the simulated market.

        check which of 6 action types are being executed, and handles each case:
        open_long
        close_long
        open_short
        close_short
        add_liquidity
            pricing model computes new market deltas
            market updates its "liquidity pool" wallet, which stores each trade's mint time and user address
            LP tokens are also stored in user wallet as fungible amounts, for ease of use
        remove_liquidity
            market figures out how much the user has contributed (calcualtes their fee weighting)
            market resolves fees, adds this to the agent_action (optional function, to check AMM logic)
            pricing model computes new market deltas
            market updates its "liquidity pool" wallet, which stores each trade's mint time and user address
            LP tokens are also stored in user wallet as fungible amounts, for ease of use
        """
        # ensure that the user action is an allowed action for this market
        allowed_actions = []
        if self.pricing_model.model_name() == "Element":
            allowed_actions = ["open_long", "close_long", "add_liquidity", "remove_liquidity"]
        elif self.pricing_model.model_name() == "Hyperdrive":
            allowed_actions = [
                "open_long",
                "close_long",
                "open_short",
                "close_short",
                "add_liquidity",
                "remove_liquidity",
            ]
        if not agent_action.action_type in allowed_actions:
            raise AssertionError(
                "markets.trade_and_update: ERROR: agent_action.action_type should be an allowed action for the"
                f" model={self.pricing_model.model_name()}, not {agent_action.action_type}!"
            )
        # TODO: check the desired amount is feasible, otherwise return descriptive error
        # update market variables which may have changed since the user action was created
        agent_action.update_market_variables(market=self)
        agent_action.print_description_string()

        # for each position, specify how to forumulate trade and then execute
        if agent_action.action_type == "open_long":  # buy to open long
            agent_action.direction = "out"  # calcOutGivenIn
            agent_action.token_out = "pt"  # sell known base for unknown PT
            market_deltas, agent_deltas = self._open_long(agent_action)
        elif agent_action.action_type == "close_long":  # sell to close long
            agent_action.direction = "out"  # calcOutGivenIn
            agent_action.token_out = "base"  # sell known PT for unknown base
            market_deltas, agent_deltas = self._close_long(agent_action)
        elif agent_action.action_type == "open_short":  # sell PT to open short
            agent_action.direction = "in"  # calcOutGivenIn
            agent_action.token_out = "pt"  # sell known PT for unknown base
            market_deltas, agent_deltas = self._open_short(agent_action)
        elif agent_action.action_type == "close_short":  # buy PT to close short
            agent_action.direction = "in"  # calcOutGivenIn
            agent_action.token_in = "pt"  # buy known PT for unknown base
            market_deltas, agent_deltas = self._close_short(agent_action)
        elif agent_action.action_type == "add_liquidity":
            market_deltas, agent_deltas = self._add_liquidity(agent_action)
        elif agent_action.action_type == "remove_liquidity":
            market_deltas, agent_deltas = self._remove_liquidity(agent_action)
        else:
            raise ValueError(f'ERROR: Unknown trade type "{agent_action["action_type"]}".')
        # update market state
        self.update_market(market_deltas)
        if self.verbose:
            print(f"{self.get_market_step_string()}")
        agent_action.agent.update_wallet(agent_deltas)  # update user state since market doesn't know about users
        if self.verbose:
            print(f" agent Δs ={agent_deltas}\n market Δs ={market_deltas}")
            print(f" post-trade {agent_action.agent.status_report()}") if self.verbose else None

    def update_market(self, market_deltas):
        """
        Increments member variables to reflect current market conditions
        """
        for field in market_deltas.__dataclass_fields__:
            value = getattr(market_deltas, field)
            if value:  # check that it's instantiated
                if field == "d_liquidity_pool_history":
                    assert isinstance(value, list), (
                        f"markets.update_market: Error:" + f" {field} has value={value} should be a dict"
                    )
                elif field in ["d_share_fee_history", "d_token_fee_history"]:
                    assert isinstance(value, dict), (
                        f"markets.update_market: Error:" + f" {field} has value={value} should be a dict"
                    )
                else:
                    assert np.isfinite(value), f"markets.update_market: ERROR: market delta key {field} is not finite."
        self.share_reserves += market_deltas.d_base_asset / self.share_price
        self.bond_reserves += market_deltas.d_token_asset
        self.share_buffer += market_deltas.d_share_buffer
        self.bond_buffer += market_deltas.d_bond_buffer
        self.liquidity_pool += market_deltas.d_liquidity_pool
        if market_deltas.d_liquidity_pool_history:  # not empty
            self.liquidity_pool_history.append(market_deltas.d_liquidity_pool_history)
        self.share_fees += market_deltas.d_share_fee
        if market_deltas.d_share_fee_history:  # not empty
            for key, value in market_deltas.d_share_fee_history.items():
                if key not in self.share_fee_history:
                    self.share_fee_history.update(market_deltas.d_share_fee_history)
                else:
                    self.share_fee_history[key] += value
        self.token_fees += market_deltas.d_token_fee
        if market_deltas.d_token_fee_history:  # not empty
            for key, value in market_deltas.d_token_fee_history.items():
                if key not in self.token_fee_history:
                    self.token_fee_history.update(market_deltas.d_token_fee_history)
                else:
                    self.token_fee_history[key] += value
        self.cum_base_asset_slippage += market_deltas.d_base_asset_slippage
        self.cum_token_asset_slippage += market_deltas.d_token_asset_slippage
        self.base_asset_orders += market_deltas.d_base_asset_orders
        self.token_asset_orders += market_deltas.d_token_asset_orders
        self.base_asset_volume += market_deltas.d_base_asset_volume
        self.token_asset_volume += market_deltas.d_token_asset_volume
        self.spot_price = self.pricing_model.calc_spot_price_from_reserves(
            share_reserves=self.share_reserves,
            bond_reserves=self.bond_reserves,
            init_share_price=self.init_share_price,
            share_price=self.share_price,
            time_remaining=time_utils.stretch_time(self.token_duration, self.time_stretch_constant),
        )
        self.rate = price_utils.calc_apr_from_spot_price(self.spot_price, self.token_duration)

    def get_market_state_string(self):
        """Returns a formatted string containing all of the Market class member variables"""
        strings = [f"{attribute} = {value}" for attribute, value in self.__dict__.items()]
        state_string = "\n".join(strings)
        return state_string

    def get_target_reserves(self, token_in, trade_direction):
        """
        Determine which asset is the target based on token_in and trade_direction
        """
        if trade_direction == "in":
            if token_in == "base":
                target_reserves = self.share_reserves
            elif token_in == "pt":
                target_reserves = self.bond_reserves
            else:
                raise AssertionError(
                    f'markets.get_target_reserves: ERROR: token_in should be "base" or "pt", not {token_in}!'
                )
        elif trade_direction == "out":
            if token_in == "base":
                target_reserves = self.share_reserves
            elif token_in == "pt":
                target_reserves = self.bond_reserves
            else:
                raise AssertionError(
                    f'markets.get_target_reserves: ERROR: token_in should be "base" or "pt", not {token_in}!'
                )
        else:
            raise AssertionError(
                f'markets.get_target_reserves: ERROR: trade_direction should be "in" or "out", not {trade_direction}!'
            )
        return target_reserves

    def check_fees(
        self,
        amount,
        tokens,
        reserves,
        trade_results,
    ):
        """Checks fee values for out of bounds and prints verbose outputs"""
        (token_in, token_out) = tokens
        (in_reserves, out_reserves) = reserves
        (
            without_fee_or_slippage,
            output_with_fee,
            output_without_fee,
            fee,
        ) = trade_results
        if (
            any(
                [
                    isinstance(output_with_fee, complex),
                    isinstance(output_without_fee, complex),
                    isinstance(fee, complex),
                ]
            )
            or fee < 0
        ):
            state_string = self.get_market_state_string()
            assert False, (
                f"Market.check_fees: Error: fee={fee} should not be < 0 and the type should not be complex."
                + f"\ntoken_in = {token_in}"
                + f"\ntoken_out = {token_out}"
                + f"\nin_reserves = {in_reserves}"
                + f"\nout_reserves = {out_reserves}"
                + f"\ntrade_amount = {amount}"
                + f"\nwithout_fee_or_slippage = {without_fee_or_slippage}"
                + f"\noutput_with_fee = {output_with_fee}"
                + f"\noutput_without_fee = {output_without_fee}\n"
                + state_string
            )

    def tick(self, delta_time):
        """Increments the time member variable"""
        self.time += delta_time

    def _open_short(self, trade_details):
        """
        take trade spec & turn it into trade details
        compute wallet update spec with specific details
        will be conditional on the pricing model
        """
        trade_results = self.pricing_model.calc_out_given_in(
            in_=trade_details.trade_amount,
            share_reserves=trade_details.share_reserves,
            bond_reserves=trade_details.bond_reserves,
            token_out=trade_details.token_out,
            fee_percent=trade_details.fee_percent,
            time_remaining=trade_details.stretched_time_remaining,
            init_share_price=trade_details.init_share_price,
            share_price=trade_details.share_price,
        )
        (
            without_fee_or_slippage,
            output_with_fee,
            output_without_fee,
            fee,
        ) = trade_results
        if self.verbose:
            print(f"opening short: {without_fee_or_slippage, output_with_fee, output_without_fee, fee}")
        market_deltas = MarketDeltas(
            d_base_asset=-output_with_fee,
            d_token_asset=+trade_details.trade_amount,
            d_bond_buffer=+trade_details.trade_amount,
            d_share_fee=+fee / trade_details.share_price,
            d_share_fee_history={trade_details.mint_time: fee / trade_details.share_price},
            d_base_asset_slippage=+abs(without_fee_or_slippage - output_without_fee),
            d_base_asset_orders=+1,
            d_base_asset_volume=+output_with_fee,
        )
        # TODO: _in_protocol values should be managed by pricing_model and referenced by user
        max_loss = trade_details.trade_amount - output_with_fee
        wallet_deltas = AgentWallet(
            base_in_wallet=-max_loss,
            base_in_protocol={trade_details.mint_time: +max_loss},
            token_in_protocol={trade_details.mint_time: -trade_details.trade_amount},
            fees_paid=+fee,
        )
        return market_deltas, wallet_deltas

    def _close_short(self, trade_details):
        """
        take trade spec & turn it into trade details
        compute wallet update spec with specific details
            will be conditional on the pricing model
        """
        trade_results = self.pricing_model.calc_in_given_out(
            trade_details.trade_amount,
            trade_details.share_reserves,
            trade_details.bond_reserves,
            trade_details.token_in,
            trade_details.fee_percent,
            trade_details.stretched_time_remaining,
            trade_details.init_share_price,
            trade_details.share_price,
        )
        (
            without_fee_or_slippage,
            output_with_fee,
            output_without_fee,
            fee,
        ) = trade_results
        market_deltas = MarketDeltas(
            d_base_asset=+output_with_fee,
            d_token_asset=-trade_details.trade_amount,
            d_bond_buffer=-trade_details.trade_amount,
            d_share_fee=+fee / trade_details.share_price,
            d_share_fee_history={trade_details.mint_time: fee / trade_details.share_price},
            d_base_asset_slippage=+abs(without_fee_or_slippage - output_without_fee),
            d_base_asset_orders=+1,
            d_base_asset_volume=+output_with_fee,
        )
        # TODO: Add logic:
        # If the user is not closing a full short (i.e. the mint_time balance is not zeroed out)
        # then the user does not get any money into their wallet
        # Right now the user has to close the full short
        agent_deltas = AgentWallet(
            base_in_wallet=+output_with_fee,
            base_in_protocol={trade_details.mint_time: -output_with_fee},
            token_in_protocol={trade_details.mint_time: +trade_details.trade_amount},
            fees_paid=+fee,
        )
        return market_deltas, agent_deltas

    def _open_long(self, trade_details):
        """
        take trade spec & turn it into trade details
        compute wallet update spec with specific details
            will be conditional on the pricing model
        """
        # test trade spec = {'trade_amount': 100, 'direction': 'out', 'token_in': 'base', 'mint_time': -1}
        # logic: use calcOutGivenIn because we want to buy unknown PT with known base
        #        use current mint time because this is a fresh
        trade_results = self.pricing_model.calc_out_given_in(
            trade_details.trade_amount,
            trade_details.share_reserves,
            trade_details.bond_reserves,
            trade_details.token_out,
            trade_details.fee_percent,
            trade_details.stretched_time_remaining,
            trade_details.init_share_price,
            trade_details.share_price,
        )
        (
            without_fee_or_slippage,
            output_with_fee,
            output_without_fee,
            fee,
        ) = trade_results

        market_deltas = MarketDeltas(
            d_base_asset=+trade_details.trade_amount,
            d_token_asset=-output_with_fee,
            d_share_buffer=+output_with_fee / trade_details.share_price,
            d_token_fee=+fee,
            d_token_fee_history={trade_details.mint_time: fee},
            d_token_asset_slippage=+abs(without_fee_or_slippage - output_without_fee),
            d_token_asset_orders=+1,
            d_token_asset_volume=+output_with_fee,
        )
        agent_deltas = AgentWallet(
            base_in_wallet=-trade_details.trade_amount,
            token_in_protocol={trade_details.mint_time: +output_with_fee},
            fees_paid=+fee,
        )
        return market_deltas, agent_deltas

    def _close_long(self, trade_details):
        """
        take trade spec & turn it into trade details
        compute wallet update spec with specific details
            will be conditional on the pricing model
        """
        trade_results = self.pricing_model.calc_out_given_in(
            trade_details.trade_amount,
            trade_details.share_reserves,
            trade_details.bond_reserves,
            trade_details.token_out,
            trade_details.fee_percent,
            trade_details.stretched_time_remaining,
            trade_details.init_share_price,
            trade_details.share_price,
        )
        (
            without_fee_or_slippage,
            output_with_fee,
            output_without_fee,
            fee,
        ) = trade_results
        market_deltas = MarketDeltas(
            d_base_asset=-output_with_fee,
            d_token_asset=+trade_details.trade_amount,
            d_share_buffer=-trade_details.trade_amount / trade_details.share_price,
            d_share_fee=+fee / trade_details.share_price,
            d_share_fee_history={trade_details.mint_time: fee / trade_details.share_price},
            d_base_asset_slippage=+abs(without_fee_or_slippage - output_without_fee),
            d_base_asset_orders=+1,
            d_base_asset_volume=+output_with_fee,
        )
        agent_deltas = AgentWallet(
            base_in_wallet=+output_with_fee,
            token_in_wallet={trade_details.mint_time: -trade_details.trade_amount},
            fees_paid=+fee,
        )
        return market_deltas, agent_deltas

    def _add_liquidity(self, trade_details):
        """
        Computes new deltas for bond & share reserves after liquidity is added
        """
        lp_out, d_base_reserves, d_token_reserves = self.pricing_model.calc_lp_out_given_tokens_in(
            base_asset_in=trade_details.trade_amount,
            share_reserves=trade_details.share_reserves,
            bond_reserves=trade_details.bond_reserves,
            share_buffer=trade_details.share_buffer,
            init_share_price=trade_details.init_share_price,
            share_price=trade_details.share_price,
            liquidity_pool=trade_details.liquidity_pool,
            rate=trade_details.rate,
            time_remaining=trade_details.time_remaining,
            stretched_time_remaining=trade_details.stretched_time_remaining,
        )
        market_deltas = MarketDeltas(
            d_base_asset=+d_base_reserves,
            d_token_asset=+d_token_reserves,
            d_liquidity_pool=+lp_out,
            d_liquidity_pool_history=[
                trade_details.mint_time,
                trade_details.wallet_address,
                +trade_details.trade_amount,
            ],
        )
        agent_deltas = AgentWallet(
            base_in_wallet=-d_base_reserves,
            lp_in_wallet=+lp_out,
        )
        return market_deltas, agent_deltas

    def _remove_liquidity(self, trade_details):
        """
        Computes new deltas for bond & share reserves after liquidity is removed
        """
        lp_in, d_base_reserves, d_token_reserves = self.pricing_model.calc_tokens_out_given_lp_in(
            lp_in=trade_details.trade_amount,
            share_reserves=trade_details.share_reserves,
            bond_reserves=trade_details.bond_reserves,
            share_buffer=trade_details.share_buffer,
            init_share_price=trade_details.init_share_price,
            share_price=trade_details.share_price,
            liquidity_pool=trade_details.liquidity_pool,
            rate=trade_details.rate,
            time_remaining=trade_details.time_remaining,
            stretched_time_remaining=trade_details.stretched_time_remaining,
        )

        market_deltas = MarketDeltas(
            d_base_asset=-d_base_reserves,
            d_token_asset=-d_token_reserves,
            d_liquidity_pool=-lp_in,
            d_liquidity_pool_history=[
                trade_details.mint_time,
                trade_details.wallet_address,
                -trade_details.trade_amount,
            ],
        )
        agent_deltas = AgentWallet(
            base_in_wallet=+d_base_reserves,
            lp_in_wallet=-lp_in,
        )
        return market_deltas, agent_deltas

    def calc_fees_owed(self, return_agent=None):
        """
        Returns the fees owed to the agent
        """
        start_time = time.time()
        cum_liq, prev_time, prev_share_fees, prev_token_fees = 0, 0, 0, 0
        cum_liq_by_agent, contribution, token_owed, share_owed = {}, {}, {}, {}
        for [current_time, acting_agent, new_liq] in self.liquidity_pool_history:
            # calculate what happened since the last update, we use marginal values for everything
            share_fees_till_now = sum([v for k, v in self.share_fee_history.items() if k <= current_time])
            token_fees_till_now = sum([v for k, v in self.token_fee_history.items() if k <= current_time])
            delta_share_fees = share_fees_till_now - prev_share_fees
            delta_token_fees = token_fees_till_now - prev_token_fees
            delta_time = current_time - prev_time
            # initialize agent if this is the first time we see them
            if acting_agent not in cum_liq_by_agent:
                (
                    contribution[acting_agent],
                    token_owed[acting_agent],
                    share_owed[acting_agent],
                    cum_liq_by_agent[acting_agent],
                ) = (0, 0, 0, 0)
            if current_time != 0:  # only do a marginal update after first timestep where deltas are zero
                for update_agent in cum_liq_by_agent:  # for each agent
                    # update their marginal share of cumulative liquidity, give them credit for it (contribution)
                    contribution[update_agent] += cum_liq_by_agent[update_agent] / cum_liq
                    # update their owed fees
                    share_owed[update_agent] = (
                        share_owed[update_agent] * prev_time
                        + contribution[update_agent] * delta_share_fees * delta_time
                    ) / current_time
                    token_owed[update_agent] = (
                        token_owed[update_agent] * prev_time
                        + contribution[update_agent] * delta_token_fees * delta_time
                    ) / current_time
            # update values used for next iteration
            cum_liq += new_liq
            cum_liq_by_agent[acting_agent] += new_liq
            prev_time = current_time
            prev_share_fees, prev_token_fees = share_fees_till_now, token_fees_till_now
        if self.verbose:
            print(f"cum_liq_by_agent = {cum_liq_by_agent}")
            print(
                f"      share_owed = {share_owed} calculated sum = {sum(share_owed.values())}"
                + f"\n                                           vs. direct = {self.share_fees} it's a "
                + f"match "
                if sum(share_owed.values()) == self.share_fees
                else f"mismatch "
            )
            print(
                f"      token_owed = {token_owed} calculated sum = {sum(token_owed.values())}"
                + f"\n                                           vs. direct = {self.token_fees} it's a "
                + f"match "
                if sum(token_owed.values()) == self.token_fees
                else f"mismatch "
            )
        dur = time.time() - start_time
        # TODO: remove this once we're happy with the performance
        if self.verbose:
            print(
                f"calc_fees took ",
                end=f"{float_to_string(dur,precision=2)} seconds"
                if dur > 1
                else f"{float_to_string(dur*1000,precision=2)} milliseconds\n",
            )
        if return_agent is not None:
            return share_owed[return_agent], token_owed[return_agent]

    def get_market_step_string(self):
        """Returns a string that describes the current market step"""
        output_string = f"t={bcolors.HEADER}{self.time}{bcolors.ENDC}"
        output_string += (
            f" reserves=["
            + f"x:{bcolors.OKBLUE}{self.share_reserves*self.share_price}{bcolors.ENDC}"
            + f",y:{bcolors.OKBLUE}{self.bond_reserves}{bcolors.ENDC}"
            + f",z:{bcolors.OKBLUE}{self.share_reserves}{bcolors.ENDC}"
            + f",z_b:{bcolors.OKBLUE}{self.share_buffer}{bcolors.ENDC}"
            + f",y_b:{bcolors.OKBLUE}{self.bond_buffer}{bcolors.ENDC}"
            + f"]"
        )
        output_string += f"\n liquidity_pool_history={self.liquidity_pool_history}"
        output_string += f"\n share_fee_history={self.share_fee_history}"
        output_string += f"\n token_fee_history={self.token_fee_history}"
        if self.verbose:
            output_string += (
                f" fees=["
                + f"x:{bcolors.OKBLUE}{self.share_fees}{bcolors.ENDC}"
                + f",y:{bcolors.OKBLUE}{self.token_fees}{bcolors.ENDC}"
            )
        output_string += f" p={bcolors.FAIL}{self.spot_price}{bcolors.ENDC}"
        output_string += f" rate={bcolors.FAIL}{self.rate}{bcolors.ENDC}"
        return output_string
