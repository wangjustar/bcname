from web3.gas_strategies.rpc import rpc_gas_price_strategy

from docs.gpt import contract
from datetime import datetime
from docs import config

w3 = contract.w3
contract3 = contract.contract3
bytes32_param = b'\x00' * 32


def create_account(username):
    new_account = w3.eth.account.create()
    address = new_account.address
    contract.registeruser(username, address)
    return new_account.key.hex(), address


def all_accounts():
    new_account = w3.eth.account.create()
    address = new_account.address
    print(new_account.key.hex())
    address = "0xA1217b89c17B767Bb515bAbE2C95F252Dc5a74A9"
    sender_address = "0x5D32F55bE205131C777173d434aA7506d592339b"
    sender_private_key = "0xc3aa19f9ea8f8981e7f038aaee1e1f479785cadadc0272b8567696381dc1f513"
    # 获取发送者账户的 nonce

    w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

    # 5. Sign tx with PK
    tx_create = w3.eth.account.sign_transaction(
        {
            "nonce": w3.eth.get_transaction_count(
                w3.to_checksum_address(sender_address)
            ),
            "gasPrice": w3.eth.generate_gas_price(),
            "gas": 21000,
            "to": w3.to_checksum_address(address),
            "value": w3.to_wei("3", "ether"),
        },
        sender_private_key
    )

    # 6. Send tx and wait for receipt
    tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Transaction successful!")
    print("新账户：", new_account.address)
    accounts = w3.eth.accounts
    print("Ganache 上的所有账户:")
    for account in accounts:
        print(account)


# 寻找符合的发送者
def find_high_active_workers(seed, x):
    current_timestamp = int(datetime.now().timestamp())
    providers = contract.getresourceswithseed(seed)
    user_activity = []
    for provider in providers:
        providerinfo = contract.getuserinfo(provider)
        days_since_registration = (current_timestamp - providerinfo[3]) / (60 * 60 * 24)
        released_task_num = providerinfo[6]
        finished_task_num = providerinfo[5]
        activity = (finished_task_num - released_task_num) / (days_since_registration + 1)
        user_activity.append({"username": provider, "activity": activity})
    user_activity.sort(key=lambda x: x["activity"], reverse=True)
    top_x_users = [user["username"] for user in user_activity[:x]]
    return top_x_users


# 形成交易合约
def make_tras_contract(receivername, seed):
    fcontract = w3.eth.contract(address=contract3.contract_address, abi=contract3.contract_abi)

    # 调用合约的 constructor 函数来部署合约实例
    tx_hash = fcontract.constructor(contract.contract1.contract_address, contract.contract2.contract_address,
                                    receivername, seed).transact(
        {'from': w3.eth.accounts[0]})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # 获取部署的合约地址
    deployed_contract_address = tx_receipt.contractAddress
    return deployed_contract_address


# 发布寻找任务
def releasetask(contract_address, title, desc, reward, autoMatch, blockNum):
    fcontract = w3.eth.contract(address=contract_address, abi=contract3.contract_abi)
    try:
        tx_hash = fcontract.functions.releasetask(title, desc, reward, autoMatch, blockNum).transact(
            {'from': w3.eth.accounts[0], 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


# 接受任务
def receivetask(contract_address, workerName):
    fcontract = w3.eth.contract(address=contract_address, abi=contract3.contract_abi)
    try:
        tx_hash = fcontract.functions.receiveTask(workerName).transact(
            {'from': w3.eth.accounts[0], 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
        estabp2p(fcontract.functions.receiverName().call(), workerName)
    except Exception as e:
        print(f"Transaction failed: {e}")


def estabp2p(receiverName, providerName):
    raise NotImplementedError("This function is not yet implemented")


# 已找到资源，自动接入
def resourcematch(seed, receiverName, providerName, title, desc, reward, blockNum):
    contract_address = make_tras_contract(receiverName, seed)
    releasetask(contract_address, title, desc, reward, False, blockNum)
    receivetask(contract_address, providerName)


def evaluatesolution(contract_address, wokername, result):
    fcontract = w3.eth.contract(address=contract_address, abi=contract3.contract_abi)
    try:
        tx_hash = fcontract.functions.evaluateSolution(wokername, result).transact(
            {'from': w3.eth.accounts[0], 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


# 寻找新的发送者
def waiting_workers(contract_address, seed):
    providers = contract.getresourceswithseed(seed)
    working_probiders = []
    fcontract = w3.eth.contract(address=contract_address, abi=contract3.contract_abi)
    list_length = contract.functions.workerListLength().call()
    result = fcontract.functions.workerList().call()
    for i in range(list_length):
        working_probiders.append(result[i].workerName)
    not_in = [item for item in providers if item not in working_probiders]
    return not_in


def finishtask(contract_address, wokername):
    fcontract = w3.eth.contract(address=contract_address, abi=contract3.contract_abi)
    try:
        tx_hash = fcontract.functions.finishTask(wokername).transact(
            {'from': w3.eth.accounts[0], 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")
