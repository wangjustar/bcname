import random


# 生成随机交易数据
def generate_random_transactions(num_nodes, s):
    transactions = []
    all_nodes = [chr(65 + i) for i in range(num_nodes)]  # 生成所有节点的列表
    fraud_node = 'F'
    all_nodes.append(fraud_node)
    num_selling = num_nodes - 1  # 刷单节点作为卖家的交易数，总节点数减去自身
    num_buying = num_nodes // 10  # 刷单节点作为买家的交易数，总节点数的1/10
    high_amount = random.randint(10, 100)  # 较大的交易金额
    for _ in range(s):
        buyer = random.choice(all_nodes)  # 随机选择一个节点作为买家
        all_sellers = [node for node in all_nodes if (node != buyer and node != fraud_node )]  # 去除买家自身作为卖家
        num_sellers = random.randint(1, num_nodes - 3)  # 随机选择卖家数量
        sellers = random.sample(all_sellers, num_sellers)  # 随机选择卖家
        amount = random.randint(1, 10)  # 随机生成交易金额
        transactions.append([buyer, sellers, amount])

    for _ in range(num_selling):
        sellers = random.sample(all_nodes, num_selling)  # 作为卖家，随机选择其他节点作为买家
        if fraud_node in sellers:
            sellers.remove(fraud_node)
        amount = random.randint(1, 10)  # 随机生成交易金额
        transactions.append([fraud_node, sellers, amount])

    for _ in range(num_buying):
        buyers = [fraud_node]  # 刷单节点作为买家
        sellers = random.sample([node for node in all_nodes if node != fraud_node], 1)  # 随机选择一个节点作为卖家
        amount = high_amount  # 使用较大的交易金额
        transactions.append([fraud_node, sellers, amount])

    return transactions


# 输出生成的交易数据
def print_transactions(transactions):
    for transaction in transactions:
        print(transaction)


if __name__ == "__main__":
    # 示例：生成 20 个节点的随机交易数据
    num_nodes = 20
    transactions = generate_random_transactions(num_nodes, 10)

    # 输出交易数据
    print_transactions(transactions)
