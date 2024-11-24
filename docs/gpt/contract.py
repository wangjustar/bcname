import json
import time

from web3 import Web3
from docs import config

# 连接到以太坊网络
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
contract_address_reg = config.Config.contract_address_reg
contract_address_agg = config.Config.contract_address_agg
contract_address_rel = config.Config.contract_address_rel
contract_abi_reg = config.Config.contract_abi_reg
contract_abi_agg = config.Config.contract_abi_agg

# 加载合约
contract1 = w3.eth.contract(address=contract_address_reg, abi=contract_abi_reg)
contract2 = w3.eth.contract(address=contract_address_agg, abi=contract_abi_agg)


# 调用 registerUser 方法
def registeruser(username, address):
    try:
        t_hash = contract1.functions.registerUser(username).transact(
            {'gas': 3000000, 'from': address})
        # 等待交易确认
        tx_receipt = None
        max_attempts = 60  # 设置最大尝试次数为60次
        attempts = 0
        while tx_receipt is None and attempts < max_attempts:
            tx_receipt = w3.eth.get_transaction_receipt(t_hash)
            attempts += 1
            time.sleep(1)  # 等待1秒钟再次尝试获取交易收据
        if tx_receipt is None:
            print("获取交易收据超时")
            return {"error": "获取交易收据超时", "type": "TimeoutError"}
        else:
            return {"success": True}
    except Exception as error:
        return {"error": error.args[0]}


def getuserinfo(address):
    try:
        result = contract1.functions.getUserInfo(address).call()
    except Exception as error:
        return {"error": error.args[0]}
    return result


def updateprofile(profile, address):
    try:
        tx_hash = contract1.functions.updateProfile(profile).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as error:
        return {"error": error.args[0]}


def updateusername(username, address):
    try:
        tx_hash = contract1.functions.updateUsername(username).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as error:
        return {"error": error.args[0]}


def deductreputation(address, opaddr, reputvalue):
    try:
        tx_hash = contract1.functions.deductReputation(opaddr, reputvalue).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as error:
        return {"error": error.args[0]}


def increasereputation(address, opaddr, reputvalue):
    try:
        tx_hash = contract1.functions.increaseReputation(opaddr, reputvalue).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as error:
        return {"error": error.args[0]}


def restorereputation(address):
    try:
        tx_hash = contract1.functions.restoreReputation().transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as error:
        return {"error": error.args[0]}


#################################################################################
# 读取 Warehouse 数据并返回 JSON
def get_warehouse_data():
    try:
        # 获取 Warehouse 数组的长度
        length = contract2.functions.getWarehouseLength().call()

        # 初始化结果列表
        warehouse_data = []

        # 遍历 Warehouse 数组并读取数据
        for i in range(length):
            ware = contract2.functions.Warehouse(i).call()
            ware_data = {
                "title": ware[0],
                "desc": ware[1],
                "seed": ware[2].hex(),  # bytes32 转为十六进制字符串
                "publisherAddr": ware[3],
                "status": ware[4],
                "blockNum": ware[5],
                "copyrightFee": ware[6],
            }
            warehouse_data.append(ware_data)

        # 将结果转换为 JSON 并返回
        return json.dumps(warehouse_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)


def publishware(title, desc, seed, blockNum, copyrightFee, address):
    try:
        tx_hash = contract2.functions.pubishWare(title, desc, Web3.to_bytes(w3.keccak(text=seed)),
                                                 blockNum, copyrightFee).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def modifyware(seed, title, desc, blockNum, copyrightFee, address):
    try:
        tx_hash = contract2.functions.modifyWare(title, desc, Web3.to_bytes(w3.keccak(text=seed)),
                                                 blockNum, copyrightFee).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def reportware(seed, address):
    try:
        tx_hash = contract2.functions.reportWare(seed).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def evaluateware(seed, address, result):
    try:
        tx_hash = contract2.functions.evaluateWare(seed, result).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def provideresource(seed, address, ipaddr):
    try:
        tx_hash = contract2.functions.provideResource(seed, ipaddr).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def deleteresource(seed, providerName, address):
    try:
        tx_hash = contract2.functions.deleteResource(seed, providerName).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def modifyresource(seed, ipaddr, address):
    try:
        tx_hash = contract2.functions.modifyResource(seed, ipaddr).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def deletedemandmarket(seed, address):
    try:
        tx_hash = contract2.functions.deleteDemandmarket(seed).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def getresourceswithseed(seed):
    try:
        result = contract2.functions.getResourcesWithSeed(seed).call()
    except Exception as error:
        return {"error": error.args[0]}
    return result


def adddispute(complainant, objectuser, transcontract, desc, address):
    try:
        tx_hash = contract2.functions.addDispute(complainant, objectuser, transcontract, desc).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def removedispute(id, address):
    try:
        tx_hash = contract2.functions.removeDispute(id).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


############################################################################################

def loadcontract(contract_address):
    # 加载部署后的合约实例
    deployed_contract = w3.eth.contract(address=contract_address, abi=config.Config.abi)
    return deployed_contract


def call_initial_seed(contract_address, deployer_address, seed):
    contract = loadcontract(contract_address)
    try:
        tx_hash = contract.functions.initialSeed(seed).transact({"from": deployer_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Seed initialized successfully.")
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def call_ware_match(contract_address, deployer_address, seed):
    contract = loadcontract(contract_address)
    try:
        tx_hash = contract.functions.WareMatch(seed).transact({"from": deployer_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Ware matched successfully.")
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def call_add_refer(contract_address, deployer_address, seed, refer_addr):
    contract = loadcontract(contract_address)
    try:
        tx_hash = contract.functions.addRefer(seed, refer_addr).transact({"from": deployer_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Refer added successfully.")
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def call_release_task(contract_address, deployer_address, title, desc, reward, block_num, ipaddr):
    contract = loadcontract(contract_address)
    try:
        tx_hash = contract.functions.releaseTask(title, desc, reward, block_num, ipaddr).transact(
            {"from": deployer_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Task released successfully.")
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def call_get_task_info(contract_address):
    contract = loadcontract(contract_address)
    try:
        task_info = contract.functions.getTaskInfo().call()
        print("Task information retrieved successfully.")
        return {"success": True, "data": task_info}
    except Exception as e:
        return {"error": e.args[0]}


def call_receive_task(contract_address, deployer_address, value):
    contract = loadcontract(contract_address)
    try:
        tx_hash = contract.functions.receiveTask().transact(
            {"from": deployer_address, "value": value, 'gas': 3000000, })
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Task received successfully.")
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def call_finish_task(contract_address, worker_address):
    contract = loadcontract(contract_address)
    try:
        tx_hash = contract.functions.finishTask().transact({"from": worker_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Task finished successfully.")
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def call_evaluate_solution(contract_address, deployer_address, worker_addr, result):
    contract = loadcontract(contract_address)
    try:
        tx_hash = contract.functions.evaluateSolution(worker_addr, result).transact({"from": deployer_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Solution evaluated successfully.")
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}


def call_report_trans(contract_address, reporter_address, target_addr, desc):
    contract = loadcontract(contract_address)
    try:
        tx_hash = contract.functions.reportTrans(target_addr, desc).transact({"from": reporter_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Transaction dispute reported successfully.")
        return {"success": True}
    except Exception as e:
        return {"error": e.args[0]}
