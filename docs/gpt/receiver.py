import base64
import hashlib
import math
import os
import threading
import time
import json
import seed

# 新增任务超时字典


TASK_TIMEOUT = {}
LOCK = threading.Lock()
TASK_STATUS = {}
MERKLE_TREE_HASHES = []
EXTEND = ''
ROOT = ''
SIZE = 524288
TOTAL_CHUNKS = 0
OUTPUT_DIR = r"C:\Users\wangjustar\Desktop\LX"
MERGED_FILE_PATH = r"C:\Users\wangjustar\Desktop\LX\received_file."
host = "127.0.0.1"
port = 12345


def initialize_merkle_tree(n):
    x = math.ceil(math.log2(n))  # 计算需要的层数
    global MERKLE_TREE_HASHES

    # 初始化第一个元素，长度为n，所有元素为None
    MERKLE_TREE_HASHES.append([None] * n)

    # 对于接下来的每一层，长度为上一层长度的 math.ceil(l/2)
    for i in range(1, x):
        prev_layer_length = len(MERKLE_TREE_HASHES[i - 1])
        current_layer_length = math.ceil(prev_layer_length / 2)
        MERKLE_TREE_HASHES.append([None] * current_layer_length)
    MERKLE_TREE_HASHES.append([ROOT])

    return MERKLE_TREE_HASHES


def initialize_tasks(total_chunks, chunk_size, root, extend_name):
    """
    根据文件大小初始化任务队列，并计算 Merkle 树哈希。
    """
    # file_size = os.path.getsize(file_path)
    # total_chunks = (file_size + chunk_size - 1) // chunk_size
    global TASK_STATUS, TASK_TIMEOUT, MERKLE_TREE_HASHES, ROOT, SIZE, EXTEND, TOTAL_CHUNKS
    ROOT = root
    SIZE = chunk_size
    EXTEND = extend_name
    TOTAL_CHUNKS = total_chunks
    TASK_STATUS = {i: "pending" for i in range(total_chunks)}  # 全部初始化为待处理状态
    TASK_TIMEOUT = {i: None for i in range(total_chunks)}  # 初始化超时状态


def merge_files(output_dir, merged_file_path):
    # 获取所有文件块
    bin_files = [f for f in os.listdir(output_dir) if f.startswith("part_") and f.endswith(".bin")]

    # 按块 ID 排序
    bin_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))  # 提取 ID 并排序

    with open(merged_file_path, "wb") as merged_file:
        for bin_file in bin_files:
            part_path = os.path.join(output_dir, bin_file)
            with open(part_path, "rb") as part:
                data = part.read()
                merged_file.write(data)

        # 删除已合并的 .bin 文件
        for bin_file in bin_files:
            part_path = os.path.join(output_dir, bin_file)
            try:
                os.remove(part_path)
                print(f"已删除文件块: {part_path}")
            except Exception as e:
                print(f"删除文件 {part_path} 失败: {e}")

    print(f"文件已成功合并到: {merged_file_path}")


def get_next_task():
    current_time = time.time()
    for chunk_id, status in TASK_STATUS.items():
        if status == "pending":
            TASK_STATUS[chunk_id] = "assigned"
            TASK_TIMEOUT[chunk_id] = current_time + 10  # 设置10秒超时
            return chunk_id
        elif status == "assigned" and TASK_TIMEOUT[chunk_id] and current_time > TASK_TIMEOUT[chunk_id]:
            print(f"任务 {chunk_id} 超时，重新分配")
            TASK_STATUS[chunk_id] = "pending"
            TASK_TIMEOUT[chunk_id] = None  # 重置超时
            return chunk_id
    return None  # 没有可用任务


def mark_task_complete(chunk_id):
    """
    标记任务为完成状态。
    """
    global TASK_STATUS
    with LOCK:
        TASK_STATUS[chunk_id] = "completed"


def handle_client(conn, addr):
    """
    处理单个发送端的连接。
    """
    print(f"客户端 {addr} 已连接")
    conn.settimeout(50)
    while True:
        try:
            # 接收发送端请求
            data = b""
            l = 0
            try:
                chunk = conn.recv(4096)
                if chunk.decode() == "REQUEST_TASK":
                    data = chunk
                else:
                    data += chunk[10:]
                    l = chunk[:10]
            except socket.timeout:
                print("接收超时")
            if not data:
                break
            request = data.decode()
            request = request.strip()

            if request == "REQUEST_TASK":
                # 分配任务
                with LOCK:
                    chunk_id = get_next_task()
                if chunk_id is not None:
                    pathl = []
                    if MERKLE_TREE_HASHES[0][chunk_id] is not None:
                        pathl = []
                    else:
                        list_valid = seed.merkle_tree_positions(TOTAL_CHUNKS, chunk_id)
                        for i in range(seed.smallest_x(TOTAL_CHUNKS)):
                            if MERKLE_TREE_HASHES[i][list_valid[i]] is None:
                                pathl.append([i, list_valid[i]])
                    conn.sendall(json.dumps({"chunk_id": chunk_id,
                                             "pathl": pathl, }).encode())
                else:
                    conn.sendall(b"NO_TASK")  # 无可分配任务
            else:
                # 接收文件块
                loops = int(l.strip())
                if loops > 1:
                    for i in range(loops - 1):
                        chunk = conn.recv(4096)
                        data += chunk
                data = json.loads(data.decode())
                chunk_id = data["chunk_id"]
                chunk_data = bytes.fromhex(data["data"])
                path_hashes = data["path_hashes"]

                # 验证块的哈希值
                received_hash = hashlib.sha256(chunk_data).hexdigest()
                if path_hashes:
                    for i in path_hashes:
                        MERKLE_TREE_HASHES[i[0]][i[1]] = i[2]
                if MERKLE_TREE_HASHES[0][chunk_id] != received_hash:
                    if not seed.value(chunk_id, received_hash, MERKLE_TREE_HASHES):
                        print(f"文件块 {chunk_id} 校验失败！重置任务")
                        conn.sendall(b"CHECK FAILED")
                        with LOCK:
                            TASK_STATUS[chunk_id] = "pending"
                        TASK_TIMEOUT[chunk_id] = None  # 重置超时
                        continue
                conn.sendall(b"CHECK COMPLETE")

                # 保存块数据
                output_path = os.path.join(OUTPUT_DIR, f"part_{chunk_id}.bin")
                with open(output_path, "wb") as f:
                    f.write(chunk_data)

                print(f"文件块 {chunk_id} 已接收并保存到: {output_path}")
                mark_task_complete(chunk_id)

        except Exception as e:
            print(f"处理客户端 {addr} 时出错: {e}")
            break
    merge_files(OUTPUT_DIR, MERGED_FILE_PATH + EXTEND)

    conn.close()
    print(f"客户端 {addr} 断开连接")


if __name__ == "__main__":
    import socket
    from threading import Thread

    host = "127.0.0.1"
    port = 12345


    def start_receiver():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5)
            print(f"接收端启动，监听地址 {host}:{port}")

            while True:
                conn, addr = server_socket.accept()
                Thread(target=handle_client, args=(conn, addr)).start()


    initialize_tasks(6154, SIZE, '760ea8591c538e94801dd7240a93cc214704445937e215528b2ebf6e501c5d6a', extend_name='mp4')
    initialize_merkle_tree(6154)
    start_receiver()
