"""Example script showing example dashboard hyperdrive."""

# pylint: disable=pointless-statement
import time

from fixedpointmath import FixedPoint

from agent0 import LocalChain, LocalHyperdrive, PolicyZoo

# Initialization
local_chain_config = LocalChain.Config()
chain = LocalChain(local_chain_config)

initial_pool_config = LocalHyperdrive.Config()
hyperdrive0 = LocalHyperdrive(chain, initial_pool_config)

agent0 = hyperdrive0.init_agent(
    base=FixedPoint(100000),
    eth=FixedPoint(100),
    name="random_bot",
    # The underlying policy to attach to this agent
    policy=PolicyZoo.random,
    # The configuration for the underlying policy
    policy_config=PolicyZoo.random.Config(rng_seed=123),
)

initial_pool_config = LocalHyperdrive.Config()
hyperdrive1 = LocalHyperdrive(chain, initial_pool_config)

agent1 = hyperdrive1.init_agent(
    base=FixedPoint(100000),
    eth=FixedPoint(100),
    name="random_bot",
    # The underlying policy to attach to this agent
    policy=PolicyZoo.random,
    # The configuration for the underlying policy
    policy_config=PolicyZoo.random.Config(rng_seed=345),
)

# Run the dashboard in a subprocess.
# This command should automatically open a web browser that connects.
chain.run_dashboard(blocking=False)

# Make trades slowly
for _ in range(100):
    agent0.execute_policy_action()
    agent1.execute_policy_action()
    time.sleep(1)

# Clean up resources
chain.cleanup()
