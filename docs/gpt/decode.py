import binascii
import bencodepy


def decode_torrent_content(torrent_hex):
    # 将十六进制字符串解码为字节数据
    torrent_bytes = binascii.unhexlify(torrent_hex)

    # 使用 bencodepy 解析字节数据为字典
    torrent_data = bencodepy.decode(torrent_bytes)

    return torrent_data


def main():
    # 输入种子文件内容的十六进制字符串
    torrent_hex = input("Enter the hexadecimal string of the torrent content: ")

    # 解析种子文件内容并打印字典数据结构
    torrent_data = decode_torrent_content(torrent_hex)
    print("Torrent Data (Dictionary Structure):")
    print(torrent_data)


if __name__ == "__main__":
    main()
