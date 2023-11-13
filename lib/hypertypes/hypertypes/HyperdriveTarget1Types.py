"""Dataclasses for all structs in the HyperdriveTarget1 contract."""
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

from web3.types import ABIEvent

from web3.types import ABIEventParams


@dataclass
class Options:
    """Options struct."""

    destination: str
    asBase: bool
    extraData: bytes


AddLiquidity = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="provider", type="address"),
        ABIEventParams(indexed=False, name="lpAmount", type="uint256"),
        ABIEventParams(indexed=False, name="baseAmount", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
        ABIEventParams(indexed=False, name="lpSharePrice", type="uint256"),
    ],
    name="AddLiquidity",
    type="event",
)

Approval = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="owner", type="address"),
        ABIEventParams(indexed=True, name="spender", type="address"),
        ABIEventParams(indexed=False, name="value", type="uint256"),
    ],
    name="Approval",
    type="event",
)

ApprovalForAll = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="account", type="address"),
        ABIEventParams(indexed=True, name="operator", type="address"),
        ABIEventParams(indexed=False, name="approved", type="bool"),
    ],
    name="ApprovalForAll",
    type="event",
)

CloseLong = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="trader", type="address"),
        ABIEventParams(indexed=True, name="assetId", type="uint256"),
        ABIEventParams(indexed=False, name="maturityTime", type="uint256"),
        ABIEventParams(indexed=False, name="baseAmount", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
        ABIEventParams(indexed=False, name="bondAmount", type="uint256"),
    ],
    name="CloseLong",
    type="event",
)

CloseShort = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="trader", type="address"),
        ABIEventParams(indexed=True, name="assetId", type="uint256"),
        ABIEventParams(indexed=False, name="maturityTime", type="uint256"),
        ABIEventParams(indexed=False, name="baseAmount", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
        ABIEventParams(indexed=False, name="bondAmount", type="uint256"),
    ],
    name="CloseShort",
    type="event",
)

CollectGovernanceFee = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="collector", type="address"),
        ABIEventParams(indexed=False, name="fees", type="uint256"),
    ],
    name="CollectGovernanceFee",
    type="event",
)

CreateCheckpoint = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="checkpointTime", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
        ABIEventParams(indexed=False, name="maturedShorts", type="uint256"),
        ABIEventParams(indexed=False, name="maturedLongs", type="uint256"),
        ABIEventParams(indexed=False, name="lpSharePrice", type="uint256"),
    ],
    name="CreateCheckpoint",
    type="event",
)

GovernanceUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="newGovernance", type="address"),
    ],
    name="GovernanceUpdated",
    type="event",
)

Initialize = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="provider", type="address"),
        ABIEventParams(indexed=False, name="lpAmount", type="uint256"),
        ABIEventParams(indexed=False, name="baseAmount", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
        ABIEventParams(indexed=False, name="apr", type="uint256"),
    ],
    name="Initialize",
    type="event",
)

OpenLong = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="trader", type="address"),
        ABIEventParams(indexed=True, name="assetId", type="uint256"),
        ABIEventParams(indexed=False, name="maturityTime", type="uint256"),
        ABIEventParams(indexed=False, name="baseAmount", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
        ABIEventParams(indexed=False, name="bondAmount", type="uint256"),
    ],
    name="OpenLong",
    type="event",
)

OpenShort = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="trader", type="address"),
        ABIEventParams(indexed=True, name="assetId", type="uint256"),
        ABIEventParams(indexed=False, name="maturityTime", type="uint256"),
        ABIEventParams(indexed=False, name="baseAmount", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
        ABIEventParams(indexed=False, name="bondAmount", type="uint256"),
    ],
    name="OpenShort",
    type="event",
)

PauserUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="newPauser", type="address"),
    ],
    name="PauserUpdated",
    type="event",
)

RedeemWithdrawalShares = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="provider", type="address"),
        ABIEventParams(indexed=False, name="withdrawalShareAmount", type="uint256"),
        ABIEventParams(indexed=False, name="baseAmount", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
    ],
    name="RedeemWithdrawalShares",
    type="event",
)

RemoveLiquidity = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="provider", type="address"),
        ABIEventParams(indexed=False, name="lpAmount", type="uint256"),
        ABIEventParams(indexed=False, name="baseAmount", type="uint256"),
        ABIEventParams(indexed=False, name="sharePrice", type="uint256"),
        ABIEventParams(indexed=False, name="withdrawalShareAmount", type="uint256"),
        ABIEventParams(indexed=False, name="lpSharePrice", type="uint256"),
    ],
    name="RemoveLiquidity",
    type="event",
)

TransferSingle = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="operator", type="address"),
        ABIEventParams(indexed=True, name="from", type="address"),
        ABIEventParams(indexed=True, name="to", type="address"),
        ABIEventParams(indexed=False, name="id", type="uint256"),
        ABIEventParams(indexed=False, name="value", type="uint256"),
    ],
    name="TransferSingle",
    type="event",
)
