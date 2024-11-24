from web3 import Web3
import os
from solcx import compile_files, install_solc
import json

# 安装并设置 Solidity 编译器版本
install_solc("0.8.24")  # 根据需要调整版本

class Config:
    # 智能合约地址和ABI
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    keys = {}
    default = ''
    contract_address_reg = '0x8E960A02E7DE8A83861eae437D7A8057170d0EA6'
    contract_address_agg = '0xc4D4ef68C1f29dA32b8795D3C64d3346743fc134'
    contract_address_rel = ''
    # 设置 Solidity 文件路径
    SOLIDITY_FILE = "Rel.sol"
    # 编译 Solidity 文件
    compiled_sol = compile_files([SOLIDITY_FILE], solc_version="0.8.24")

    # 获取第一个合约（如果文件中有多个合约，可根据需要调整）
    contract_id = list(compiled_sol.keys())[0]
    contract_interface = compiled_sol[contract_id]

    # 提取 ABI 和 Bytecode
    abi = contract_interface["abi"]
    bytecode = contract_interface["bin"]

    # 保存 ABI 为文件（可选）
    ABI_FILE = "YourContract_abi.json"
    with open(ABI_FILE, "w") as abi_file:
        json.dump(abi, abi_file)
    contract_abi_reg = [
        {
            "inputs": [],
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "name": "Users",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "addr",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "username",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "profile",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "registerTime",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "income",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "expand",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "reput",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "x",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "reward",
                    "type": "uint256"
                }
            ],
            "name": "dealTask",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "_reputToDeduct",
                    "type": "uint256"
                }
            ],
            "name": "deductReputation",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
                }
            ],
            "name": "getUserInfo",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "addr",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "username",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "profile",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "registerTime",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "income",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "expand",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "reput",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "_reputToAdd",
                    "type": "uint256"
                }
            ],
            "name": "increaseReputation",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "lastRestoreTime",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "_username",
                    "type": "string"
                }
            ],
            "name": "registerUser",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "restoreInterval",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "restoreReputation",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "_profile",
                    "type": "string"
                }
            ],
            "name": "updateProfile",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "_username",
                    "type": "string"
                }
            ],
            "name": "updateUsername",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    contract_abi_agg = [
        {
            "inputs": [],
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "",
                    "type": "bytes32"
                }
            ],
            "name": "Reportcount",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_complainant",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "_objectUser",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "_transContract",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "desc",
                    "type": "string"
                }
            ],
            "name": "addDispute",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
                },
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                }
            ],
            "name": "deleteDemandmarket",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                }
            ],
            "name": "deleteResource",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "bool",
                    "name": "_results",
                    "type": "bool"
                }
            ],
            "name": "evaluateWare",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "_title",
                    "type": "string"
                },
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "string",
                    "name": "_desc",
                    "type": "string"
                },
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "_contractAddress",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "ipaddr",
                    "type": "string"
                }
            ],
            "name": "findResource",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                }
            ],
            "name": "findWareBySeed",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                },
                {
                    "internalType": "bytes32",
                    "name": "",
                    "type": "bytes32"
                },
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                }
            ],
            "name": "getResourcesWithSeed",
            "outputs": [
                {
                    "internalType": "address[]",
                    "name": "",
                    "type": "address[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
                }
            ],
            "name": "isExistInDemandmarket",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
                }
            ],
            "name": "isExistInResources",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                }
            ],
            "name": "isExistInWarehouse",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "string",
                    "name": "_newIpaddr",
                    "type": "string"
                }
            ],
            "name": "modifyResource",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "string",
                    "name": "_newTitle",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "_newDesc",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "_newBlockNum",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "_newCopyrightFee",
                    "type": "uint256"
                }
            ],
            "name": "modifyWare",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "string",
                    "name": "ipiddr",
                    "type": "string"
                }
            ],
            "name": "provideResource",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "_title",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "_desc",
                    "type": "string"
                },
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "uint256",
                    "name": "_blockNum",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "_copyrightFee",
                    "type": "uint256"
                }
            ],
            "name": "pubishWare",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_id",
                    "type": "uint256"
                }
            ],
            "name": "removeDispute",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                }
            ],
            "name": "reportWare",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    contract_abi_rel = []


