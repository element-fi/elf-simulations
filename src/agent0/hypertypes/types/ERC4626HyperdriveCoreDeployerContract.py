"""A web3.py Contract class for the ERC4626HyperdriveCoreDeployer contract.

DO NOT EDIT.  This file was generated by pypechain.  See documentation at
https://github.com/delvtech/pypechain"""

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

# methods are overriden with specific arguments instead of generic *args, **kwargs
# pylint: disable=arguments-differ

# consumers have too many opinions on line length
# pylint: disable=line-too-long


from __future__ import annotations

from typing import Any, Type, cast

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes
from typing_extensions import Self
from web3 import Web3
from web3.contract.contract import Contract, ContractConstructor, ContractFunction, ContractFunctions
from web3.exceptions import FallbackNotFound
from web3.types import ABI, BlockIdentifier, CallOverride, TxParams

from .IHyperdriveTypes import Fees, PoolConfig
from .utilities import dataclass_to_tuple, rename_returned_types

structs = {
    "Fees": Fees,
    "PoolConfig": PoolConfig,
}


class ERC4626HyperdriveCoreDeployerDeployContractFunction(ContractFunction):
    """ContractFunction for the deploy method."""

    def __call__(self, config: PoolConfig, arg2: bytes, target0: str, target1: str, target2: str, target3: str, target4: str, salt: bytes) -> ERC4626HyperdriveCoreDeployerDeployContractFunction:  # type: ignore
        clone = super().__call__(
            dataclass_to_tuple(config),
            dataclass_to_tuple(arg2),
            dataclass_to_tuple(target0),
            dataclass_to_tuple(target1),
            dataclass_to_tuple(target2),
            dataclass_to_tuple(target3),
            dataclass_to_tuple(target4),
            dataclass_to_tuple(salt),
        )
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
        """returns str."""
        # Define the expected return types from the smart contract call

        return_types = str

        # Call the function

        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        return cast(str, rename_returned_types(structs, return_types, raw_values))


class ERC4626HyperdriveCoreDeployerContractFunctions(ContractFunctions):
    """ContractFunctions for the ERC4626HyperdriveCoreDeployer contract."""

    deploy: ERC4626HyperdriveCoreDeployerDeployContractFunction

    def __init__(
        self,
        abi: ABI,
        w3: "Web3",
        address: ChecksumAddress | None = None,
        decode_tuples: bool | None = False,
    ) -> None:
        super().__init__(abi, w3, address, decode_tuples)
        self.deploy = ERC4626HyperdriveCoreDeployerDeployContractFunction.factory(
            "deploy",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="deploy",
        )


erc4626hyperdrivecoredeployer_abi: ABI = cast(
    ABI,
    [
        {
            "type": "function",
            "name": "deploy",
            "inputs": [
                {
                    "name": "_config",
                    "type": "tuple",
                    "internalType": "struct IHyperdrive.PoolConfig",
                    "components": [
                        {"name": "baseToken", "type": "address", "internalType": "contract IERC20"},
                        {"name": "vaultSharesToken", "type": "address", "internalType": "contract IERC20"},
                        {"name": "linkerFactory", "type": "address", "internalType": "address"},
                        {"name": "linkerCodeHash", "type": "bytes32", "internalType": "bytes32"},
                        {"name": "initialVaultSharePrice", "type": "uint256", "internalType": "uint256"},
                        {"name": "minimumShareReserves", "type": "uint256", "internalType": "uint256"},
                        {"name": "minimumTransactionAmount", "type": "uint256", "internalType": "uint256"},
                        {"name": "positionDuration", "type": "uint256", "internalType": "uint256"},
                        {"name": "checkpointDuration", "type": "uint256", "internalType": "uint256"},
                        {"name": "timeStretch", "type": "uint256", "internalType": "uint256"},
                        {"name": "governance", "type": "address", "internalType": "address"},
                        {"name": "feeCollector", "type": "address", "internalType": "address"},
                        {"name": "sweepCollector", "type": "address", "internalType": "address"},
                        {
                            "name": "fees",
                            "type": "tuple",
                            "internalType": "struct IHyperdrive.Fees",
                            "components": [
                                {"name": "curve", "type": "uint256", "internalType": "uint256"},
                                {"name": "flat", "type": "uint256", "internalType": "uint256"},
                                {"name": "governanceLP", "type": "uint256", "internalType": "uint256"},
                                {"name": "governanceZombie", "type": "uint256", "internalType": "uint256"},
                            ],
                        },
                    ],
                },
                {"name": "", "type": "bytes", "internalType": "bytes"},
                {"name": "_target0", "type": "address", "internalType": "address"},
                {"name": "_target1", "type": "address", "internalType": "address"},
                {"name": "_target2", "type": "address", "internalType": "address"},
                {"name": "_target3", "type": "address", "internalType": "address"},
                {"name": "_target4", "type": "address", "internalType": "address"},
                {"name": "_salt", "type": "bytes32", "internalType": "bytes32"},
            ],
            "outputs": [{"name": "", "type": "address", "internalType": "address"}],
            "stateMutability": "nonpayable",
        }
    ],
)
# pylint: disable=line-too-long
erc4626hyperdrivecoredeployer_bytecode = HexStr(
    "0x608060405234801561001057600080fd5b50611f4d806100206000396000f3fe60806040523480156200001157600080fd5b50600436106200002e5760003560e01c8063ed871fd71462000033575b600080fd5b6200004a6200004436600462000253565b62000066565b6040516001600160a01b03909116815260200160405180910390f35b6040805133602082015290810182905260009060600160405160208183030381529060405280519060200120898888888888604051620000a690620000e6565b620000b796959493929190620003f4565b8190604051809103906000f5905080158015620000d8573d6000803e3d6000fd5b509998505050505050505050565b6119e6806200053283390190565b634e487b7160e01b600052604160045260246000fd5b6040516101c0810167ffffffffffffffff81118282101715620001315762000131620000f4565b60405290565b80356001600160a01b03811681146200014f57600080fd5b919050565b6000608082840312156200016757600080fd5b6040516080810181811067ffffffffffffffff821117156200018d576200018d620000f4565b8060405250809150823581526020830135602082015260408301356040820152606083013560608201525092915050565b600082601f830112620001d057600080fd5b813567ffffffffffffffff80821115620001ee57620001ee620000f4565b604051601f8301601f19908116603f01168101908282118183101715620002195762000219620000f4565b816040528381528660208588010111156200023357600080fd5b836020870160208301376000602085830101528094505050505092915050565b600080600080600080600080888a036103008112156200027257600080fd5b610220808212156200028357600080fd5b6200028d6200010a565b91506200029a8b62000137565b8252620002aa60208c0162000137565b6020830152620002bd60408c0162000137565b604083015260608b0135606083015260808b0135608083015260a08b013560a083015260c08b013560c083015260e08b013560e0830152610100808c01358184015250610120808c013581840152506101406200031c818d0162000137565b90830152610160620003308c820162000137565b90830152610180620003448c820162000137565b908301526101a0620003598d8d830162000154565b9083015290985089013567ffffffffffffffff8111156200037957600080fd5b620003878b828c01620001be565b975050620003996102408a0162000137565b9550620003aa6102608a0162000137565b9450620003bb6102808a0162000137565b9350620003cc6102a08a0162000137565b9250620003dd6102c08a0162000137565b91506102e089013590509295985092959890939650565b86516001600160a01b031681526102c0810160208801516200042160208401826001600160a01b03169052565b5060408801516200043d60408401826001600160a01b03169052565b50606088015160608301526080880151608083015260a088015160a083015260c088015160c083015260e088015160e083015261010080890151818401525061012080890151818401525061014080890151620004a4828501826001600160a01b03169052565b5050610160888101516001600160a01b0390811691840191909152610180808a01518216908401526101a09889015180519984019990995260208901516101c084015260408901516101e084015260609098015161020083015295871661022082015293861661024085015291851661026084015284166102808301529092166102a0909201919091529056fe6102e06040523480156200001257600080fd5b50604051620019e6380380620019e683398101604081905262000035916200055b565b6001600081905586516001600160a01b0390811660809081526020808a018051841660a0908152928b01516101a0908152928b01516101c05260c0808c01516101e052610100808d015190915260e0808d01519052610120808d0151909152928b0180515190935282519091015161014090815282516040908101516101609081529351606090810151610180908152918d01518616610200528c015161022052908b0151600a80549186166001600160a01b0319928316179055928b0151600880549186169185169190911790558a01516009805491851691909316179091558188166102405281871661026052818616610280528185166102a0528184166102c0525188516200014a9392169162000156565b5050505050506200071a565b604080516001600160a01b038416602482015260448082018490528251808303909101815260649091019091526020810180516001600160e01b0390811663095ea7b360e01b17909152620001b090859083906200022216565b6200021c57604080516001600160a01b038516602482015260006044808301919091528251808303909101815260649091019091526020810180516001600160e01b0390811663095ea7b360e01b1790915262000210918691620002d316565b6200021c8482620002d3565b50505050565b6000806000846001600160a01b031684604051620002419190620006c5565b6000604051808303816000865af19150503d806000811462000280576040519150601f19603f3d011682016040523d82523d6000602084013e62000285565b606091505b5091509150818015620002b3575080511580620002b3575080806020019051810190620002b39190620006f6565b8015620002ca57506000856001600160a01b03163b115b95945050505050565b6000620002ea6001600160a01b0384168362000346565b9050805160001415801562000312575080806020019051810190620003109190620006f6565b155b156200034157604051635274afe760e01b81526001600160a01b03841660048201526024015b60405180910390fd5b505050565b606062000356838360006200035d565b9392505050565b606081471015620003845760405163cd78605960e01b815230600482015260240162000338565b600080856001600160a01b03168486604051620003a29190620006c5565b60006040518083038185875af1925050503d8060008114620003e1576040519150601f19603f3d011682016040523d82523d6000602084013e620003e6565b606091505b509092509050620003f986838362000403565b9695505050505050565b6060826200041c57620004168262000467565b62000356565b81511580156200043457506001600160a01b0384163b155b156200045f57604051639996b31560e01b81526001600160a01b038516600482015260240162000338565b508062000356565b805115620004785780518082602001fd5b604051630a12f52160e11b815260040160405180910390fd5b6040516101c081016001600160401b0381118282101715620004c357634e487b7160e01b600052604160045260246000fd5b60405290565b80516001600160a01b0381168114620004e157600080fd5b919050565b600060808284031215620004f957600080fd5b604051608081016001600160401b03811182821017156200052a57634e487b7160e01b600052604160045260246000fd5b8060405250809150825181526020830151602082015260408301516040820152606083015160608201525092915050565b6000806000806000808688036102c08112156200057757600080fd5b610220808212156200058857600080fd5b6200059262000491565b91506200059f89620004c9565b8252620005af60208a01620004c9565b6020830152620005c260408a01620004c9565b6040830152606089015160608301526080890151608083015260a089015160a083015260c089015160c083015260e089015160e0830152610100808a01518184015250610120808a0151818401525061014062000621818b01620004c9565b90830152610160620006358a8201620004c9565b90830152610180620006498a8201620004c9565b908301526101a06200065e8b8b8301620004e6565b818401525081975062000673818a01620004c9565b96505050620006866102408801620004c9565b9350620006976102608801620004c9565b9250620006a86102808801620004c9565b9150620006b96102a08801620004c9565b90509295509295509295565b6000825160005b81811015620006e85760208186018101518583015201620006cc565b506000920191825250919050565b6000602082840312156200070957600080fd5b815180151581146200035657600080fd5b60805160a05160c05160e05161010051610120516101405161016051610180516101a0516101c0516101e05161020051610220516102405161026051610280516102a0516102c0516111996200084d60003960008181610657015281816107ec0152610a4701526000818161059c015281816107bc0152818161084a01526109e501526000818161053501528181610a1b0152610a72015260008181610623015281816106c301526107590152600081816101e4015281816103a601528181610693015281816106f5015281816107270152818161078d0152818161081f0152818161087b015281816109b30152610a9b015260005050600050506000505060005050600050506000505060005050600050506000505060005050600050506000505060005050600050506111996000f3fe6080604052600436106101cd5760003560e01c80639cd241af116100f7578063d899e11211610095578063e4af29d111610064578063e4af29d1146102dd578063eac3e79914610611578063f3f7070714610645578063f698da2514610679576101cd565b8063d899e1121461058a578063dbbe8070146105be578063ded06231146105d1578063e44808bc146105f1576101cd565b8063a6e8a859116100d1578063a6e8a85914610523578063ab033ea9146102dd578063cba2e58d14610557578063cbc134341461056a576101cd565b80639cd241af14610503578063a22cb465146104b0578063a42dce80146102dd576101cd565b806330adf81f1161016f5780634ed2d6ac1161013e5780634ed2d6ac146104955780637180c8ca146104b057806377d05ff4146104d05780639032c726146104e3576101cd565b806330adf81f1461040e5780633e691db914610442578063414f826d146104625780634c2ac1d914610482576101cd565b806317fad7fc116101ab57806317fad7fc146103545780631c0f12b61461037457806321b57d531461039457806329b23fc1146103e0576101cd565b806301681a62146102dd57806302329a29146102ff578063074a6de91461031a575b3480156101d957600080fd5b5060003660606000807f00000000000000000000000000000000000000000000000000000000000000006001600160a01b0316858560405161021c929190610b71565b600060405180830381855af49150503d8060008114610257576040519150601f19603f3d011682016040523d82523d6000602084013e61025c565b606091505b5091509150811561028057604051638bb0a34b60e01b815260040160405180910390fd5b600061028b82610b81565b90506001600160e01b03198116636e64089360e11b146102ad57815160208301fd5b8151600319810160048401908152926102ce91810160200190602401610bf2565b80519650602001945050505050f35b3480156102e957600080fd5b506102fd6102f8366004610cb7565b61068e565b005b34801561030b57600080fd5b506102fd6102f8366004610cf0565b34801561032657600080fd5b5061033a610335366004610d1d565b6106bb565b604080519283526020830191909152015b60405180910390f35b34801561036057600080fd5b506102fd61036f366004610db9565b6106f0565b34801561038057600080fd5b506102fd61038f366004610e4e565b610722565b3480156103a057600080fd5b506103c87f000000000000000000000000000000000000000000000000000000000000000081565b6040516001600160a01b03909116815260200161034b565b3480156103ec57600080fd5b506104006103fb366004610e96565b610752565b60405190815260200161034b565b34801561041a57600080fd5b506104007f65619c8664d6db8aae8c236ad19598696159942a4245b23b45565cc18e97367381565b34801561044e57600080fd5b5061040061045d366004610ef0565b610786565b34801561046e57600080fd5b506102fd61047d366004610f2d565b6107b7565b610400610490366004610f4f565b6107e5565b3480156104a157600080fd5b506102fd61038f366004610fb3565b3480156104bc57600080fd5b506102fd6104cb366004610ffd565b61081a565b6104006104de366004610d1d565b610843565b3480156104ef57600080fd5b506102fd6104fe366004611032565b610876565b34801561050f57600080fd5b506102fd61051e3660046110b0565b6109ae565b34801561052f57600080fd5b506103c87f000000000000000000000000000000000000000000000000000000000000000081565b61033a610565366004610e96565b6109dd565b34801561057657600080fd5b5061033a610585366004610d1d565b610a13565b34801561059657600080fd5b506103c87f000000000000000000000000000000000000000000000000000000000000000081565b61033a6105cc366004610e96565b610a3f565b3480156105dd57600080fd5b506104006105ec366004610e96565b610a6b565b3480156105fd57600080fd5b506102fd61060c3660046110e8565b610a96565b34801561061d57600080fd5b506103c87f000000000000000000000000000000000000000000000000000000000000000081565b34801561065157600080fd5b506103c87f000000000000000000000000000000000000000000000000000000000000000081565b34801561068557600080fd5b50610400610ac7565b6106b77f0000000000000000000000000000000000000000000000000000000000000000610b55565b5050565b6000806106e77f0000000000000000000000000000000000000000000000000000000000000000610b55565b50935093915050565b6107197f0000000000000000000000000000000000000000000000000000000000000000610b55565b50505050505050565b61074b7f0000000000000000000000000000000000000000000000000000000000000000610b55565b5050505050565b600061077d7f0000000000000000000000000000000000000000000000000000000000000000610b55565b50949350505050565b60006107b17f0000000000000000000000000000000000000000000000000000000000000000610b55565b50919050565b6107e07f0000000000000000000000000000000000000000000000000000000000000000610b55565b505050565b60006108107f0000000000000000000000000000000000000000000000000000000000000000610b55565b5095945050505050565b6107e07f0000000000000000000000000000000000000000000000000000000000000000610b55565b600061086e7f0000000000000000000000000000000000000000000000000000000000000000610b55565b509392505050565b6000807f00000000000000000000000000000000000000000000000000000000000000006001600160a01b03166108ab610ac7565b60405160248101919091527f65619c8664d6db8aae8c236ad19598696159942a4245b23b45565cc18e97367360448201526001600160a01b03808c1660648301528a16608482015288151560a482015260c4810188905260ff871660e4820152610104810186905261012481018590526101440160408051601f198184030181529181526020820180516001600160e01b03166314e5f07b60e01b179052516109549190611147565b600060405180830381855af49150503d806000811461098f576040519150601f19603f3d011682016040523d82523d6000602084013e610994565b606091505b5091509150816109a657805160208201fd5b805160208201f35b6109d77f0000000000000000000000000000000000000000000000000000000000000000610b55565b50505050565b600080610a097f0000000000000000000000000000000000000000000000000000000000000000610b55565b5094509492505050565b6000806106e77f0000000000000000000000000000000000000000000000000000000000000000610b55565b600080610a097f0000000000000000000000000000000000000000000000000000000000000000610b55565b600061077d7f0000000000000000000000000000000000000000000000000000000000000000610b55565b610abf7f0000000000000000000000000000000000000000000000000000000000000000610b55565b505050505050565b60408051808201825260018152603160f81b60209182015281517f2aef22f9d7df5f9d21c56d14029233f3fdaa91917727e1eb68e504d27072d6cd818301527fc89efdaa54c0f20c7adf612882df0950f5a951637e0307cdcb4c672f298b8bc681840152466060820152306080808301919091528351808303909101815260a0909101909252815191012090565b6060600080836001600160a01b03166000366040516109549291905b8183823760009101908152919050565b805160208201516001600160e01b03198082169291906004831015610bb05780818460040360031b1b83161693505b505050919050565b634e487b7160e01b600052604160045260246000fd5b60005b83811015610be9578181015183820152602001610bd1565b50506000910152565b600060208284031215610c0457600080fd5b815167ffffffffffffffff80821115610c1c57600080fd5b818401915084601f830112610c3057600080fd5b815181811115610c4257610c42610bb8565b604051601f8201601f19908116603f01168101908382118183101715610c6a57610c6a610bb8565b81604052828152876020848701011115610c8357600080fd5b610c94836020830160208801610bce565b979650505050505050565b6001600160a01b0381168114610cb457600080fd5b50565b600060208284031215610cc957600080fd5b8135610cd481610c9f565b9392505050565b80358015158114610ceb57600080fd5b919050565b600060208284031215610d0257600080fd5b610cd482610cdb565b6000606082840312156107b157600080fd5b600080600060608486031215610d3257600080fd5b8335925060208401359150604084013567ffffffffffffffff811115610d5757600080fd5b610d6386828701610d0b565b9150509250925092565b60008083601f840112610d7f57600080fd5b50813567ffffffffffffffff811115610d9757600080fd5b6020830191508360208260051b8501011115610db257600080fd5b9250929050565b60008060008060008060808789031215610dd257600080fd5b8635610ddd81610c9f565b95506020870135610ded81610c9f565b9450604087013567ffffffffffffffff80821115610e0a57600080fd5b610e168a838b01610d6d565b90965094506060890135915080821115610e2f57600080fd5b50610e3c89828a01610d6d565b979a9699509497509295939492505050565b60008060008060808587031215610e6457600080fd5b843593506020850135610e7681610c9f565b92506040850135610e8681610c9f565b9396929550929360600135925050565b60008060008060808587031215610eac57600080fd5b843593506020850135925060408501359150606085013567ffffffffffffffff811115610ed857600080fd5b610ee487828801610d0b565b91505092959194509250565b600060208284031215610f0257600080fd5b813567ffffffffffffffff811115610f1957600080fd5b610f2584828501610d0b565b949350505050565b60008060408385031215610f4057600080fd5b50508035926020909101359150565b600080600080600060a08688031215610f6757600080fd5b85359450602086013593506040860135925060608601359150608086013567ffffffffffffffff811115610f9a57600080fd5b610fa688828901610d0b565b9150509295509295909350565b60008060008060808587031215610fc957600080fd5b843593506020850135610fdb81610c9f565b9250604085013591506060850135610ff281610c9f565b939692955090935050565b6000806040838503121561101057600080fd5b823561101b81610c9f565b915061102960208401610cdb565b90509250929050565b600080600080600080600060e0888a03121561104d57600080fd5b873561105881610c9f565b9650602088013561106881610c9f565b955061107660408901610cdb565b945060608801359350608088013560ff8116811461109357600080fd5b9699959850939692959460a0840135945060c09093013592915050565b6000806000606084860312156110c557600080fd5b8335925060208401356110d781610c9f565b929592945050506040919091013590565b600080600080600060a0868803121561110057600080fd5b85359450602086013561111281610c9f565b9350604086013561112281610c9f565b925060608601359150608086013561113981610c9f565b809150509295509295909350565b60008251611159818460208701610bce565b919091019291505056fea2646970667358221220df83c1c67ddfbb1c741090baf8a0aaff066b2e016d20bdd8200387da2ffe15e364736f6c63430008140033a264697066735822122000882ef16cf4a226dca73e247421292b910b75cef42d69954ca009330fe95b5d64736f6c63430008140033"
)


class ERC4626HyperdriveCoreDeployerContract(Contract):
    """A web3.py Contract class for the ERC4626HyperdriveCoreDeployer contract."""

    abi: ABI = erc4626hyperdrivecoredeployer_abi
    bytecode: bytes = HexBytes(erc4626hyperdrivecoredeployer_bytecode)

    def __init__(self, address: ChecksumAddress | None = None) -> None:
        try:
            # Initialize parent Contract class
            super().__init__(address=address)
            self.functions = ERC4626HyperdriveCoreDeployerContractFunctions(erc4626hyperdrivecoredeployer_abi, self.w3, address)  # type: ignore

        except FallbackNotFound:
            print("Fallback function not found. Continuing...")

    functions: ERC4626HyperdriveCoreDeployerContractFunctions

    @classmethod
    def constructor(cls) -> ContractConstructor:  # type: ignore
        """Creates a transaction with the contract's constructor function.

        Parameters
        ----------

        w3 : Web3
            A web3 instance.
        account : LocalAccount
            The account to use to deploy the contract.

        Returns
        -------
        Self
            A deployed instance of the contract.

        """

        return super().constructor()

    @classmethod
    def deploy(cls, w3: Web3, account: LocalAccount | ChecksumAddress) -> Self:
        """Deploys and instance of the contract.

        Parameters
        ----------
        w3 : Web3
            A web3 instance.
        account : LocalAccount
            The account to use to deploy the contract.

        Returns
        -------
        Self
            A deployed instance of the contract.
        """
        deployer = cls.factory(w3=w3)
        constructor_fn = deployer.constructor()

        # if an address is supplied, try to use a web3 default account
        if isinstance(account, str):
            tx_hash = constructor_fn.transact({"from": account})
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            deployed_contract = deployer(address=tx_receipt.contractAddress)  # type: ignore
            return deployed_contract

        # otherwise use the account provided.
        deployment_tx = constructor_fn.build_transaction()
        current_nonce = w3.eth.get_transaction_count(account.address)
        deployment_tx.update({"nonce": current_nonce})

        # Sign the transaction with local account private key
        signed_tx = account.sign_transaction(deployment_tx)

        # Send the signed transaction and wait for receipt
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        deployed_contract = deployer(address=tx_receipt.contractAddress)  # type: ignore
        return deployed_contract

    @classmethod
    def factory(cls, w3: Web3, class_name: str | None = None, **kwargs: Any) -> Type[Self]:
        """Deploys and instance of the contract.

        Parameters
        ----------
        w3 : Web3
            A web3 instance.
        class_name: str | None
            The instance class name.

        Returns
        -------
        Self
            A deployed instance of the contract.
        """
        contract = super().factory(w3, class_name, **kwargs)
        contract.functions = ERC4626HyperdriveCoreDeployerContractFunctions(erc4626hyperdrivecoredeployer_abi, w3, None)

        return contract
