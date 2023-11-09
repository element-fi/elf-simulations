"""Extend the dfault JSON encoder to include additional types."""

import json
from datetime import datetime
from enum import Enum
from traceback import format_tb
from types import TracebackType

import numpy as np
from fixedpointmath import FixedPoint
from hexbytes import HexBytes
from numpy.random._generator import Generator as NumpyGenerator
from web3.datastructures import AttributeDict, MutableAttributeDict


class ExtendedJSONEncoder(json.JSONEncoder):
    r"""Custom encoder for JSON string dumps."""

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    def default(self, o):
        r"""Override default behavior"""
        if isinstance(o, set):
            return list(o)
        if isinstance(o, HexBytes):
            return o.hex()
        if isinstance(o, (AttributeDict, MutableAttributeDict)):
            return dict(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, FixedPoint):
            return str(o)
        if isinstance(o, NumpyGenerator):
            return "NumpyGenerator"
        if isinstance(o, datetime):
            return str(o)
        if isinstance(o, TracebackType):
            return format_tb(o)
        if isinstance(o, BaseException):
            return repr(o)
        if isinstance(o, Enum):
            return o.name
        if isinstance(o, bytes):
            return str(o)
        try:
            return o.__dict__
        except AttributeError:
            pass
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)
