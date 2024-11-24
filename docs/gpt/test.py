import math
from math import log

import networkx as nx
import matplotlib.pyplot as plt
from net import generate_random_transactions


def calculate_out_edge_weight_sum(graph, node):
    out_edges = graph.out_edges(node, data=True)
    weight_sum = sum(data['amount'] for _, _, data in out_edges if 'amount' in data)
    return weight_sum


def calculate_in_edge_weight_sum(graph, node):
    in_edges = graph.in_edges(node, data=True)
    weight_sum = sum(data['amount'] for _, _, data in in_edges if 'amount' in data)
    return weight_sum


def find_lowest_suspiciousness_node(scores):
    return min(scores, key=scores.get)


def calculate_suspiciousness(graph):
    suspiciousness_scores = {}

    for node in graph.nodes():
        out_degree = graph.out_degree(node)
        in_degree = graph.in_degree(node)
        edge_weights_sum_out = calculate_out_edge_weight_sum(graph, node)
        edge_weights_sum_in = calculate_in_edge_weight_sum(graph, node)

        # Weighted sum of out_degree, in_degree, and edge_weights_sum
        # You can adjust the weights for each factor according to your preference
        x = edge_weights_sum_out / len(graph.nodes())
        score1 = 1 - math.exp(-x) + 1 / log(out_degree + 5)
        y = edge_weights_sum_in / len(graph.nodes())
        score2 = 1 - math.exp(-y) + 1 / log(in_degree + 5)
        score = score2 + score1
        print(node, score)
        suspiciousness_scores[node] = score
    return suspiciousness_scores


def add_transaction(graph, buyer, sellers, amount):
    # 添加买家节点
    graph.add_node(buyer)

    # 添加卖家节点并添加边
    for seller in sellers:
        graph.add_node(seller)
        if graph.has_edge(buyer, seller):
            graph[buyer][seller]['amount'] += amount
        elif graph.has_edge(seller, buyer):
            if graph[seller][buyer]['amount'] == amount:
                graph.remove_edge(seller, buyer)
            else:
                # 否则根据方向和长度进行合并
                if amount > graph[seller][buyer]['amount']:
                    graph.remove_edge(seller, buyer)
                    graph.add_edge(buyer, seller, amount=amount)
                else:
                    graph[seller][buyer]['amount'] -= amount

        else:
            graph.add_edge(buyer, seller, amount=amount)


def construct_directed_graph(transactions):
    graph = nx.DiGraph()
    for transaction in transactions:
        buyer = transaction[0]
        sellers = transaction[1]
        amount = transaction[2]
        add_transaction(graph, buyer, sellers, amount)
    return graph


def draw_directed_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=12, font_weight="bold")
    edge_labels = nx.get_edge_attributes(graph, 'amount')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()


def find_edges_of_most_suspicious_node(graph, scores):
    max_suspiciousness = max(scores.values())
    most_suspicious_nodes = [node for node, score in scores.items() if score == max_suspiciousness]
    edge_list = []
    for node in most_suspicious_nodes:
        for neighbor in graph.successors(node):
            edge_list.append((node, neighbor))
    return edge_list


def calculate_average_suspiciousness(scores):
    print("avg", sum(scores.values()) / len(scores))
    return sum(scores.values()) / len(scores)


# 示例交易数据
runs = 50
transactions = []
average_suspiciousness_list = []
iteration_number_list = []
first_decrease_iterations = []  # 存储首次下降的迭代次数
f_removal_iterations = []  # 存储节点 F 被移除的迭代次数
run_indices = list(range(1, runs + 1))  # 横坐标为运行次数

if __name__ == "__main__":
    # 构建有向图
    for run in range(runs):
        print(f"运行 {run + 1}/{runs} 中...")
        transactions = generate_random_transactions(50, 50000)
        graph = construct_directed_graph(transactions)
        # scores = calculate_suspiciousness(graph)
        # print(scores)
        # el = find_edges_of_most_suspicious_node(graph, scores)
        # print(el)
        #
        # # 绘制有向图
        # draw_directed_graph(graph)
        scores = calculate_suspiciousness(graph)
        lgn = (len(graph.nodes()))
        prev_average_suspiciousness = None  # 记录上一轮的平均可疑性分数
        iteration = 0  # 当前迭代次数
        first_decrease_iteration = None
        f_removal_iteration = None
        while len(graph.nodes()) > 1:
            # Calculate average suspiciousness
            average_suspiciousness = calculate_average_suspiciousness(scores)
            average_suspiciousness_list.append(average_suspiciousness)
            iteration_number_list.append(lgn - len(graph.nodes()))
            if (
                    prev_average_suspiciousness is not None
                    and average_suspiciousness < prev_average_suspiciousness
                    and first_decrease_iteration is None
            ):
                first_decrease_iteration = iteration
                if first_decrease_iteration is not None:
                    if first_decrease_iteration < 40:
                        first_decrease_iteration = None


            prev_average_suspiciousness = average_suspiciousness

            # Remove the node with the lowest suspiciousness score
            lowest_suspiciousness_node = find_lowest_suspiciousness_node(scores)
            if lowest_suspiciousness_node == "F" and f_removal_iteration is None:
                f_removal_iteration = iteration
            graph.remove_node(lowest_suspiciousness_node)

            # Recalculate suspiciousness scores for the updated graph
            scores = calculate_suspiciousness(graph)
            iteration += 1
        # plt.plot(iteration_number_list, average_suspiciousness_list, marker='o')
        # plt.xlabel('Iteration Number')
        # plt.ylabel('Average Suspiciousness')
        # plt.title('Average Suspiciousness vs Iteration Number')
        # plt.grid(True)
        # plt.show()

            # 输出首次下降迭代次数和 F 被移除时的迭代次数
        print("首次出现下降的迭代次数:", first_decrease_iteration)
        if f_removal_iteration is None:
            f_removal_iteration = 49
        print("节点 F 被移除时的迭代次数:", f_removal_iteration)
        first_decrease_iterations.append(first_decrease_iteration)
        f_removal_iterations.append(f_removal_iteration)


    # Plotting the results



    plt.plot(run_indices, f_removal_iterations, marker='o', label='F Removal Iteration', color='red')
    plt.plot(run_indices, first_decrease_iterations, marker='x', label='First Decrease Iteration', color='blue')
    plt.ylim(0, max(max(first_decrease_iterations), max(f_removal_iterations), 1))
    plt.xlabel('Run Number')
    plt.ylabel('Iteration Number')
    plt.title('Comparison of Iterations Across Multiple Runs')
    plt.legend()
    plt.grid(True)
    plt.show()
