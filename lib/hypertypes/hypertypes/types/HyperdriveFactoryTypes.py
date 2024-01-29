"""Dataclasses for all structs in the HyperdriveFactory contract.

DO NOT EDIT.  This file was generated by pypechain.  See documentation at
https://github.com/delvtech/pypechain """

# super() call methods are generic, while our version adds values & types
# pylint: disable=arguments-differ
# contracts have PascalCase names
# pylint: disable=invalid-name
# contracts control how many attributes and arguments we have in generated code
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# unable to determine which imports will be used in the generated code
# pylint: disable=unused-import
# we don't need else statement if the other conditionals all have return,
# but it's easier to generate
# pylint: disable=no-else-return
from __future__ import annotations

from dataclasses import dataclass

from web3.types import ABIEvent, ABIEventParams

from . import IHyperdriveTypes as IHyperdrive


@dataclass
class FactoryConfig:
    """FactoryConfig struct."""

    governance: str
    hyperdriveGovernance: str
    defaultPausers: list[str]
    feeCollector: str
    checkpointDurationResolution: int
    minCheckpointDuration: int
    maxCheckpointDuration: int
    minPositionDuration: int
    maxPositionDuration: int
    minFixedAPR: int
    maxFixedAPR: int
    minTimeStretchAPR: int
    maxTimeStretchAPR: int
    minFees: IHyperdrive.Fees
    maxFees: IHyperdrive.Fees
    linkerFactory: str
    linkerCodeHash: bytes


CheckpointDurationResolutionUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newCheckpointDurationResolution", type="uint256"),
    ],
    name="CheckpointDurationResolutionUpdated",
    type="event",
)

DefaultPausersUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newDefaultPausers", type="address[]"),
    ],
    name="DefaultPausersUpdated",
    type="event",
)

Deployed = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="deployerCoordinator", type="address"),
        ABIEventParams(indexed=False, name="hyperdrive", type="address"),
        ABIEventParams(indexed=False, name="config", type="tuple"),
        ABIEventParams(indexed=False, name="extraData", type="bytes"),
    ],
    name="Deployed",
    type="event",
)

DeployerCoordinatorAdded = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="deployerCoordinator", type="address"),
    ],
    name="DeployerCoordinatorAdded",
    type="event",
)

DeployerCoordinatorRemoved = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="deployerCoordinator", type="address"),
    ],
    name="DeployerCoordinatorRemoved",
    type="event",
)

FeeCollectorUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="newFeeCollector", type="address"),
    ],
    name="FeeCollectorUpdated",
    type="event",
)

GovernanceUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="governance", type="address"),
    ],
    name="GovernanceUpdated",
    type="event",
)

HyperdriveGovernanceUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="hyperdriveGovernance", type="address"),
    ],
    name="HyperdriveGovernanceUpdated",
    type="event",
)

ImplementationUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="newDeployer", type="address"),
    ],
    name="ImplementationUpdated",
    type="event",
)

LinkerCodeHashUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="newLinkerCodeHash", type="bytes32"),
    ],
    name="LinkerCodeHashUpdated",
    type="event",
)

LinkerFactoryUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="newLinkerFactory", type="address"),
    ],
    name="LinkerFactoryUpdated",
    type="event",
)

MaxCheckpointDurationUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMaxCheckpointDuration", type="uint256"),
    ],
    name="MaxCheckpointDurationUpdated",
    type="event",
)

MaxFeesUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMaxFees", type="tuple"),
    ],
    name="MaxFeesUpdated",
    type="event",
)

MaxFixedAPRUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMaxFixedAPR", type="uint256"),
    ],
    name="MaxFixedAPRUpdated",
    type="event",
)

MaxPositionDurationUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMaxPositionDuration", type="uint256"),
    ],
    name="MaxPositionDurationUpdated",
    type="event",
)

MaxTimeStretchAPRUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMaxTimeStretchAPR", type="uint256"),
    ],
    name="MaxTimeStretchAPRUpdated",
    type="event",
)

MinCheckpointDurationUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMinCheckpointDuration", type="uint256"),
    ],
    name="MinCheckpointDurationUpdated",
    type="event",
)

MinFeesUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMinFees", type="tuple"),
    ],
    name="MinFeesUpdated",
    type="event",
)

MinFixedAPRUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMinFixedAPR", type="uint256"),
    ],
    name="MinFixedAPRUpdated",
    type="event",
)

MinPositionDurationUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMinPositionDuration", type="uint256"),
    ],
    name="MinPositionDurationUpdated",
    type="event",
)

MinTimeStretchAPRUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=False, name="newMinTimeStretchAPR", type="uint256"),
    ],
    name="MinTimeStretchAPRUpdated",
    type="event",
)
