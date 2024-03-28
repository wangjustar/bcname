from docs import gpt
from flask import Flask, request, render_template
from docs.gpt import ask
from docs.gpt.wrap import create_account
from docs.gpt.wrap import all_accounts

app = Flask(__name__)


#


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
        a, b = create_account(username)
    else:
        a, b = 0, 0
    return a, "eee", b


@app.route('/all', methods=['POST'])
def accounts():
    all_accounts()
    return 0


if __name__ == '__main__':
    app.run(debug=False)
