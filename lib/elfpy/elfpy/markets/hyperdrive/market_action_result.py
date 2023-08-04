"""The resulting deltas of a market action"""
# Please enter the commit message for your changes. Lines starting
from __future__ import annotations

from dataclasses import dataclass

from fixedpointmath import FixedPoint

from lib.elfpy.elfpy import types
from lib.elfpy.elfpy.markets.base import BaseMarketActionResult


@types.freezable(frozen=True, no_new_attribs=True)
@dataclass
class MarketActionResult(BaseMarketActionResult):
    r"""The result to a market of performing a trade"""
    d_base: FixedPoint
    d_bonds: FixedPoint
