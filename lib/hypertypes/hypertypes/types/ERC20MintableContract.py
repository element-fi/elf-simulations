"""A web3.py Contract class for the ERC20Mintable contract."""

# contracts have PascalCase names
# pylint: disable=invalid-name

# contracts control how many attributes and arguments we have in generated code
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments

# we don't need else statement if the other conditionals all have return,
# but it's easier to generate
# pylint: disable=no-else-return

# This file is bound to get very long depending on contract sizes.
# pylint: disable=too-many-lines

from __future__ import annotations
from typing import Any, Tuple, Type, TypeVar, cast
from typing_extensions import Self
from dataclasses import fields, is_dataclass

from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes
from web3 import Web3
from web3.contract.contract import Contract, ContractFunction, ContractFunctions
from web3.exceptions import FallbackNotFound
from web3.types import ABI, BlockIdentifier, CallOverride, TxParams

from multimethod import multimethod


T = TypeVar("T")

structs = {}


def tuple_to_dataclass(cls: type[T], tuple_data: Any | Tuple[Any, ...]) -> T:
    """
    Converts a tuple (including nested tuples) to a dataclass instance.  If cls is not a dataclass,
    then the data will just be passed through this function.

    Arguments
    ---------
    cls: type[T]
        The dataclass type to which the tuple data is to be converted.
    tuple_data: Any | Tuple[Any, ...]
        A tuple (or nested tuple) of values to convert into a dataclass instance.

    Returns
    -------
    T
        Either an instance of cls populated with data from tuple_data or tuple_data itself.
    """
    if not is_dataclass(cls):
        return cast(T, tuple_data)

    field_types = {field.name: field.type for field in fields(cls)}
    field_values = {}

    for (field_name, field_type), value in zip(field_types.items(), tuple_data):
        field_type = structs.get(field_type, field_type)
        if is_dataclass(field_type):
            # Recursively convert nested tuples to nested dataclasses
            field_values[field_name] = tuple_to_dataclass(field_type, value)
        elif (
            isinstance(value, tuple)
            and not getattr(field_type, "_name", None) == "Tuple"
        ):
            # If it's a tuple and the field is not intended to be a tuple, assume it's a nested dataclass
            field_values[field_name] = tuple_to_dataclass(field_type, value)
        else:
            # Otherwise, set the primitive value directly
            field_values[field_name] = value

    return cls(**field_values)


class ERC20MintableDOMAIN_SEPARATORContractFunction(ContractFunction):
    """ContractFunction for the DOMAIN_SEPARATOR method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "ERC20MintableDOMAIN_SEPARATORContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bytes:
        """returns bytes"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bytes

        return cast(bytes, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableAllowanceContractFunction(ContractFunction):
    """ContractFunction for the allowance method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, arg1: str, arg2: str
    ) -> "ERC20MintableAllowanceContractFunction":
        clone = super().__call__(arg1, arg2)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableApproveContractFunction(ContractFunction):
    """ContractFunction for the approve method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, spender: str, amount: int
    ) -> "ERC20MintableApproveContractFunction":
        clone = super().__call__(spender, amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableAuthorityContractFunction(ContractFunction):
    """ContractFunction for the authority method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "ERC20MintableAuthorityContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableBalanceOfContractFunction(ContractFunction):
    """ContractFunction for the balanceOf method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str) -> "ERC20MintableBalanceOfContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableBurnContractFunction(ContractFunction):
    """ContractFunction for the burn method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ# disable this warning when there is overloading
    # pylint: disable=function-redefined
    @multimethod
    def __call__(self, amount: int) -> "ERC20MintableBurnContractFunction":  # type: ignore
        clone = super().__call__(amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    @multimethod
    def call(  # type: ignore
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    @multimethod
    def __call__(self, destination: str, amount: int) -> "ERC20MintableBurnContractFunction":  # type: ignore
        clone = super().__call__(destination, amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    @multimethod
    def call(  # type: ignore
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableCanCallContractFunction(ContractFunction):
    """ContractFunction for the canCall method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, user: str, target: str, functionSig: bytes
    ) -> "ERC20MintableCanCallContractFunction":
        clone = super().__call__(user, target, functionSig)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableDecimalsContractFunction(ContractFunction):
    """ContractFunction for the decimals method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "ERC20MintableDecimalsContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableDoesRoleHaveCapabilityContractFunction(ContractFunction):
    """ContractFunction for the doesRoleHaveCapability method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, role: int, functionSig: bytes
    ) -> "ERC20MintableDoesRoleHaveCapabilityContractFunction":
        clone = super().__call__(role, functionSig)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableDoesUserHaveRoleContractFunction(ContractFunction):
    """ContractFunction for the doesUserHaveRole method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, user: str, role: int
    ) -> "ERC20MintableDoesUserHaveRoleContractFunction":
        clone = super().__call__(user, role)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableGetRolesWithCapabilityContractFunction(ContractFunction):
    """ContractFunction for the getRolesWithCapability method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, arg1: bytes
    ) -> "ERC20MintableGetRolesWithCapabilityContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bytes:
        """returns bytes"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bytes

        return cast(bytes, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableGetTargetCustomAuthorityContractFunction(ContractFunction):
    """ContractFunction for the getTargetCustomAuthority method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, arg1: str
    ) -> "ERC20MintableGetTargetCustomAuthorityContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableGetUserRolesContractFunction(ContractFunction):
    """ContractFunction for the getUserRoles method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, arg1: str
    ) -> "ERC20MintableGetUserRolesContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bytes:
        """returns bytes"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bytes

        return cast(bytes, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableIsCapabilityPublicContractFunction(ContractFunction):
    """ContractFunction for the isCapabilityPublic method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, arg1: bytes
    ) -> "ERC20MintableIsCapabilityPublicContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableIsCompetitionModeContractFunction(ContractFunction):
    """ContractFunction for the isCompetitionMode method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "ERC20MintableIsCompetitionModeContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableMintContractFunction(ContractFunction):
    """ContractFunction for the mint method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ# disable this warning when there is overloading
    # pylint: disable=function-redefined
    @multimethod
    def __call__(self, destination: str, amount: int) -> "ERC20MintableMintContractFunction":  # type: ignore
        clone = super().__call__(destination, amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    @multimethod
    def call(  # type: ignore
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    @multimethod
    def __call__(self, amount: int) -> "ERC20MintableMintContractFunction":  # type: ignore
        clone = super().__call__(amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    @multimethod
    def call(  # type: ignore
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableNameContractFunction(ContractFunction):
    """ContractFunction for the name method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "ERC20MintableNameContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableNoncesContractFunction(ContractFunction):
    """ContractFunction for the nonces method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str) -> "ERC20MintableNoncesContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableOwnerContractFunction(ContractFunction):
    """ContractFunction for the owner method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "ERC20MintableOwnerContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintablePermitContractFunction(ContractFunction):
    """ContractFunction for the permit method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self,
        owner: str,
        spender: str,
        value: int,
        deadline: int,
        v: int,
        r: bytes,
        s: bytes,
    ) -> "ERC20MintablePermitContractFunction":
        clone = super().__call__(owner, spender, value, deadline, v, r, s)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableSetAuthorityContractFunction(ContractFunction):
    """ContractFunction for the setAuthority method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, newAuthority: str
    ) -> "ERC20MintableSetAuthorityContractFunction":
        clone = super().__call__(newAuthority)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableSetPublicCapabilityContractFunction(ContractFunction):
    """ContractFunction for the setPublicCapability method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, functionSig: bytes, enabled: bool
    ) -> "ERC20MintableSetPublicCapabilityContractFunction":
        clone = super().__call__(functionSig, enabled)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableSetRoleCapabilityContractFunction(ContractFunction):
    """ContractFunction for the setRoleCapability method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, role: int, functionSig: bytes, enabled: bool
    ) -> "ERC20MintableSetRoleCapabilityContractFunction":
        clone = super().__call__(role, functionSig, enabled)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableSetTargetCustomAuthorityContractFunction(ContractFunction):
    """ContractFunction for the setTargetCustomAuthority method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, target: str, customAuthority: str
    ) -> "ERC20MintableSetTargetCustomAuthorityContractFunction":
        clone = super().__call__(target, customAuthority)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableSetUserRoleContractFunction(ContractFunction):
    """ContractFunction for the setUserRole method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, user: str, role: int, enabled: bool
    ) -> "ERC20MintableSetUserRoleContractFunction":
        clone = super().__call__(user, role, enabled)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableSymbolContractFunction(ContractFunction):
    """ContractFunction for the symbol method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "ERC20MintableSymbolContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableTotalSupplyContractFunction(ContractFunction):
    """ContractFunction for the totalSupply method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "ERC20MintableTotalSupplyContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableTransferContractFunction(ContractFunction):
    """ContractFunction for the transfer method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, to: str, amount: int
    ) -> "ERC20MintableTransferContractFunction":
        clone = super().__call__(to, amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableTransferFromContractFunction(ContractFunction):
    """ContractFunction for the transferFrom method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, _from: str, to: str, amount: int
    ) -> "ERC20MintableTransferFromContractFunction":
        clone = super().__call__(_from, to, amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableTransferOwnershipContractFunction(ContractFunction):
    """ContractFunction for the transferOwnership method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self, newOwner: str
    ) -> "ERC20MintableTransferOwnershipContractFunction":
        clone = super().__call__(newOwner)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ):
        """No return value"""
        raw_values = super().call(
            transaction, block_identifier, state_override, ccip_read_enabled
        )
        # Define the expected return types from the smart contract call
        return_types = None

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (
                    tuple_to_dataclass(return_type, value)
                    for return_type, value in zip(return_types, raw_values)
                )
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class ERC20MintableContractFunctions(ContractFunctions):
    """ContractFunctions for the ERC20Mintable contract."""

    DOMAIN_SEPARATOR: ERC20MintableDOMAIN_SEPARATORContractFunction

    allowance: ERC20MintableAllowanceContractFunction

    approve: ERC20MintableApproveContractFunction

    authority: ERC20MintableAuthorityContractFunction

    balanceOf: ERC20MintableBalanceOfContractFunction

    burn: ERC20MintableBurnContractFunction

    canCall: ERC20MintableCanCallContractFunction

    decimals: ERC20MintableDecimalsContractFunction

    doesRoleHaveCapability: ERC20MintableDoesRoleHaveCapabilityContractFunction

    doesUserHaveRole: ERC20MintableDoesUserHaveRoleContractFunction

    getRolesWithCapability: ERC20MintableGetRolesWithCapabilityContractFunction

    getTargetCustomAuthority: ERC20MintableGetTargetCustomAuthorityContractFunction

    getUserRoles: ERC20MintableGetUserRolesContractFunction

    isCapabilityPublic: ERC20MintableIsCapabilityPublicContractFunction

    isCompetitionMode: ERC20MintableIsCompetitionModeContractFunction

    mint: ERC20MintableMintContractFunction

    name: ERC20MintableNameContractFunction

    nonces: ERC20MintableNoncesContractFunction

    owner: ERC20MintableOwnerContractFunction

    permit: ERC20MintablePermitContractFunction

    setAuthority: ERC20MintableSetAuthorityContractFunction

    setPublicCapability: ERC20MintableSetPublicCapabilityContractFunction

    setRoleCapability: ERC20MintableSetRoleCapabilityContractFunction

    setTargetCustomAuthority: ERC20MintableSetTargetCustomAuthorityContractFunction

    setUserRole: ERC20MintableSetUserRoleContractFunction

    symbol: ERC20MintableSymbolContractFunction

    totalSupply: ERC20MintableTotalSupplyContractFunction

    transfer: ERC20MintableTransferContractFunction

    transferFrom: ERC20MintableTransferFromContractFunction

    transferOwnership: ERC20MintableTransferOwnershipContractFunction

    def __init__(
        self,
        abi: ABI,
        w3: "Web3",
        address: ChecksumAddress | None = None,
        decode_tuples: bool | None = False,
    ) -> None:
        super().__init__(abi, w3, address, decode_tuples)
        self.DOMAIN_SEPARATOR = (
            ERC20MintableDOMAIN_SEPARATORContractFunction.factory(
                "DOMAIN_SEPARATOR",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="DOMAIN_SEPARATOR",
            )
        )
        self.allowance = ERC20MintableAllowanceContractFunction.factory(
            "allowance",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="allowance",
        )
        self.approve = ERC20MintableApproveContractFunction.factory(
            "approve",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="approve",
        )
        self.authority = ERC20MintableAuthorityContractFunction.factory(
            "authority",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="authority",
        )
        self.balanceOf = ERC20MintableBalanceOfContractFunction.factory(
            "balanceOf",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="balanceOf",
        )
        self.burn = ERC20MintableBurnContractFunction.factory(
            "burn",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="burn",
        )
        self.canCall = ERC20MintableCanCallContractFunction.factory(
            "canCall",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="canCall",
        )
        self.decimals = ERC20MintableDecimalsContractFunction.factory(
            "decimals",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="decimals",
        )
        self.doesRoleHaveCapability = (
            ERC20MintableDoesRoleHaveCapabilityContractFunction.factory(
                "doesRoleHaveCapability",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="doesRoleHaveCapability",
            )
        )
        self.doesUserHaveRole = (
            ERC20MintableDoesUserHaveRoleContractFunction.factory(
                "doesUserHaveRole",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="doesUserHaveRole",
            )
        )
        self.getRolesWithCapability = (
            ERC20MintableGetRolesWithCapabilityContractFunction.factory(
                "getRolesWithCapability",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="getRolesWithCapability",
            )
        )
        self.getTargetCustomAuthority = (
            ERC20MintableGetTargetCustomAuthorityContractFunction.factory(
                "getTargetCustomAuthority",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="getTargetCustomAuthority",
            )
        )
        self.getUserRoles = ERC20MintableGetUserRolesContractFunction.factory(
            "getUserRoles",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="getUserRoles",
        )
        self.isCapabilityPublic = (
            ERC20MintableIsCapabilityPublicContractFunction.factory(
                "isCapabilityPublic",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="isCapabilityPublic",
            )
        )
        self.isCompetitionMode = (
            ERC20MintableIsCompetitionModeContractFunction.factory(
                "isCompetitionMode",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="isCompetitionMode",
            )
        )
        self.mint = ERC20MintableMintContractFunction.factory(
            "mint",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="mint",
        )
        self.name = ERC20MintableNameContractFunction.factory(
            "name",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="name",
        )
        self.nonces = ERC20MintableNoncesContractFunction.factory(
            "nonces",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="nonces",
        )
        self.owner = ERC20MintableOwnerContractFunction.factory(
            "owner",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="owner",
        )
        self.permit = ERC20MintablePermitContractFunction.factory(
            "permit",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="permit",
        )
        self.setAuthority = ERC20MintableSetAuthorityContractFunction.factory(
            "setAuthority",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="setAuthority",
        )
        self.setPublicCapability = (
            ERC20MintableSetPublicCapabilityContractFunction.factory(
                "setPublicCapability",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="setPublicCapability",
            )
        )
        self.setRoleCapability = (
            ERC20MintableSetRoleCapabilityContractFunction.factory(
                "setRoleCapability",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="setRoleCapability",
            )
        )
        self.setTargetCustomAuthority = (
            ERC20MintableSetTargetCustomAuthorityContractFunction.factory(
                "setTargetCustomAuthority",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="setTargetCustomAuthority",
            )
        )
        self.setUserRole = ERC20MintableSetUserRoleContractFunction.factory(
            "setUserRole",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="setUserRole",
        )
        self.symbol = ERC20MintableSymbolContractFunction.factory(
            "symbol",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="symbol",
        )
        self.totalSupply = ERC20MintableTotalSupplyContractFunction.factory(
            "totalSupply",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="totalSupply",
        )
        self.transfer = ERC20MintableTransferContractFunction.factory(
            "transfer",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="transfer",
        )
        self.transferFrom = ERC20MintableTransferFromContractFunction.factory(
            "transferFrom",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="transferFrom",
        )
        self.transferOwnership = (
            ERC20MintableTransferOwnershipContractFunction.factory(
                "transferOwnership",
                w3=w3,
                contract_abi=abi,
                address=address,
                decode_tuples=decode_tuples,
                function_identifier="transferOwnership",
            )
        )


erc20mintable_abi: ABI = cast(
    ABI,
    [
        {
            "inputs": [
                {"internalType": "string", "name": "name", "type": "string"},
                {"internalType": "string", "name": "symbol", "type": "string"},
                {"internalType": "uint8", "name": "decimals", "type": "uint8"},
                {"internalType": "address", "name": "admin", "type": "address"},
                {
                    "internalType": "bool",
                    "name": "isCompetitionMode_",
                    "type": "bool",
                },
            ],
            "stateMutability": "nonpayable",
            "type": "constructor",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "owner",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "spender",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Approval",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "contract Authority",
                    "name": "newAuthority",
                    "type": "address",
                },
            ],
            "name": "AuthorityUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address",
                },
            ],
            "name": "OwnershipTransferred",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "enabled",
                    "type": "bool",
                },
            ],
            "name": "PublicCapabilityUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint8",
                    "name": "role",
                    "type": "uint8",
                },
                {
                    "indexed": True,
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "enabled",
                    "type": "bool",
                },
            ],
            "name": "RoleCapabilityUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "target",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "contract Authority",
                    "name": "authority",
                    "type": "address",
                },
            ],
            "name": "TargetCustomAuthorityUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "from",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Transfer",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "uint8",
                    "name": "role",
                    "type": "uint8",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "enabled",
                    "type": "bool",
                },
            ],
            "name": "UserRoleUpdated",
            "type": "event",
        },
        {
            "inputs": [],
            "name": "DOMAIN_SEPARATOR",
            "outputs": [
                {"internalType": "bytes32", "name": "", "type": "bytes32"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"},
                {"internalType": "address", "name": "", "type": "address"},
            ],
            "name": "allowance",
            "outputs": [
                {"internalType": "uint256", "name": "", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "spender",
                    "type": "address",
                },
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "approve",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "authority",
            "outputs": [
                {
                    "internalType": "contract Authority",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"}
            ],
            "name": "balanceOf",
            "outputs": [
                {"internalType": "uint256", "name": "", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "amount", "type": "uint256"}
            ],
            "name": "burn",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "destination",
                    "type": "address",
                },
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "burn",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "user", "type": "address"},
                {
                    "internalType": "address",
                    "name": "target",
                    "type": "address",
                },
                {
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
            ],
            "name": "canCall",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "decimals",
            "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint8", "name": "role", "type": "uint8"},
                {
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
            ],
            "name": "doesRoleHaveCapability",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint8", "name": "role", "type": "uint8"},
            ],
            "name": "doesUserHaveRole",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes4", "name": "", "type": "bytes4"}
            ],
            "name": "getRolesWithCapability",
            "outputs": [
                {"internalType": "bytes32", "name": "", "type": "bytes32"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"}
            ],
            "name": "getTargetCustomAuthority",
            "outputs": [
                {
                    "internalType": "contract Authority",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"}
            ],
            "name": "getUserRoles",
            "outputs": [
                {"internalType": "bytes32", "name": "", "type": "bytes32"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes4", "name": "", "type": "bytes4"}
            ],
            "name": "isCapabilityPublic",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "isCompetitionMode",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "destination",
                    "type": "address",
                },
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "mint",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "amount", "type": "uint256"}
            ],
            "name": "mint",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [
                {"internalType": "string", "name": "", "type": "string"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"}
            ],
            "name": "nonces",
            "outputs": [
                {"internalType": "uint256", "name": "", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [
                {"internalType": "address", "name": "", "type": "address"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "owner", "type": "address"},
                {
                    "internalType": "address",
                    "name": "spender",
                    "type": "address",
                },
                {"internalType": "uint256", "name": "value", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "deadline",
                    "type": "uint256",
                },
                {"internalType": "uint8", "name": "v", "type": "uint8"},
                {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                {"internalType": "bytes32", "name": "s", "type": "bytes32"},
            ],
            "name": "permit",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "contract Authority",
                    "name": "newAuthority",
                    "type": "address",
                }
            ],
            "name": "setAuthority",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
                {"internalType": "bool", "name": "enabled", "type": "bool"},
            ],
            "name": "setPublicCapability",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint8", "name": "role", "type": "uint8"},
                {
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
                {"internalType": "bool", "name": "enabled", "type": "bool"},
            ],
            "name": "setRoleCapability",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "target",
                    "type": "address",
                },
                {
                    "internalType": "contract Authority",
                    "name": "customAuthority",
                    "type": "address",
                },
            ],
            "name": "setTargetCustomAuthority",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint8", "name": "role", "type": "uint8"},
                {"internalType": "bool", "name": "enabled", "type": "bool"},
            ],
            "name": "setUserRole",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "symbol",
            "outputs": [
                {"internalType": "string", "name": "", "type": "string"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "totalSupply",
            "outputs": [
                {"internalType": "uint256", "name": "", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "to", "type": "address"},
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "transfer",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "from", "type": "address"},
                {"internalType": "address", "name": "to", "type": "address"},
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "transferFrom",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address",
                }
            ],
            "name": "transferOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ],
)
# pylint: disable=line-too-long
erc20mintable_bytecode = HexStr(
    "0x6101006040523480156200001257600080fd5b5060405162001de338038062001de3833981016040819052620000359162000291565b8130818188888860006200004a8482620003d7565b506001620000598382620003d7565b5060ff81166080524660a0526200006f6200011a565b60c0525050600680546001600160a01b038086166001600160a01b03199283168117909355600780549186169190921617905560405190915033907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e090600090a36040516001600160a01b0382169033907fa3396fd7f6e0a21b50e5089d2da70d5ac0a3bbbd1f617a93f134b7638998019890600090a350505050151560e052506200052192505050565b60007f8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f60006040516200014e9190620004a3565b6040805191829003822060208301939093528101919091527fc89efdaa54c0f20c7adf612882df0950f5a951637e0307cdcb4c672f298b8bc660608201524660808201523060a082015260c00160405160208183030381529060405280519060200120905090565b634e487b7160e01b600052604160045260246000fd5b600082601f830112620001de57600080fd5b81516001600160401b0380821115620001fb57620001fb620001b6565b604051601f8301601f19908116603f01168101908282118183101715620002265762000226620001b6565b816040528381526020925086838588010111156200024357600080fd5b600091505b8382101562000267578582018301518183018401529082019062000248565b600093810190920192909252949350505050565b805180151581146200028c57600080fd5b919050565b600080600080600060a08688031215620002aa57600080fd5b85516001600160401b0380821115620002c257600080fd5b620002d089838a01620001cc565b96506020880151915080821115620002e757600080fd5b50620002f688828901620001cc565b945050604086015160ff811681146200030e57600080fd5b60608701519093506001600160a01b03811681146200032c57600080fd5b91506200033c608087016200027b565b90509295509295909350565b600181811c908216806200035d57607f821691505b6020821081036200037e57634e487b7160e01b600052602260045260246000fd5b50919050565b601f821115620003d257600081815260208120601f850160051c81016020861015620003ad5750805b601f850160051c820191505b81811015620003ce57828155600101620003b9565b5050505b505050565b81516001600160401b03811115620003f357620003f3620001b6565b6200040b8162000404845462000348565b8462000384565b602080601f8311600181146200044357600084156200042a5750858301515b600019600386901b1c1916600185901b178555620003ce565b600085815260208120601f198616915b82811015620004745788860151825594840194600190910190840162000453565b5085821015620004935787850151600019600388901b60f8161c191681555b5050505050600190811b01905550565b6000808354620004b38162000348565b60018281168015620004ce5760018114620004e45762000515565b60ff198416875282151583028701945062000515565b8760005260208060002060005b858110156200050c5781548a820152908401908201620004f1565b50505082870194505b50929695505050505050565b60805160a05160c05160e05161186c620005776000396000818161037901528181610882015281816108e801528181610c270152610c890152600061085e01526000610829015260006102b9015261186c6000f3fe608060405234801561001057600080fd5b50600436106101f05760003560e01c80637a9e5e4b1161010f578063bf7e214f116100a2578063e688747b11610071578063e688747b146104c7578063ea7ca276146104fd578063ed0d0efb14610534578063f2fde38b1461055457600080fd5b8063bf7e214f1461044d578063c53a398514610460578063d505accf14610489578063dd62ed3e1461049c57600080fd5b80639dc29fac116100de5780639dc29fac14610401578063a0712d6814610414578063a9059cbb14610427578063b70096131461043a57600080fd5b80637a9e5e4b1461039b5780637ecebe00146103ae5780638da5cb5b146103ce57806395d89b41146103f957600080fd5b80633644e5151161018757806367aff4841161015657806367aff4841461032e57806370a0823114610341578063728b952b146103615780637a8c63b51461037457600080fd5b80633644e515146102ed57806340c10f19146102f557806342966c68146103085780634b5159da1461031b57600080fd5b80630ea9b75b116101c35780630ea9b75b1461028357806318160ddd1461029857806323b872dd146102a1578063313ce567146102b457600080fd5b806306a36aee146101f557806306fdde0314610228578063095ea7b31461023d5780630bade8a414610260575b600080fd5b610215610203366004611324565b60096020526000908152604090205481565b6040519081526020015b60405180910390f35b610230610567565b60405161021f9190611341565b61025061024b36600461138f565b6105f5565b604051901515815260200161021f565b61025061026e3660046113d8565b600a6020526000908152604090205460ff1681565b610296610291366004611412565b610662565b005b61021560025481565b6102506102af366004611459565b610743565b6102db7f000000000000000000000000000000000000000000000000000000000000000081565b60405160ff909116815260200161021f565b610215610825565b61029661030336600461138f565b610880565b61029661031636600461149a565b6108e6565b6102966103293660046114b3565b61094b565b61029661033c3660046114ea565b6109dd565b61021561034f366004611324565b60036020526000908152604090205481565b61029661036f366004611518565b610aa5565b6102507f000000000000000000000000000000000000000000000000000000000000000081565b6102966103a9366004611324565b610b2e565b6102156103bc366004611324565b60056020526000908152604090205481565b6006546103e1906001600160a01b031681565b6040516001600160a01b03909116815260200161021f565b610230610c18565b61029661040f36600461138f565b610c25565b61029661042236600461149a565b610c87565b61025061043536600461138f565b610ce9565b610250610448366004611546565b610d4f565b6007546103e1906001600160a01b031681565b6103e161046e366004611324565b6008602052600090815260409020546001600160a01b031681565b61029661049736600461158d565b610e4d565b6102156104aa366004611518565b600460209081526000928352604080842090915290825290205481565b6102506104d53660046115fb565b6001600160e01b0319166000908152600b602052604090205460ff919091161c600116151590565b61025061050b36600461162e565b6001600160a01b0391909116600090815260096020526040902054600160ff9092161c16151590565b6102156105423660046113d8565b600b6020526000908152604090205481565b610296610562366004611324565b611091565b600080546105749061165a565b80601f01602080910402602001604051908101604052809291908181526020018280546105a09061165a565b80156105ed5780601f106105c2576101008083540402835291602001916105ed565b820191906000526020600020905b8154815290600101906020018083116105d057829003601f168201915b505050505081565b3360008181526004602090815260408083206001600160a01b038716808552925280832085905551919290917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925906106509086815260200190565b60405180910390a35060015b92915050565b610678336000356001600160e01b03191661110f565b61069d5760405162461bcd60e51b815260040161069490611694565b60405180910390fd5b80156106cd576001600160e01b031982166000908152600b602052604090208054600160ff86161b1790556106f4565b6001600160e01b031982166000908152600b602052604090208054600160ff86161b191690555b816001600160e01b0319168360ff167fbfe16b2c35ce23dfd1ab0e7b5d086a10060c9b52d1574e1680c881b3b3a2b15183604051610736911515815260200190565b60405180910390a3505050565b6001600160a01b0383166000908152600460209081526040808320338452909152812054600019811461079f5761077a83826116d0565b6001600160a01b03861660009081526004602090815260408083203384529091529020555b6001600160a01b038516600090815260036020526040812080548592906107c79084906116d0565b90915550506001600160a01b0380851660008181526003602052604090819020805487019055519091871690600080516020611817833981519152906108109087815260200190565b60405180910390a360019150505b9392505050565b60007f0000000000000000000000000000000000000000000000000000000000000000461461085b576108566111b9565b905090565b507f000000000000000000000000000000000000000000000000000000000000000090565b7f0000000000000000000000000000000000000000000000000000000000000000156108d8576108bc336000356001600160e01b03191661110f565b6108d85760405162461bcd60e51b8152600401610694906116e3565b6108e28282611253565b5050565b7f00000000000000000000000000000000000000000000000000000000000000001561093e57610922336000356001600160e01b03191661110f565b61093e5760405162461bcd60e51b8152600401610694906116e3565b61094833826112ad565b50565b610961336000356001600160e01b03191661110f565b61097d5760405162461bcd60e51b815260040161069490611694565b6001600160e01b031982166000818152600a6020908152604091829020805460ff191685151590811790915591519182527f36d28126bef21a4f3765d7fcb7c45cead463ae4c41094ef3b771ede598544103910160405180910390a25050565b6109f3336000356001600160e01b03191661110f565b610a0f5760405162461bcd60e51b815260040161069490611694565b8015610a3e576001600160a01b03831660009081526009602052604090208054600160ff85161b179055610a64565b6001600160a01b03831660009081526009602052604090208054600160ff85161b191690555b8160ff16836001600160a01b03167f4c9bdd0c8e073eb5eda2250b18d8e5121ff27b62064fbeeeed4869bb99bc5bf283604051610736911515815260200190565b610abb336000356001600160e01b03191661110f565b610ad75760405162461bcd60e51b815260040161069490611694565b6001600160a01b0382811660008181526008602052604080822080546001600160a01b0319169486169485179055517fa4908e11a5f895b13d51526c331ac93cdd30e59772361c5d07874eb36bff20659190a35050565b6006546001600160a01b0316331480610bc3575060075460405163b700961360e01b81526001600160a01b039091169063b700961390610b8290339030906001600160e01b0319600035169060040161171a565b602060405180830381865afa158015610b9f573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610bc39190611747565b610bcc57600080fd5b600780546001600160a01b0319166001600160a01b03831690811790915560405133907fa3396fd7f6e0a21b50e5089d2da70d5ac0a3bbbd1f617a93f134b7638998019890600090a350565b600180546105749061165a565b7f000000000000000000000000000000000000000000000000000000000000000015610c7d57610c61336000356001600160e01b03191661110f565b610c7d5760405162461bcd60e51b8152600401610694906116e3565b6108e282826112ad565b7f000000000000000000000000000000000000000000000000000000000000000015610cdf57610cc3336000356001600160e01b03191661110f565b610cdf5760405162461bcd60e51b8152600401610694906116e3565b6109483382611253565b33600090815260036020526040812080548391908390610d0a9084906116d0565b90915550506001600160a01b03831660008181526003602052604090819020805485019055513390600080516020611817833981519152906106509086815260200190565b6001600160a01b038083166000908152600860205260408120549091168015610deb5760405163b700961360e01b81526001600160a01b0382169063b700961390610da29088908890889060040161171a565b602060405180830381865afa158015610dbf573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610de39190611747565b91505061081e565b6001600160e01b031983166000908152600a602052604090205460ff1680610e4457506001600160e01b031983166000908152600b60209081526040808320546001600160a01b03891684526009909252909120541615155b95945050505050565b42841015610e9d5760405162461bcd60e51b815260206004820152601760248201527f5045524d49545f444541444c494e455f455850495245440000000000000000006044820152606401610694565b60006001610ea9610825565b6001600160a01b038a811660008181526005602090815260409182902080546001810190915582517f6e71edae12b1b97f4d1f60370fef10105fa2faae0126114a169c64845d6126c98184015280840194909452938d166060840152608083018c905260a083019390935260c08083018b90528151808403909101815260e08301909152805192019190912061190160f01b6101008301526101028201929092526101228101919091526101420160408051601f198184030181528282528051602091820120600084529083018083525260ff871690820152606081018590526080810184905260a0016020604051602081039080840390855afa158015610fb5573d6000803e3d6000fd5b5050604051601f1901519150506001600160a01b03811615801590610feb5750876001600160a01b0316816001600160a01b0316145b6110285760405162461bcd60e51b815260206004820152600e60248201526d24a72b20a624a22fa9a4a3a722a960911b6044820152606401610694565b6001600160a01b0390811660009081526004602090815260408083208a8516808552908352928190208990555188815291928a16917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925910160405180910390a350505050505050565b6110a7336000356001600160e01b03191661110f565b6110c35760405162461bcd60e51b815260040161069490611694565b600680546001600160a01b0319166001600160a01b03831690811790915560405133907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e090600090a350565b6007546000906001600160a01b03168015801590611199575060405163b700961360e01b81526001600160a01b0382169063b7009613906111589087903090889060040161171a565b602060405180830381865afa158015611175573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906111999190611747565b806111b157506006546001600160a01b038581169116145b949350505050565b60007f8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f60006040516111eb9190611764565b6040805191829003822060208301939093528101919091527fc89efdaa54c0f20c7adf612882df0950f5a951637e0307cdcb4c672f298b8bc660608201524660808201523060a082015260c00160405160208183030381529060405280519060200120905090565b80600260008282546112659190611803565b90915550506001600160a01b03821660008181526003602090815260408083208054860190555184815260008051602061181783398151915291015b60405180910390a35050565b6001600160a01b038216600090815260036020526040812080548392906112d59084906116d0565b90915550506002805482900390556040518181526000906001600160a01b03841690600080516020611817833981519152906020016112a1565b6001600160a01b038116811461094857600080fd5b60006020828403121561133657600080fd5b813561081e8161130f565b600060208083528351808285015260005b8181101561136e57858101830151858201604001528201611352565b506000604082860101526040601f19601f8301168501019250505092915050565b600080604083850312156113a257600080fd5b82356113ad8161130f565b946020939093013593505050565b80356001600160e01b0319811681146113d357600080fd5b919050565b6000602082840312156113ea57600080fd5b61081e826113bb565b803560ff811681146113d357600080fd5b801515811461094857600080fd5b60008060006060848603121561142757600080fd5b611430846113f3565b925061143e602085016113bb565b9150604084013561144e81611404565b809150509250925092565b60008060006060848603121561146e57600080fd5b83356114798161130f565b925060208401356114898161130f565b929592945050506040919091013590565b6000602082840312156114ac57600080fd5b5035919050565b600080604083850312156114c657600080fd5b6114cf836113bb565b915060208301356114df81611404565b809150509250929050565b6000806000606084860312156114ff57600080fd5b833561150a8161130f565b925061143e602085016113f3565b6000806040838503121561152b57600080fd5b82356115368161130f565b915060208301356114df8161130f565b60008060006060848603121561155b57600080fd5b83356115668161130f565b925060208401356115768161130f565b9150611584604085016113bb565b90509250925092565b600080600080600080600060e0888a0312156115a857600080fd5b87356115b38161130f565b965060208801356115c38161130f565b955060408801359450606088013593506115df608089016113f3565b925060a0880135915060c0880135905092959891949750929550565b6000806040838503121561160e57600080fd5b611617836113f3565b9150611625602084016113bb565b90509250929050565b6000806040838503121561164157600080fd5b823561164c8161130f565b9150611625602084016113f3565b600181811c9082168061166e57607f821691505b60208210810361168e57634e487b7160e01b600052602260045260246000fd5b50919050565b6020808252600c908201526b15539055551213d49256915160a21b604082015260600190565b634e487b7160e01b600052601160045260246000fd5b8181038181111561065c5761065c6116ba565b6020808252601d908201527f45524332304d696e7461626c653a206e6f7420617574686f72697a6564000000604082015260600190565b6001600160a01b0393841681529190921660208201526001600160e01b0319909116604082015260600190565b60006020828403121561175957600080fd5b815161081e81611404565b600080835481600182811c91508083168061178057607f831692505b6020808410820361179f57634e487b7160e01b86526022600452602486fd5b8180156117b357600181146117c8576117f5565b60ff19861689528415158502890196506117f5565b60008a81526020902060005b868110156117ed5781548b8201529085019083016117d4565b505084890196505b509498975050505050505050565b8082018082111561065c5761065c6116ba56feddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3efa26469706673582212208b21ead367f6232df18a0540291ea968c19726d0081bfe5621f88fe54f60c50964736f6c63430008130033"
)


class ERC20MintableContract(Contract):
    """A web3.py Contract class for the ERC20Mintable contract."""

    abi: ABI = erc20mintable_abi
    bytecode: bytes = HexBytes(erc20mintable_bytecode)

    def __init__(self, address: ChecksumAddress | None = None) -> None:
        try:
            # Initialize parent Contract class
            super().__init__(address=address)
            self.functions = ERC20MintableContractFunctions(
                erc20mintable_abi, self.w3, address
            )

        except FallbackNotFound:
            print("Fallback function not found. Continuing...")

    # TODO: add events
    # events: ERC20ContractEvents

    functions: ERC20MintableContractFunctions

    @classmethod
    def factory(
        cls, w3: Web3, class_name: str | None = None, **kwargs: Any
    ) -> Type[Self]:
        contract = super().factory(w3, class_name, **kwargs)
        contract.functions = ERC20MintableContractFunctions(
            erc20mintable_abi, w3, None
        )

        return contract
