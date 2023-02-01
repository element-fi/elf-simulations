"""Helper functions for delivering simulation outputs"""
from __future__ import annotations  # types will be strings by default in 3.11
from typing import TYPE_CHECKING
import os
import sys
import json
import logging
from logging.handlers import RotatingFileHandler

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

import elfpy

if TYPE_CHECKING:
    from typing import Optional, Any
    import pandas as pd
    from matplotlib.figure import Figure
    from matplotlib.gridspec import GridSpec
    from matplotlib.pyplot import Axes


## Plotting
def plot_market_lp_reserves(state_df: pd.DataFrame) -> Figure:
    r"""Plot the simulator market LP reserves per day

    Parameters
    ----------
    simulator : Simulator
        An instantiated simulator that has run trades with agents

    Returns
    -------
    Figure
    """
    fig, axes, _ = get_gridspec_subplots()
    axis = state_df.plot(x="day", y="lp_reserves", ax=axes[0])
    axis.get_legend().remove()
    axis.set_title("Market liquidity provider reserves")
    axis.set_ylabel("LP reserves")
    axis.set_xlabel("Day")
    return fig


def plot_market_spot_price(state_df: pd.DataFrame) -> Figure:
    r"""Plot the simulator market APR per day

    Parameters
    ----------
    state_df : DataFrame
        Pandas dataframe containing the simulation_state keys as columns, as well as some computed columns

    Returns
    -------
    Figure
    """
    fig, axes, _ = get_gridspec_subplots()
    axis = state_df.plot(x="day", y="spot_price", ax=axes[0])
    axis.get_legend().remove()
    axis.set_title("Market spot price")
    axis.set_ylabel("Spot price of principle tokens")
    axis.set_xlabel("Day")
    return fig


def plot_pool_apr(state_df: pd.DataFrame) -> Figure:
    r"""Plot the simulator market APR per day

    Parameters
    ----------
    state_df : DataFrame
        Pandas dataframe containing the simulation_state keys as columns, as well as some computed columns

    Returns
    -------
    Figure
    """
    fig, axes, _ = get_gridspec_subplots()
    axis = state_df.plot(x="day", y="pool_apr_percent", ax=axes[0])
    axis.get_legend().remove()
    axis.set_title("Market pool APR")
    axis.set_ylabel("APR (%)")
    axis.set_xlabel("Day")
    return fig


def plot_longs_and_shorts(state_df: pd.DataFrame, exclude_first_agent: bool = True, xtick_step: int = 10) -> Figure:
    r"""Plot the total market longs & shorts over time

    Parameters
    ----------
    state_df : DataFrame
        Pandas dataframe containing the simulation_state keys as columns, as well as some computed columns
    exclude_first_agent : bool
        If true, exclude the first agent in simulator.agents (this is usually the init_lp agent)

    Returns
    -------
    Figure
    """
    fig, axes, _ = get_gridspec_subplots(nrows=1, ncols=2, wspace=0.5)
    addresses = []
    for column in state_df.columns:
        splits = column.split("_")
        if splits[0] == "agent":
            addresses.append(int(splits[1]))
    agents = set(addresses)
    for address in agents:
        if (exclude_first_agent and address > 0) or (not exclude_first_agent):
            dict_key = f"agent_{address}"
            _ = state_df.plot(x="run_trade_number", y=f"{dict_key}_total_longs", label=f"0x{address}", ax=axes[0])
            _ = state_df.plot(x="run_trade_number", y=f"{dict_key}_total_shorts", label=f"0x{address}", ax=axes[1])
    axes[0].set_ylabel("Total longs")
    axes[1].set_ylabel("Total shorts")
    axes[0].legend()
    trade_labels = state_df.loc[:, "run_trade_number"][::xtick_step]
    for axis in axes:
        axis.set_xlabel("Trade number")
        axis.set_xticks(trade_labels)
        axis.set_xticklabels([str(x + 1) for x in trade_labels])
        axis.set_box_aspect(1)
    fig_size = fig.get_size_inches()  # [width (or cols), height (or rows)]
    fig.set_size_inches([2 * fig_size[0], fig_size[1]])
    _ = fig.suptitle("Longs and shorts per agent", y=0.90)
    return fig


def plot_wallet_reserves(state_df: pd.DataFrame, exclude_first_agent: bool = True, xtick_step: int = 10) -> Figure:
    r"""Plot the wallet base asset and LP token quantities over time

    Parameters
    ----------
    state_df : DataFrame
        Pandas dataframe containing the simulation_state keys as columns, as well as some computed columns
    exclude_first_agent : bool
        If true, exclude the first agent in simulator.agents (this is usually the init_lp agent)

    Returns
    -------
    Figure
    """
    fig, axes, _ = get_gridspec_subplots(nrows=1, ncols=2, wspace=0.5)
    addresses = []
    for column in state_df.columns:
        splits = column.split("_")
        if splits[0] == "agent":
            addresses.append(int(splits[1]))
    agents = set(addresses)
    for address in agents:
        if (exclude_first_agent and address > 0) or (not exclude_first_agent):
            dict_key = f"agent_{address}"
            _ = state_df.plot(x="run_trade_number", y=f"{dict_key}_base", label=f"0x{address}", ax=axes[0])
            _ = state_df.plot(x="run_trade_number", y=f"{dict_key}_lp_tokens", label=f"0x{address}", ax=axes[1])
    axes[0].set_ylabel("Base asset in wallet")
    axes[1].set_ylabel("LP tokens in wallet")
    axes[0].legend()
    trade_labels = state_df.loc[:, "run_trade_number"][::xtick_step]
    for axis in axes:
        axis.set_xlabel("Trade number")
        axis.set_xticks(trade_labels)
        axis.set_xticklabels([str(x + 1) for x in trade_labels])
        axis.set_box_aspect(1)
    fig_size = fig.get_size_inches()  # [width (or cols), height (or rows)]
    fig.set_size_inches([2 * fig_size[0], fig_size[1]])
    _ = fig.suptitle("Agent wallet reserves", y=0.90)
    return fig


def get_gridspec_subplots(nrows: int = 1, ncols: int = 1, **kwargs: Any) -> tuple[Figure, Axes, GridSpec]:
    r"""Setup a figure with axes that have reasonable spacing

    Parameters
    ----------
    nrows : int
       number of rows in the figure
    ncols : int
       number of columns in the figure
    kwargs : Any
        optional keyword arguments to be supplied to matplotlib.gridspec.GridSpec()

    Returns
    -------
    tuple[Figure, Axes, GridSpec]
        a tuple containing the relevant figure objects
    """
    if "wspace" not in kwargs:
        kwargs["wspace"] = 1.0
    grid_spec = gridspec.GridSpec(nrows, ncols, **kwargs)
    fig = plt.figure()
    axes = [fig.add_subplot(grid_spec[plot_id]) for plot_id in np.ndindex((nrows, ncols))]
    return fig, axes, grid_spec


def clear_axis(axis: Axes, spines: str = "none") -> Axes:
    r"""Clear spines & tick labels from proplot axis object

    Parameters
    ----------
        axis : matplotlib axis object
           axis to be cleared
        spines : str
           any matplotlib color, defaults to "none" which makes the spines invisible

    Returns
    -------
        axis : matplotlib axis object
    """
    for ax_loc in ["top", "bottom", "left", "right"]:
        axis.spines[ax_loc].set_color(spines)
    axis.set_yticklabels([])
    axis.set_xticklabels([])
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)
    axis.tick_params(axis="both", bottom=False, top=False, left=False, right=False)
    return axis


def clear_axes(axes: list[Axes], spines: str = "none") -> list:
    r"""Calls clear_axis iteratively for each axis in axes

    Parameters
    ----------
        axes : list of matplotlib axis objects
           axes to be cleared
        spines : str
           any matplotlib color, defaults to "none" which makes the spines invisible

    Returns
    -------
        axes : list of matplotlib axis objects
    """
    for axis in axes:
        clear_axis(axis, spines)
    return axes


def format_axis(
    axis_handle, xlabel="", fontsize=18, linestyle="--", linewidth="1", color="grey", which="both", axis="y"
):
    r"""Formats the axis"""
    # pylint: disable=too-many-arguments
    axis_handle.set_xlabel(xlabel)
    axis_handle.tick_params(axis="both", labelsize=fontsize)
    axis_handle.grid(visible=True, linestyle=linestyle, linewidth=linewidth, color=color, which=which, axis=axis)
    if xlabel == "":
        axis_handle.xaxis.set_ticklabels([])
    axis_handle.legend(fontsize=fontsize)


def annotate(axis_handle, text, major_offset, minor_offset, val):
    r"""Adds legend-like labels"""
    annotation_handle = axis_handle.annotate(
        text,
        xy=(
            val["position_x"],
            val["position_y"] - val["major_offset"] * major_offset - val["minor_offset"] * minor_offset,
        ),
        xytext=(
            val["position_x"],
            val["position_y"] - val["major_offset"] * major_offset - val["minor_offset"] * minor_offset,
        ),
        xycoords="subfigure fraction",
        fontsize=val["font_size"],
        alpha=val["alpha"],
    )
    annotation_handle.set_bbox(
        {"facecolor": "white", "edgecolor": "black", "alpha": val["alpha"], "linewidth": 0, "boxstyle": "round,pad=0.1"}
    )


## Logging
def delete_log_file() -> None:
    r"""If the logger's handler if a file handler, delete the underlying file."""
    handler = logging.getLogger().handlers[0]
    if isinstance(handler, logging.FileHandler):
        os.remove(handler.baseFilename)
    logging.getLogger().removeHandler(handler)


def setup_logging(
    log_filename: Optional[str] = None,
    max_bytes: int = elfpy.DEFAULT_LOG_MAXBYTES,
    log_level: int = elfpy.DEFAULT_LOG_LEVEL,
) -> None:
    r"""Setup logging and handlers with default settings"""
    if log_filename is None:
        handler = logging.StreamHandler(sys.stdout)
    else:
        log_dir, log_name = os.path.split(log_filename)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        handler = RotatingFileHandler(os.path.join(log_dir, log_name), mode="w", maxBytes=max_bytes)
    logging.getLogger().setLevel(log_level)  # events of this level and above will be tracked
    handler.setFormatter(logging.Formatter(elfpy.DEFAULT_LOG_FORMATTER, elfpy.DEFAULT_LOG_DATETIME))
    logging.getLogger().handlers = [handler]  # overwrite handlers with the desired one


def close_logging(delete_logs=True):
    r"""Close logging and handlers for the test"""
    logging.shutdown()
    if delete_logs:
        for handler in logging.getLogger().handlers:
            if hasattr(handler, "baseFilename") and not isinstance(handler, logging.StreamHandler):
                # access baseFilename in a type safe way
                handler_file_name = getattr(handler, "baseFilename")
                if os.path.exists(handler_file_name):
                    os.remove(handler_file_name)
            handler.close()


class CustomEncoder(json.JSONEncoder):
    r"""Custom encoder for JSON string dumps"""

    def default(self, o):
        r"""Override default behavior"""
        match o:
            case np.integer():
                return int(o)
            case np.floating():
                return float(o)
            case np.ndarray():
                return o.tolist()
            case _:
                try:
                    return o.__dict__
                except AttributeError:
                    return repr(o)
