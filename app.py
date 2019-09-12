from typing import Dict, List, Any

from flask import jsonify
from flask import json
from flask import Flask
from gremlin_python.structure.graph import Vertex
from config import gremlinConfig

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getList1', methods=['GET'])
def get_list_1():
    g = gremlinConfig.get_graph()
    vl = g.V().toList()
    result = []  ## 空列表
    for Vertex in vl:
        # 空的字典对象
        dict_ver = {}
        dict_ver['id'] = Vertex.id
        dict_ver['label'] = Vertex.label
        result.append(dict_ver)
    return jsonify(result)


@app.route('/getList2', methods=['GET'])
def get_list_2():
    g = gremlinConfig.get_graph()
    vs = g.V().valueMap(True).toList()
    print(vs)
    result = []  ## 空列表
    for dic in vs:
        dict2 = {}  # 创建新的字典
        for key, value in dic.items():
            dict2.setdefault(str(key), value)
        result.append(dict2)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
