"""Test transaction behavior."""

import pytest
from fixedpointmath import FixedPoint

from agent0.core.hyperdrive.interactive import ILocalChain, ILocalHyperdrive
from agent0.core.hyperdrive.policies import PolicyZoo
from agent0.ethpy.base.transactions import build_transaction


@pytest.mark.anvil
def test_gas_price_base_multiple_explicit(chain: ILocalChain):
    """Set the gas price base multiple explicitly."""
    # set up config, hyperdrive, interface, web3, and agent
    base_fee_multiple = 100
    config = ILocalHyperdrive.Config()
    hyperdrive = ILocalHyperdrive(chain, config)
    interface = hyperdrive.interface
    web3 = interface.web3
    agent = hyperdrive.init_agent(eth=FixedPoint(1))

    fn_args_mint = (
        agent.checksum_address,  # destination
        FixedPoint(11111).scaled_value,  # amount
    )
    regular_built_transaction = build_transaction(
        func_handle=interface.base_token_contract.functions.mint(*fn_args_mint),
        signer=agent.agent,
        web3=web3,
    )
    assert "maxPriorityFeePerGas" in regular_built_transaction
    assert isinstance(regular_built_transaction["maxPriorityFeePerGas"], int)
    regular_priority_fee_per_gas = regular_built_transaction["maxPriorityFeePerGas"]
    assert "maxFeePerGas" in regular_built_transaction
    assert isinstance(regular_built_transaction["maxFeePerGas"], int)
    regular_base_fee_per_gas = regular_built_transaction["maxFeePerGas"] - regular_priority_fee_per_gas

    multiplied_built_transaction = build_transaction(
        func_handle=interface.base_token_contract.functions.mint(*fn_args_mint),
        signer=agent.agent,
        web3=web3,
        txn_options_base_fee_multiple=base_fee_multiple,
    )
    assert "maxPriorityFeePerGas" in multiplied_built_transaction
    assert isinstance(multiplied_built_transaction["maxPriorityFeePerGas"], int)
    multiplied_priority_fee_per_gas = multiplied_built_transaction["maxPriorityFeePerGas"]
    assert "maxFeePerGas" in multiplied_built_transaction
    assert isinstance(multiplied_built_transaction["maxFeePerGas"], int)
    multiplied_base_fee_per_gas = multiplied_built_transaction["maxFeePerGas"] - multiplied_priority_fee_per_gas

    assert multiplied_base_fee_per_gas / regular_base_fee_per_gas == base_fee_multiple


@pytest.mark.anvil
def test_gas_price_priority_multiple_explicit(chain: ILocalChain):
    """Set the gas price priority multiple explicitly."""
    # set up config, hyperdrive, interface, web3, and agent
    priority_fee_multiple = 100
    config = ILocalHyperdrive.Config()
    hyperdrive = ILocalHyperdrive(chain, config)
    interface = hyperdrive.interface
    web3 = interface.web3
    agent = hyperdrive.init_agent(eth=FixedPoint(1))

    fn_args_mint = (
        agent.checksum_address,  # destination
        FixedPoint(11111).scaled_value,  # amount
    )
    regular_built_transaction = build_transaction(
        func_handle=interface.base_token_contract.functions.mint(*fn_args_mint),
        signer=agent.agent,
        web3=web3,
    )
    assert "maxPriorityFeePerGas" in regular_built_transaction
    assert isinstance(regular_built_transaction["maxPriorityFeePerGas"], int)
    regular_priority_fee_per_gas = regular_built_transaction["maxPriorityFeePerGas"]

    multiplied_built_transaction = build_transaction(
        func_handle=interface.base_token_contract.functions.mint(*fn_args_mint),
        signer=agent.agent,
        web3=web3,
        txn_options_priority_fee_multiple=priority_fee_multiple,
    )
    assert "maxPriorityFeePerGas" in multiplied_built_transaction
    assert isinstance(multiplied_built_transaction["maxPriorityFeePerGas"], int)
    multiplied_priority_fee_per_gas = multiplied_built_transaction["maxPriorityFeePerGas"]

    assert multiplied_priority_fee_per_gas / regular_priority_fee_per_gas == priority_fee_multiple


@pytest.mark.anvil
def test_gas_price_base_multiple_policy(chain: ILocalChain):
    """Set the gas price base multiple through an agent policy."""
    # set up config, hyperdrive, interface, web3, and agent
    base_fee_multiple = 100
    config = ILocalHyperdrive.Config()
    hyperdrive = ILocalHyperdrive(chain, config)
    interface = hyperdrive.interface

    regular_agent = hyperdrive.init_agent(
        base=FixedPoint(11111), policy=PolicyZoo.random, policy_config=PolicyZoo.random.Config()
    )
    multiplied_agent = hyperdrive.init_agent(
        base=FixedPoint(11111),
        policy=PolicyZoo.random,
        policy_config=PolicyZoo.random.Config(base_fee_multiple=base_fee_multiple),
    )

    actions, _ = regular_agent.agent.policy.action(interface, regular_agent.agent.wallet)
    regular_base_fee_multiple = actions[0].market_action.base_fee_multiple
    assert regular_base_fee_multiple is None

    actions, _ = multiplied_agent.agent.policy.action(interface, multiplied_agent.agent.wallet)
    multiplied_base_fee_multiple = actions[0].market_action.base_fee_multiple
    assert multiplied_base_fee_multiple == base_fee_multiple


@pytest.mark.anvil
def test_gas_price_priority_multiple_policy(chain: ILocalChain):
    """Set the gas price priority multiple through an agent policy."""
    # set up config, hyperdrive, interface, web3, and agent
    priority_fee_multiple = 100
    config = ILocalHyperdrive.Config()
    hyperdrive = ILocalHyperdrive(chain, config)
    interface = hyperdrive.interface

    regular_agent = hyperdrive.init_agent(
        base=FixedPoint(11111), policy=PolicyZoo.random, policy_config=PolicyZoo.random.Config()
    )
    multiplied_agent = hyperdrive.init_agent(
        base=FixedPoint(11111),
        policy=PolicyZoo.random,
        policy_config=PolicyZoo.random.Config(priority_fee_multiple=priority_fee_multiple),
    )

    actions, _ = regular_agent.agent.policy.action(interface, regular_agent.agent.wallet)
    regular_priority_fee_multiple = actions[0].market_action.priority_fee_multiple
    assert regular_priority_fee_multiple is None

    actions, _ = multiplied_agent.agent.policy.action(interface, multiplied_agent.agent.wallet)
    multiplied_priority_fee_multiple = actions[0].market_action.priority_fee_multiple
    assert multiplied_priority_fee_multiple == priority_fee_multiple
