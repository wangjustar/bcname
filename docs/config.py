class Config:
    # 智能合约地址和ABI
    contract_address_reg = '0x6ef85E4fB5F40207FAE652B5d4029f3634f0145c'
    contract_address_agg = '0x3349Fb249b2C8D59c2D53C81d334835B488f3f11'
    contract_address_rel = '0xd9145CCE52D386f254917e481eB44e9943F39138'
    contract_abi_reg = [
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
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
                    "name": "activeTaskNum",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "finishedTaskNum",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "releasedTaskNum",
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
                }
            ],
            "name": "containsAddr",
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
                    "internalType": "string",
                    "name": "username",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "x",
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
                    "internalType": "string",
                    "name": "_username",
                    "type": "string"
                }
            ],
            "name": "getUserAddr",
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
                    "name": "activeTaskNum",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "finishedTaskNum",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "releasedTaskNum",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "name": "loginUsers",
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
            "inputs": [
                {
                    "internalType": "string",
                    "name": "_username",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "_tasknum",
                    "type": "uint256"
                }
            ],
            "name": "releasedTaskFinished",
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
                },
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
        }
    ]
    contract_abi_agg = [
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
                    "internalType": "bytes32",
                    "name": "_seed",
                    "type": "bytes32"
                },
                {
                    "internalType": "string",
                    "name": "_receiverName",
                    "type": "string"
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
                },
                {
                    "internalType": "string",
                    "name": "_providerName",
                    "type": "string"
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
                    "internalType": "string",
                    "name": "_receiverName",
                    "type": "string"
                },
                {
                    "internalType": "address",
                    "name": "_contractAddress",
                    "type": "address"
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
                    "internalType": "string",
                    "name": "",
                    "type": "string"
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
                    "internalType": "string[]",
                    "name": "",
                    "type": "string[]"
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
                    "name": "_receiverName",
                    "type": "string"
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
                    "internalType": "string",
                    "name": "_providerName",
                    "type": "string"
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
                    "name": "_providerName",
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
                    "internalType": "string",
                    "name": "_plserName",
                    "type": "string"
                },
                {
                    "internalType": "address",
                    "name": "_addr",
                    "type": "address"
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
