from docs.gpt import contract

web3 = contract.w3
from docs import config

# 使用 Web3.py 创建合约对象
Contract = web3.eth.contract(abi=config.Config.abi, bytecode=config.Config.bytecode)


def deploy_user_relation_contract(web3, deployer_address, seed):
    # 部署合约
    tx_hash = Contract.constructor(config.Config.contract_abi_reg, config.Config.contract_abi_agg, seed).transact(
        {"from": deployer_address})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    print(f"Contract deployed at address: {contract_address}")
    return contract_address
