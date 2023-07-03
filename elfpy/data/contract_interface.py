"""Functions and classes for interfacing with smart contracts"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from datetime import datetime
from typing import Any, Sequence

import attr
import requests
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import URI, BlockNumber
from eth_utils import address
from fixedpointmath import FixedPoint
from hexbytes import HexBytes
from web3 import Web3
from web3.contract.contract import Contract, ContractEvent, ContractFunction
from web3.middleware import geth_poa
from web3.types import ABI, ABIEvent, BlockData, EventData, LogReceipt, TxReceipt

from elfpy.data.db_schema import PoolInfo, Transaction
from elfpy.markets.hyperdrive import hyperdrive_assets


class TestAccount:
    """Web3 account that has helper functions & associated funding source"""

    # TODO: We should be adding more methods to this class.
    # If not, we can delete it at the end of the refactor.
    # pylint: disable=too-few-public-methods

    def __init__(self, extra_entropy: str = "TEST ACCOUNT"):
        """Initialize an account"""
        self.account: LocalAccount = Account().create(extra_entropy=extra_entropy)

    @property
    def address(self) -> str:
        """Return the address of the account"""
        return self.account.address


@attr.s
class HyperdriveAddressesJson:
    """Addresses for deployed Hyperdrive contracts."""

    # pylint: disable=too-few-public-methods

    base_token: str = attr.ib()
    mock_hyperdrive: str = attr.ib()
    mock_hyperdrive_math: str = attr.ib()


def get_account_balance_for_contract(funding_contract: Contract, account_address: str) -> int:
    """Return the balance of the account"""
    return funding_contract.functions.balanceOf(account_address).call()


def fund_account(funding_contract: Contract, account_address: str, amount: int) -> HexBytes:
    """Add funds to the account"""
    tx_receipt = funding_contract.functions.mint(account_address, amount).transact()
    return tx_receipt


def camel_to_snake(camel_string: str) -> str:
    """Convert camelCase to snake_case"""
    snake_string = re.sub(r"(?<!^)(?=[A-Z])", "_", camel_string)
    return snake_string.lower()


def collect_files(folder_path: str, extension: str = ".json") -> list[str]:
    """Load all files with the given extension into a list"""
    collected_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                collected_files.append(file_path)
    return collected_files


def load_all_abis(abi_folder: str) -> dict:
    """Load the ABI from the JSON file"""
    abis = {}
    abi_files = collect_files(abi_folder)
    for abi_file in abi_files:
        file_name = os.path.splitext(os.path.basename(abi_file))[0]
        with open(abi_file, mode="r", encoding="UTF-8") as file:
            data = json.load(file)
        if "abi" in data:
            logging.info("Loaded ABI file %s", abi_file)
            abis[file_name] = data["abi"]
        else:
            logging.warning("JSON file %s did not contain an ABI", abi_file)
    return abis


def fetch_and_decode_logs(web3: Web3, contract: Contract, tx_receipt: TxReceipt) -> list[dict[Any, Any]]:
    """Decode logs from a transaction receipt"""
    logs = []
    if tx_receipt.get("logs"):
        for log in tx_receipt["logs"]:
            event_data, event = get_event_object(web3, contract, log, tx_receipt)
            if event_data and event:
                formatted_log = dict(event_data)
                formatted_log["event"] = event.get("name")
                formatted_log["args"] = dict(event_data["args"])
                logs.append(formatted_log)
    return logs


def convert_fixedpoint(input_val: int | None) -> float | None:
    """Given a scaled value int, converts it to an unscaled value in float, while dealing with Nones"""

    # We cast to FixedPoint, then to floats to keep noise to a minimum
    # This is assuming there's no loss of precision going from Fixedpoint to float
    # Once this gets fed into postgres, postgres has fixed precision Numeric type
    if input is not None:
        return float(FixedPoint(scaled_value=input_val))
    else:
        return None


# TODO receipt isn't used, but adding it here to map previous implementation of writing this to file
# Remove if necessary
def build_transaction_object(
    transaction_dict: dict[str, Any],
    logs: list[dict[str, Any]],
    receipt: dict[str, Any],
) -> Transaction:
    """Conversion function to translate output of chain queries to the Transaction object"""

    # Build output obj dict incrementally to be passed into Transaction
    # i.e., Transaction(**out_dict)

    # Base transaction fields
    out_dict: dict[str, Any] = {
        "blockNumber": transaction_dict["blockNumber"],
        "transactionIndex": transaction_dict["transactionIndex"],
        "nonce": transaction_dict["nonce"],
        "transactionHash": transaction_dict["hash"],
        "txn_to": transaction_dict["to"],
        "txn_from": transaction_dict["from"],
        "gasUsed": receipt["gasUsed"],
    }

    # Input solidity methods and parameters
    # TODO can the input field ever be empty or not exist?
    out_dict["input_method"] = transaction_dict["input"]["method"]
    input_params = transaction_dict["input"]["params"]
    out_dict["input_params_contribution"] = convert_fixedpoint(input_params.get("_contribution", None))
    out_dict["input_params_apr"] = convert_fixedpoint(input_params.get("_apr", None))
    out_dict["input_params_destination"] = input_params.get("_destination", None)
    out_dict["input_params_asUnderlying"] = input_params.get("_asUnderlying", None)
    out_dict["input_params_baseAmount"] = convert_fixedpoint(input_params.get("_baseAmount", None))
    out_dict["input_params_minOutput"] = convert_fixedpoint(input_params.get("_minOutput", None))
    out_dict["input_params_bondAmount"] = convert_fixedpoint(input_params.get("_bondAmount", None))
    out_dict["input_params_maxDeposit"] = convert_fixedpoint(input_params.get("_maxDeposit", None))
    out_dict["input_params_maturityTime"] = input_params.get("_maturityTime", None)
    out_dict["input_params_minApr"] = convert_fixedpoint(input_params.get("_minApr", None))
    out_dict["input_params_maxApr"] = convert_fixedpoint(input_params.get("_maxApr", None))
    out_dict["input_params_shares"] = convert_fixedpoint(input_params.get("_shares", None))

    # Assuming one TransferSingle per transfer
    # TODO Fix this below eventually
    # There can be two transfer singles
    # Currently grab first transfer single (e.g., Minting hyperdrive long, so address 0 to agent)
    # Eventually need grabbing second transfer single (e.g., DAI from agent to hyperdrive)
    event_logs = [log for log in logs if log["event"] == "TransferSingle"]
    if len(event_logs) == 0:
        event_args: dict[str, Any] = {}
        # Set args as None
    elif len(event_logs) == 1:
        event_args: dict[str, Any] = event_logs[0]["args"]
    else:
        logging.warning("Tranfer event contains multiple TransferSingle logs, selecting first")
        event_args: dict[str, Any] = event_logs[0]["args"]

    out_dict["event_value"] = convert_fixedpoint(event_args.get("value", None))
    out_dict["event_from"] = event_args.get("from", None)
    out_dict["event_to"] = event_args.get("to", None)
    out_dict["event_operator"] = event_args.get("operator", None)
    out_dict["event_id"] = event_args.get("id", None)

    # Decode logs here
    if out_dict["event_id"]:
        event_prefix, event_maturity_time = hyperdrive_assets.decode_asset_id(out_dict["event_id"])
        out_dict["event_prefix"] = event_prefix
        out_dict["event_maturity_time"] = event_maturity_time

    transaction = Transaction(**out_dict)

    return transaction


def fetch_transactions_for_block(web3: Web3, contract: Contract, block_number: BlockNumber) -> list[Transaction]:
    """Fetch transactions related to the contract"""
    block: BlockData = web3.eth.get_block(block_number, full_transactions=True)
    transactions = block.get("transactions")
    if not transactions:
        logging.info("no transactions in block %s", block.get("number"))
        return []
    # decoded_block_transactions = []
    out_transactions = []
    for transaction in transactions:
        if isinstance(transaction, HexBytes):
            logging.warning("transaction HexBytes")
            continue
        if transaction.get("to") != contract.address:
            logging.warning("transaction not from contract")
            continue
        transaction_dict: dict[str, Any] = dict(transaction)
        # Convert the HexBytes fields to their hex representation
        tx_hash = transaction.get("hash") or HexBytes("")
        transaction_dict["hash"] = tx_hash.hex()
        # Decode the transaction input
        try:
            method, params = contract.decode_function_input(transaction["input"])
            transaction_dict["input"] = {"method": method.fn_name, "params": params}
        except ValueError:  # if the input is not meant for the contract, ignore it
            continue
        tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
        logs = fetch_and_decode_logs(web3, contract, tx_receipt)
        receipt: dict[str, Any] = recursive_dict_conversion(tx_receipt)  # type: ignore

        out_transactions.append(build_transaction_object(transaction_dict, logs, receipt))

    return out_transactions


def get_event_object(
    web3: Web3, contract: Contract, log: LogReceipt, tx_receipt: TxReceipt
) -> tuple[EventData, ABIEvent] | tuple[None, None]:
    """Retrieves the event object and anonymous types for a  given contract and log"""
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


def get_smart_contract_read_call(contract: Contract, function_name: str, **function_args) -> dict[Any, Any]:
    """Get a smart contract read call"""
    # TODO: Fix this up to actually decode the ABI using web3
    # decode ABI to get variable names
    abi: ABI = contract.abi
    abi_function_index = [idx for idx in range(len(abi)) if abi[idx].get("name") == function_name][0]
    abi_outputs = abi[abi_function_index].get("outputs")
    if not isinstance(abi_outputs, Sequence):
        raise AssertionError("could not find outputs in the abi")
    abi_components = abi_outputs[0].get("components")
    if abi_components is None:
        raise AssertionError("could not find output components in the abi")
    return_value_keys = [component.get("name") for component in abi_components]
    # get the callable contract function from function_name & call it
    function: ContractFunction = contract.get_function_by_name(function_name)()
    return_values = function.call(**function_args)
    # associate returned values with the keys
    assert len(return_value_keys) == len(return_values)
    function_return_dict = dict((variable_name, info) for variable_name, info in zip(return_value_keys, return_values))
    return function_return_dict


def recursive_dict_conversion(obj):
    """Recursively converts a dictionary to convert objects to hex values"""
    if isinstance(obj, HexBytes):
        return obj.hex()
    if isinstance(obj, dict):
        return {key: recursive_dict_conversion(value) for key, value in obj.items()}
    if hasattr(obj, "items"):
        return {key: recursive_dict_conversion(value) for key, value in obj.items()}
    return obj


def initialize_web3_with_http_provider(ethereum_node: URI | str, request_kwargs: dict | None = None) -> Web3:
    """Initialize a Web3 instance using an HTTP provider and inject a geth Proof of Authority (poa) middleware.

    Arguments
    ---------
    ethereum_node: URI | str
        Address of the http provider
    request_kwargs: dict
        The HTTPProvider uses the python requests library for making requests.
        If you would like to modify how requests are made,
        you can use the request_kwargs to do so.
    """
    if request_kwargs is None:
        request_kwargs = {}
    provider = Web3.HTTPProvider(ethereum_node, request_kwargs)
    web3 = Web3(provider)
    web3.middleware_onion.inject(geth_poa.geth_poa_middleware, layer=0)
    return web3


def fetch_address_from_url(contracts_url: str) -> HyperdriveAddressesJson:
    """Fetch addresses for deployed contracts in the Hyperdrive system."""
    attempt_num = 0
    response = None
    while attempt_num < 100:
        response = requests.get(contracts_url, timeout=60)
        # Check the status code and retry the request if it fails
        if response.status_code != 200:
            logging.warning("Request failed with status code %s @ %s", response.status_code, time.ctime())
            time.sleep(10)
            continue
        attempt_num += 1
    if response is None:
        raise ConnectionError("Request failed, returning status `None`")
    if response.status_code != 200:
        raise ConnectionError(f"Request failed with status code {response.status_code} @ {time.ctime()}")
    addresses_json = response.json()
    addresses = HyperdriveAddressesJson(**{camel_to_snake(key): value for key, value in addresses_json.items()})
    return addresses


def get_block_pool_info(web3_container: Web3, hyperdrive_contract: Contract, block_number: BlockNumber) -> PoolInfo:
    """Returns the block pool info from the Hyperdrive contract"""
    pool_info_data_dict = get_smart_contract_read_call(
        hyperdrive_contract, "getPoolInfo", block_identifier=block_number
    )

    # All data returned from this call is in scaled notation
    # We cast to FixedPoint, then to floats to keep noise to a minimum
    # This is assuming there's no loss of precision going from Fixedpoint to float
    # Once this gets fed into postgres, postgres has fixed precision Numeric type
    pool_info_data_dict: dict[Any, Any] = {
        key: float(FixedPoint(scaled_value=value)) for (key, value) in pool_info_data_dict.items()
    }

    current_block: BlockData = web3_container.eth.get_block(block_number)
    current_block_timestamp = current_block.get("timestamp")
    if current_block_timestamp is None:
        raise AssertionError("Current block has no timestamp")

    pool_info_data_dict.update({"timestamp": current_block_timestamp})
    pool_info_data_dict.update({"blockNumber": block_number})

    pool_info_dict = {}
    for key in PoolInfo.__annotations__.keys():
        # Required keys
        if key == "timestamp":
            pool_info_dict[key] = datetime.fromtimestamp(pool_info_data_dict[key])
        elif key == "blockNumber":
            pool_info_dict[key] = pool_info_data_dict[key]
        # Otherwise default to None if not exist
        else:
            pool_info_dict[key] = pool_info_data_dict.get(key, None)

    # Populating the dataclass from the dictionary
    pool_info = PoolInfo(**pool_info_dict)

    return pool_info


def get_hyperdrive_contract(abi_file_path: str, contracts_url: str, web3: Web3) -> Contract:
    """Get the hyperdrive contract for a given abi"""
    addresses = fetch_address_from_url(contracts_url)
    # Load the ABI from the JSON file
    with open(abi_file_path, "r", encoding="UTF-8") as file:
        state_abi = json.load(file)["abi"]
    # get contract instance of hyperdrive
    hyperdrive_contract: Contract = web3.eth.contract(
        address=address.to_checksum_address(addresses.mock_hyperdrive), abi=state_abi
    )
    return hyperdrive_contract


def get_hyperdrive_config(hyperdrive_contract: Contract) -> dict:
    """Get the hyperdrive config from a deployed hyperdrive contract.

    Arguments
    ----------
    hyperdrive_contract : Contract
        The deployed hyperdrive contract instance.

    Returns
    -------
    hyperdrive_config : dict
        The hyperdrive config.

    """
    hyperdrive_config: dict = get_smart_contract_read_call(hyperdrive_contract, "getPoolConfig")
    hyperdrive_config["invScaledTimeStretch"] = 1 / (hyperdrive_config["timeStretch"] / 1e18)
    hyperdrive_config["termLength"] = hyperdrive_config["positionDuration"] / 60 / 60 / 24  # in days
    return hyperdrive_config
