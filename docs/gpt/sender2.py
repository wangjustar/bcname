import json
import math
import socket
import time

from docs.gpt.seed import sha256_chunks, get_value_node, make_tree, get_chunk_data

chunk_size = 524288


def start_sender(file_path, host, port):
    """
    发送端：动态请求任务并发送文件块和路径哈希。
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"已连接到接收端：{host}:{port}")

        # 获取 Merkle 树哈希
        hash_list = sha256_chunks(file_path, chunk_size)
        tree = make_tree(hash_list)

        while True:
            resend = 0
            try:
                # 请求任务
                client_socket.sendall(b"REQUEST_TASK")
                response = client_socket.recv(4096).decode()
                if response == "NO_TASK":
                    print("无可分配任务，发送端完成工作")
                    break

                task_info = json.loads(response)
                chunk_id = task_info["chunk_id"]
                pathl = task_info["pathl"]

                # 获取块数据
                chunk_data = get_chunk_data(file_path, chunk_size, chunk_id)
                chunk_hash = hash_list[chunk_id]

                # 生成路径哈希
                path_hashes = []
                if pathl:
                    for tuplex in pathl:
                        path_hashes.append([tuplex[0], tuplex[1], tree[tuplex[0]][tuplex[1]]])
                jsonx = json.dumps({
                    "chunk_id": chunk_id,
                    "data": chunk_data.hex(),
                    "chunk_hash": chunk_hash,
                    "path_hashes": path_hashes,
                })
                content = jsonx.encode()
                length = math.ceil((len(content) + 10) / 4096)
                # 发送块数据、路径哈希
                s = f"{length:<10}" + jsonx
                client_socket.sendall(s.encode())
                response2 = client_socket.recv(4096).decode()
                print(f"文件块 {chunk_id} 和路径哈希已发送")
                if response2 == "CHECK COMPLETE":
                    continue
                else:
                    print("块校验失败。")
            except Exception as e:
                print(f"任务 {chunk_id} 传输失败，重新请求: {e}")
                resend += 1
                if resend < 10:
                    time.sleep(1)  # 短暂休眠后重试
                else:
                    break


if __name__ == "__main__":
    file_path = r"C:\Users\wangjustar\Desktop\World Finals ｜ Day 3 ｜ Clash Royale League 2024.mp4" # 测试文件
    host = "127.0.0.1"
    port = 12345

    start_sender(file_path, host, port)

