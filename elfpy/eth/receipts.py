"""Utilities for handling transaction receipts"""
from __future__ import annotations

from typing import Any, Sequence

from hexbytes import HexBytes
from web3 import Web3
from web3.contract.contract import Contract, ContractEvent
from web3.types import ABIEvent, EventData, LogReceipt, TxReceipt


def get_transaction_logs(
    web3: Web3, contract: Contract, tx_receipt: TxReceipt, event_names: Sequence[str] | None = None
) -> dict[str, Any]:
    """Decode a transaction receipt.

    Arguments
    ---------
    web3 : Web3
        web3 provider object
    contract : Contract
        The contract that emitted the receipt
    tx_receipt : TxReceipt
        The emitted receipt after a transaction was completed
    event_names : Sequence[str] | None
        If not None, then only return logs with matching event names


    Returns
    -------

    """
    logs: list[dict[Any, Any]] = []
    if tx_receipt.get("logs"):
        for log in tx_receipt["logs"]:
            event_data, event = get_event_object(web3, contract, log, tx_receipt)
            if event_data and event:
                formatted_log = dict(event_data)
                formatted_log["event"] = event.get("name")
                if (event_names is not None and formatted_log["event"] in event_names) or (event_names is None):
                    formatted_log["args"] = dict(event_data["args"])
                    logs.append(formatted_log)
    return logs


def get_event_object(
    web3: Web3, contract: Contract, log: LogReceipt, tx_receipt: TxReceipt
) -> tuple[EventData, ABIEvent] | tuple[None, None]:
    """Retrieve the event object and anonymous types for a given contract and log.

    Arguments
    ---------
    web3 : Web3
        web3 provider object
    contract : Contract
        The contract that emitted the receipt
    log : LogReceipt
        A TypedDict parsed out of the transaction receipt
    tx_receipt: TxReceipt
        The emitted receipt after a transaction was completed

    Returns
    -------
    tuple[EventData, ABIEvent] | tuple[None, None]
        If faile, return (None, None). Otherwise, return the decoded event information as (data, abi).
    """
    abi_events = [abi for abi in contract.abi if abi["type"] == "event"]  # type: ignore
    for event in abi_events:  # type: ignore
        # Get event signature components
        name = event["name"]  # type: ignore
        inputs = [param["type"] for param in event["inputs"]]  # type: ignore
        inputs = ",".join(inputs)
        # Hash event signature
        event_signature_text = f"{name}({inputs})"
        event_signature_hex = web3.keccak(text=event_signature_text).hex()
        # Find match between log's event signature and ABI's event signature
        receipt_event_signature_hex = log["topics"][0].hex()
        if event_signature_hex == receipt_event_signature_hex:
            # Decode matching log
            contract_event: ContractEvent = contract.events[event["name"]]()  # type: ignore
            event_data: EventData = contract_event.process_receipt(tx_receipt)[0]
            return event_data, event  # type: ignore
    return (None, None)
