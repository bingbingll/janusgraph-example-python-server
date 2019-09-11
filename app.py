from flask import jsonify
from flask import json
from flask import Flask
from config import gremlinConfig
from gremlin_python.process.traversal import T

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getList', methods=['GET'])
def get_list():
    g = gremlinConfig.get_graph()
    vs = g.V().valueMap(True).toList()
    print(vs)
    # 目前不知道该怎么将vs转换为json数据返回
    return '111'


if __name__ == '__main__':
    app.run(debug=True)


# list 转成Json格式数据
def listToJson(lst):
    import json
    import numpy as np
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json
