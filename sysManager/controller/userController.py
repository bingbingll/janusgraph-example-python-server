# -*- coding: utf-8 -*-
from flask import jsonify

from config.app import app
from test import dataload


@app.route('/sys/user/ins', methods=['GET'])
def instest():
    dataload.inst_test()
    return 'ok'


@app.route('/sys/user/getall', methods=['GET'])
def getall():
    data = dataload.query_test()
    # 返回字符串
    # return json.dumps(data, ensure_ascii=False)
    return jsonify(data)
