from eth_account import Account
from flask import jsonify, json
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from deploy import deploy_user_relation_contract
from docs.gpt import contract
from datetime import datetime
from docs import config

w3 = contract.w3
contract2 = contract.contract2
bytes32_param = b'\x00' * 32


def is_hexadecimal(s):
    return all(c.isdigit() or c.lower() in 'abcdef' for c in s)


def verify_account_and_private_key(address, private_key):
    # 将地址转换为检验和地址
    checksum_address = w3.toChecksumAddress(address)

    # 使用私钥创建账户对象
    account = Account.from_key(private_key)

    # 获取私钥对应的账户地址
    private_key_address = account.address

    # 比较地址是否一致
    if checksum_address == private_key_address:
        return True
    else:
        return False


def is_address_in_chain(address, pvkey):
    # 检查地址是否有效
    if not w3.isAddress(address):
        return {"success": False, "error": "Invalid address"}
    if verify_account_and_private_key(address, pvkey) > 0:
        return {"success": True, "message": "Address has balance"}
    return {"success": False, "error": "Address not found in the blockchain"}


# tent wrestle direct pact rose raven joy plate away enlist truth exotic
# 仅供测试调用，由管理员账号发送以太币到新注册帐号
def create_account_local(username, private_key, address):
    # 调用注册用户函数
    sender_address = address
    sender_private_key = private_key
    if not w3.is_address(sender_address):
        return "Invalid sender address"
    w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
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
    result = contract.registeruser(username, sender_address)
    if "error" in result:
        return result["error"]
    return "success"


# 寻找符合的发送者
def find_high_active_workers(seed, x):
    current_timestamp = int(datetime.now().timestamp())
    providers = contract.getresourceswithseed(seed)
    user_activity = []
    for provider in providers:
        providerinfo = contract.getuserinfo(provider)
        days_since_registration = (current_timestamp - providerinfo[3]) / (60 * 60 * 24)
        expand = providerinfo[6]
        income = providerinfo[5]
        activity = (expand - income) / (days_since_registration + 1)
        user_activity.append({"username": provider, "activity": activity})
    user_activity.sort(key=lambda x: x["activity"], reverse=True)
    top_x_users = [user["username"] for user in user_activity[:x]]
    return top_x_users


# 形成交易合约
def make_tras_contract( seed):
    contract3_address = deploy_user_relation_contract(w3,w3.eth.accounts[0],seed)
    return contract3_address


# 发布寻找任务
def releasetask(contract_address, title, desc, reward, blockNum,ipaddr):
    try:
        contract.call_release_task(contract_address,w3.eth.accounts[0], title, desc, reward, blockNum,ipaddr)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


# 接受任务
def receivetask(contract_address,value):
    try:
        contract.call_receive_task(contract_address,w3.eth.accounts[0],value)
        print("Transaction successful.")
        estabp2p()
    except Exception as e:
        print(f"Transaction failed: {e}")


def estabp2p():
    raise NotImplementedError("This function is not yet implemented")


def evaluatesolution(contract_address,worker_address,result):
    try:
        contract.call_evaluate_solution(contract_address,w3.eth.accounts[0],worker_address,result)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


# 寻找新的发送者
def waiting_workers(contract_address, seed):
    providers = contract.getresourceswithseed(seed)
    working_probiders = []
    fcontract = contract.loadcontract(contract_address)
    list_length = contract.contract2.functions.workerListLength().call()
    result = fcontract.functions.workerList().call()
    for i in range(list_length):
        working_probiders.append(result[i].workerName)
    not_in = [item for item in providers if item not in working_probiders]
    return not_in


def finishtask(contract_address, worker_address):
    try:
        contract.call_finish_task(contract_address,worker_address)
    except Exception as e:
        print(f"Transaction failed: {e}")
