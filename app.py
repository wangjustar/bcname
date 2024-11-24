import json

from flask import Flask, request, render_template, jsonify
from docs.gpt.wrap import create_account_local, is_address_in_chain, is_hexadecimal
from docs.gpt.contract import getuserinfo, publishware, reportware, evaluateware, updateprofile, updateusername,get_warehouse_data
from docs import config
from flask_cors import CORS

app = Flask(__name__)
w3 = config.Config.w3
CORS(app, supports_credentials=True)


def start_bg():
    return 'Welcome to the Index Page!'


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    start_bg()
    print("启动")
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def process_files():
    data = request.json
    if data:
        username = data.get('username')
        address = data.get('address')
        r = 0
    else:
        return jsonify({'error': "Invalid username."}), 500
    return r


@app.route('/add_account', methods=['POST'])
def add_account():
    try:
        data = request.get_json()
        private_key = str(data.get('privateKey'))
        username = data.get('username')
        # 进行一些私钥有效性验证等操作
        if not is_hexadecimal(private_key) or len(private_key) != 64:
            raise ValueError("Invalid private key")

        # 从私钥中解析出地址
        address = w3.eth.account.from_key(private_key).address
        if address in config.Config.keys:
            raise ValueError("Account already exists")

        # 将地址和私钥对保存到全局变量
        config.Config.keys[address] = private_key
        if username == '':
            return jsonify({'error': "Invalid username."}), 500
        create_account_local(username, private_key, address)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_accounts', methods=['GET'])
def get_accounts():
    try:
        return jsonify({'keys': config.Config.keys, 'default': config.Config.default})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/set_default_account', methods=['POST'])
def set_default_account():
    try:
        data = request.get_json()
        address = data.get('defaultAccount')
        w3.eth.default_account = w3.eth.account.from_key(config.Config.keys[address])
        # 更新默认账户
        config.Config.default = address
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/register_local', methods=['POST'])
# def process_files_local():
#     data = request.json
#     if data:
#         username = data.get('username')
#         if username == '':
#             return jsonify({'error': "Invalid username."}), 500
#         r = create_account_local(username)
#     else:
#         return jsonify({'error': "Invalid username."}), 500
#     return r


@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    if data:
        profile = data.get('profile')
        address = data.get('address')
        if profile == '':
            return jsonify({'error': "Invalid profile."}), 500
        r = updateprofile(profile, address)
    else:
        return jsonify({'error': "Invalid profile."}), 500
    return r


@app.route('/update_username', methods=['POST'])
def update_username():
    data = request.json
    if data:
        username = data.get('username')
        address = data.get('address')
        if username == '':
            return jsonify({'error': "Invalid username."}), 500
        r = updateusername(username, address)
    else:
        return jsonify({'error': "Invalid username."}), 500
    return r


@app.route('/info', methods=['POST'])
def get_info():
    data = request.json
    if data:
        addr = data.get('addr')
        if addr == "0x0000000000000000000000000000000000000000":
            return jsonify({'error': "User not exist."}), 500
        data = getuserinfo(addr)
        user_dict = {
            'addr': data[0],
            'username': data[1],
            'profile': data[2],
            'registerTime': data[3],
            'income': data[4],
            'expand': data[5],
            'reput': data[6]
        }

    else:
        return jsonify({'error': "Invalid address."}), 500
    return user_dict


@app.route('/warehouse', methods=['GET'])
def warehouse():
    data = get_warehouse_data()
    return jsonify(json.loads(data))  # 返回 JSON 响应


@app.route('/pb_ware', methods=['POST'])
def publish_ware():
    data = request.json
    if data:
        title = data.get('title')
        desc = data.get('desc')
        seed = data.get('seed')
        blockNum = data.get('blockNum')
        copyrightFee = data.get('copyrightFee')
        address = config.Config.default
        if title == '' or desc == '' or seed == '' or \
                blockNum == '' or copyrightFee == '' or desc == '':
            return jsonify({'error': "Invalid publish info."}), 500
        r = publishware(title, desc, seed, blockNum, copyrightFee, address)
    else:
        return jsonify({'error': "Invalid input json."}), 500
    return r


@app.route('/rp_ware', methods=['POST'])
def report_ware():
    data = request.json
    if data:
        seed = data.get('seed')
        address = data.get('address')
        if seed == '' or address == '':
            return jsonify({'error': "Invalid report info."}), 500
        r = reportware(seed, address)
    else:
        return jsonify({'error': "Invalid input json."}), 500
    return r


@app.route('/valid_account', methods=['POST'])
def valid_account():
    data = request.json
    if data:
        address = data.get('address')
        pvkey = data.get('pvkey')
        if address == '':
            return jsonify({'error': "Invalid address info."}), 500
        r = is_address_in_chain(address, pvkey)
    else:
        return jsonify({'error': "Invalid input json."}), 500
    return jsonify(r)


@app.route('/el_ware', methods=['POST'])
def evaluate_ware():
    data = request.json
    if data:
        seed = data.get('seed')
        address = data.get('address')
        result = data.get('result')
        if seed == '' or address == '':
            return jsonify({'error': "Invalid evaluate info."}), 500
        r = evaluateware(seed, address, result)
    else:
        return jsonify({'error': "Invalid input json."}), 500
    return r


if __name__ == '__main__':
    app.run(debug=False)
