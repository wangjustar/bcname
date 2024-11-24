import hashlib
import math
import os

file_path1 = r"C:\Users\wangjustar\Desktop\World Finals ｜ Day 3 ｜ Clash Royale League 2024.mp4"


def smallest_x(n):
    x = math.ceil(math.log2(n))
    return x


def get_chunk_data(file_path, chunk_size, chunk_id):
    with open(file_path, 'rb') as f:
        f.seek(chunk_size * chunk_id)  # 跳到块的起始位置
        return f.read(chunk_size)


def sha256_chunks(file_path, chunk_size=524288):
    hash_values = []
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            hash_object = hashlib.sha256()
            hash_object.update(data)
            hash_values.append(hash_object.hexdigest())
    return hash_values


def recursive_sha256(hash_list):
    if len(hash_list) == 1:
        return hash_list[0]
    else:
        new_list = []
        for i in range(0, len(hash_list) - 1, 2):
            concat_value = hash_list[i] + hash_list[i + 1]
            hash_object = hashlib.sha256()
            hash_object.update(concat_value.encode())
            new_list.append(hash_object.hexdigest())
        if len(hash_list) % 2 != 0:
            concat_value = hash_list[-1] + hash_list[-1]
            hash_object = hashlib.sha256()
            hash_object.update(concat_value.encode())
            new_list.append(hash_object.hexdigest())
        return new_list


def make_tree(hash_list):
    if len(hash_list) == 1:
        return hash_list[0]
    else:
        new_list = [hash_list]  # 将初始列表作为新列表的第一个元素
        for i in range(smallest_x(len(hash_list))):
            hash_list = recursive_sha256(hash_list)
            new_list.append(hash_list)
    return new_list


def get_root(tree):
    return tree[-1][0]


def get_value_node(tree, x):
    p = merkle_tree_positions(len(tree[0]) - 1, x)
    h = len(tree)
    l = []
    for i in range(0, h - 1):
        l.append(tree[i][p[i]])
    return l


def value(node, node_hash, tree):
    root = get_root(tree)
    l = get_value_node(tree, node)
    for i in range(0, len(l)):
        if node % 2 == 0:
            concat_value = node_hash + l[i]
            node = node // 2
        else:
            concat_value = l[i] + node_hash
            node = (node - 1) // 2
        hash_object = hashlib.sha256()
        hash_object.update(concat_value.encode())
        node_hash = hash_object.hexdigest()
    return node_hash == root


def valid(node, node_hash, l, root):
    for i in range(0, len(l)):
        if node % 2 == 0:
            concat_value = node_hash + l[i]
            node = node // 2
        else:
            concat_value = l[i] + node_hash
            node = (node - 1) // 2
        hash_object = hashlib.sha256()
        hash_object.update(concat_value.encode())
        node_hash = hash_object.hexdigest()
    return node_hash != root


def dealn(n):
    if n % 2 == 0:
        return n // 2
    else:
        return (n - 1) // 2


def merkle_tree_positions(n, x):
    positions = []
    num_layers = smallest_x(n)

    # 计算每层所需的验证节点位置
    for layer in range(num_layers):
        if x % 2 == 0 and x < n:
            positions.append(int(x + 1))
            x = x / 2
        elif x % 2 == 0 and x == n:
            positions.append(int(x))
            x = x / 2
        else:
            positions.append(int(x - 1))
            x = (x - 1) / 2
        n = dealn(n)
    return positions


def process_file(file_path, chunk_size=524288):
    """
    处理文件并输出分块数和根哈希值。
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件路径不存在: {file_path}")

    # 计算文件的块哈希值
    chunk_hashes = sha256_chunks(file_path, chunk_size)
    block_count = len(chunk_hashes)

    # 生成 Merkle 树并获取根哈希值
    root_hash = get_root(make_tree(chunk_hashes))
    return block_count, root_hash


if __name__ == "__main__":
    print(process_file(file_path1))
