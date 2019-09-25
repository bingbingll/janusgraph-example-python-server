from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#af"F4Q8z\n\xec]/'

# 中文不进行ASCII转换
app.config['JSON_AS_ASCII'] = False

login_manager = LoginManager(app)
login_manager.session_protection = "strong"


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    '''若是pycharm 开发工具这里设置不起作用，需要在编辑设置 FLASK_DEBUG 进行勾选'''
    # app.run(debug=True)
