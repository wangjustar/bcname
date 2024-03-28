from web3 import Web3
from docs import config

# 连接到以太坊网络
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
contract_address_reg = config.Config.contract_address_reg
contract_address_agg = config.Config.contract_address_agg
contract_address_rel = config.Config.contract_address_rel
contract_abi_reg = config.Config.contract_abi_reg
contract_abi_agg = config.Config.contract_abi_agg
contract_abi_rel = config.Config.contract_abi_rel

# 加载合约
contract1 = w3.eth.contract(address=contract_address_reg, abi=contract_abi_reg)
contract2 = w3.eth.contract(address=contract_address_agg, abi=contract_abi_agg)
contract3 = w3.eth.contract(address=contract_address_rel, abi=contract_abi_rel)


# 调用 registerUser 方法
def registeruser(username,address):
    try:
        t_hash = contract1.functions.registerUser(username).transact({
            'from': address, 'gas': 3000000, })
        # 等待交易确认
        tx_receipt = w3.eth.get_transaction_receipt(t_hash)
        print("Transaction Receipt:", tx_receipt)
    except Exception as error:
        print(f"Transaction failed: {error}")


def getuserinfo(username):
    result = None
    try:
        result = contract1.functions.getUserInfo(username).call()
    except Exception as error:
        print(f"Request failed: {error}")
    return result


# t:task状态
def dealtask(username, t,address):
    try:
        tx_hash = contract1.functions.dealTask(username, t).transact({'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


# t:完成的小任务数
def releasedtaskfinished(username, t,address):
    try:
        tx_hash = contract1.functions.releasedTaskFinished(username, t).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def updateprofile(username, profile,address):
    try:
        tx_hash = contract1.functions.updateProfile(username, profile).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def getuseraddress(username):
    result = None
    try:
        result = contract1.functions.getUserAddr(username).call()
    except Exception as error:
        print(f"Request failed: {error}")
    return result


def loginuser(username, password,address):
    try:
        tx_hash = contract1.functions.getUserAddr(username, password).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def logoutuser(username):
    try:
        contract1.functions.logotUser(username).call()
    except Exception as error:
        print(f"Request failed: {error}")


#################################################################################
def publishware(title, desc, seed, plserName, addr, blockNum, copyrightFee,address):
    try:
        tx_hash = contract2.functions.publishWare(title, desc, seed, plserName, addr, blockNum, copyrightFee).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def reportware(seed,address):
    try:
        tx_hash = contract2.functions.reportWare(seed).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def evaluateware(seed,address):
    try:
        tx_hash = contract2.functions.evaluateWare(seed).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def findresource(title, seed, esc, receiverName, contractAddress,address):
    try:
        tx_hash = contract2.functions.findResource(title, seed, esc, receiverName, contractAddress).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def provideresource(seed, providerName,address):
    try:
        tx_hash = contract2.functions.findResource(seed, providerName).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def deleteresource(seed, providerName,address):
    try:
        tx_hash = contract2.functions.deleteResource(seed, providerName).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def deletedemandmarket(seed, receiverName,address):
    try:
        tx_hash = contract2.functions.deleteDemandmarket(seed, receiverName).transact(
            {'from': address, 'gas': 3000000, })
        w3.eth.get_transaction_receipt(tx_hash)
        print("Transaction successful.")
    except Exception as e:
        print(f"Transaction failed: {e}")


def getresourceswithseed(seed):
    result = None
    try:
        result = contract2.functions.getResourcesWithSeed(seed).call()
    except Exception as error:
        print(f"Request failed: {error}")
    return result

############################################################################################
