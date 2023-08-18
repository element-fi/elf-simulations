"""Script to generate typed web3.py classes for solidity contracts."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import TypeGuard

from jinja2 import Environment, FileSystemLoader
from web3 import Web3
from web3.types import ABIEvent, ABIFunction

from .pypechain.utilities.format import avoid_python_keywords
from .pypechain.utilities.types import solidity_to_python_type


def load_abi_from_file(file_path: Path):
    """Loads a contract ABI from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)["abi"]


def main(abi_file_path: str, output_file_path: str):
    """Generates class files for a given abi."""
    # Load ABI
    file_path = Path(abi_file_path)
    # contract_abi = load_abi_from_file(file_path)

    # Set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))

    template_file_path = "/templates/contract.jinja2"
    print(f"{os.getcwd() + template_file_path}")

    template = env.get_template("contract.jinja2")

    _web3 = Web3()
    contract = _web3.eth.contract(abi=abi_file_path)

    # leverage the private list of ABIFunction's
    # pylint: disable=protected-access
    abi_functions_and_events = contract.functions._functions

    # Extract function names and their input parameters from the ABI
    function_datas = []
    for abi_function in abi_functions_and_events:
        if is_abi_function(abi_function):
            function_data = {
                "name": abi_function.get("name"),
                "input_names_and_types": get_input_names_and_values(abi_function),
                "input_names": [get_input_names(abi_function)],
            }
            function_datas.append(function_data)

    # Render the template
    filename = file_path.name
    contract_name = os.path.splitext(filename)[0]
    rendered_code = template.render(contract_name=contract_name, functions=function_datas)

    # Save the rendered code to a file
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(rendered_code)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <path_to_abi_file> <contract_address> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2])


def get_input_names_and_values(function: ABIFunction) -> list[str]:
    """Returns function input name/type strings for jinja templating.

    i.e. for the solidity function signature:
    function doThing(address who, uint256 amount, bool flag, bytes extraData)

    the following list would be returned:
    ['who: str', 'amount: int', 'flag: bool', 'extraData: bytes']
    """

    stringified_function_parameters: list[str] = []
    for _input in function.get("inputs", []):
        name = _input.get("name")
        if name is None:
            raise ValueError("Solidity function parameter name cannot be None")
        python_type = solidity_to_python_type(_input.get("type", "unknown"))
        stringified_function_parameters.append(f"{name}: {python_type}")

    return stringified_function_parameters


def get_input_names(function: ABIFunction) -> list[str]:
    """Returns function input name/type strings for jinja templating.

    i.e. for the solidity function signature:
    function doThing(address who, uint256 amount, bool flag, bytes extraData)

    the following list would be returned:
    ['who', 'amount', 'flag', 'extraData']
    """

    stringified_function_parameters: list[str] = []
    for _input in function.get("inputs", []):
        name = _input.get("name")
        if name is None:
            raise ValueError("name cannot be None")
        stringified_function_parameters.append(avoid_python_keywords(name))

    return stringified_function_parameters


def is_abi_function(item: ABIFunction | ABIEvent) -> TypeGuard[ABIFunction]:
    """Typeguard function"""
    # Check if the required keys exist
    required_keys = ["type", "name", "inputs"]

    # Check if the required keys exist
    if not all(key in item for key in required_keys):
        return False

    # Check if the type is "function"
    if item.get("type") != "function":
        return False

    return True
