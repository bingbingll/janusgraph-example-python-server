from flask import Flask
from flask import jsonify

from janusgraph import gremlinConfig
from test import dataload

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 中文不进行ASCII转换


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getAllVertex1', methods=['GET'])
def get_all_vertex_1():
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


@app.route('/getAllVertex2', methods=['GET'])
def get_all_vertex_2():
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


@app.route('/delId')
def del_id():
    gremlinConfig.drop_vertex(gremlinConfig.get_graph(), 110123456789123456)
    return '成功'


@app.route('/addVer')
def add_ver():
    prp1 = {'age': 32, 'addr': '北京市昌平区', 'phone': '13812345678', 'xuli': '本科', 'no': '110123456789123456'}
    gremlinConfig.add_vertex(gremlinConfig.get_graph(), '张明', prp1)

    prp2 = {'age': 34, 'addr': '北京市昌平区', 'phone': '13312345678', 'xuli': '本科', 'no': '110546546465461321'}
    gremlinConfig.add_vertex(gremlinConfig.get_graph(), '王晓', prp2)

    prp3 = {'age': 29, 'addr': '北京市朝阳区', 'phone': '13112345678', 'xuli': '本科', 'no': '112346546546546546'}
    gremlinConfig.add_vertex(gremlinConfig.get_graph(), '李菲', prp3)
    return '成功'


@app.route('/get', methods=['GET'])
def get():
    v = gremlinConfig.query_edges_of_vertex(gremlinConfig.get_graph(), 28672)
    return jsonify(v)


@app.route('/ins', methods=['GET'])
def instest():
    dataload.inst_test()
    return 'ok'


@app.route('/getall', methods=['GET'])
def getall():
    data = dataload.query_test()
    # 返回字符串
    # return json.dumps(data, ensure_ascii=False)
    return jsonify(data)


if __name__ == '__main__':
    '''若是pycharm 开发工具这里设置不起作用，需要在编辑设置 FLASK_DEBUG 进行勾选'''
    # app.run(debug=True)
