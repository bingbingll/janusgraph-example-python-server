from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver import client
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

url = '172.16.2.137:8182'


# 获取GraphTraversalSource对象
def get_graph():
    graph = Graph()
    g = graph.traversal().withRemote(
        DriverRemoteConnection('ws://' + url + '/gremlin', 'g', pool_size=20, max_workers=15))
    return g


# 获取客户端
def get_client():
    clients = client.Client('ws://' + url + '/gremlin', 'g', pool_size=20, max_workers=15)
    return clients


# 新增节点只需传入新增节点的 label 以及 properties（dict，可选），返回 Vertex(id, label)类型。
def add_vertex(graph, label, properties=None):
    """
    add vertex
    :param graph: graph, type: GraphTraversalSource
    :param label: label, type: str
    :param properties: property dict, like {'p1': 'value1', 'p2': 'value2'}
    :return: vertex, Vertex(id, label)
    """
    vert = graph.addV(label)
    if properties:
        for key in properties.keys():
            vert.property(key, properties.get(key))
    return vert.next()


# 新增边传入新增边的 label 和 properties（dict，可选），以及需要添加边的两节点（或其ID）v_from和v_to。
def add_edge(graph, label, v_from, v_to, properties=None):
    """
    add edge
    :param graph: graph, type: GraphTraversalSource
    :param label: label, type: str
    :param v_from: long vertex id or Vertex(id, label) of from
    :param v_to: long vertex id or Vertex(id, label) of to
    :param properties: property dict, like {'p1': 'value1', 'p2': 'value2'}
    :return: None
    """
    if isinstance(v_from, int):
        v_from = graph.V().hasId(v_from).next()
    if isinstance(v_to, int):
        v_to = graph.V().hasId(v_to).next()
    edge = graph.V(v_from).addE(label).to(v_to)
    if properties:
        for key in properties.keys():
            edge.property(key, properties.get(key))
    edge.next()


# 删除节点可以根据要求来删除特定节点，如根据节点（或其ID）、label、properties。如果不传入其他参数，则默认删除所有节点。
def drop_vertex(graph, v_id=None, label=None, properties=None):
    """
    drop all vertex or specific vertex
    :param graph: graph, type: GraphTraversalSource
    :param v_id: long vertex id or Vertex(id, label)
    :param label: label, type: str
    :param properties: property list, like ['p1', 'p2', {'p3': 'value'}]
    :return: None
    """
    if isinstance(v_id, int):
        v_id = graph.V().hasId(v_id).next()
    travel = graph.V(v_id) if v_id else graph.V()
    if label:
        travel = travel.hasLabel(label)
    if properties:
        for p in properties:
            if isinstance(p, dict):
                key = list(p.keys())[0]
                travel = travel.has(key, p.get(key))
            else:
                travel = travel.has(p)
    travel.drop().iterate()


# 删除边可以根据要求来删除特定边，如根据边ID、label、properties。如果不传入其他参数，则默认删除所有边。
def drop_edge(graph, e_id=None, label=None, properties=None):
    """
    drop all edges or specific edge
    :param graph: graph, type: GraphTraversalSource
    :param e_id: edge id, type str
    :param label: label, type: str
    :param properties: property list, like ['p1', 'p2', {'p3': 'value'}]
    :return: None
    """
    travel = graph.E(e_id) if e_id else graph.E()
    if label:
        travel = travel.hasLabel(label)
    if properties:
        for p in properties:
            if isinstance(p, dict):
                key = list(p.keys())[0]
                travel = travel.has(key, p.get(key))
            else:
                travel = travel.has(p)
    travel.drop().iterate()


# 查询节点
# 首先，可以根据节点（或其ID）查询该节点的所有属性值，此时需使用return travel.valueMap().toList()。
# 其次，可以通过 label 或 properties 来查询符合条件的所有节点，此时使用return travel.toList()。
def query_vertex(graph, v_id=None, label=None, properties=None):
    """
    query graph vertex (value) list
    :param graph: graph, type: GraphTraversalSource
    :param v_id: long vertex id or Vertex(id, label)
    :param label: label, type: str
    :param properties: property list, like ['p1', 'p2', {'p3': 'value'}]
    :return: vertex list or vertex value list
    """
    if isinstance(v_id, int):
        v_id = graph.V().hasId(v_id).next()
    travel = graph.V(v_id) if v_id else graph.V()
    if label:
        travel = travel.hasLabel(label)
    if properties:
        for p in properties:
            if isinstance(p, dict):
                key = list(p.keys())[0]
                travel = travel.has(key, p.get(key))
            else:
                travel = travel.has(p)
    # return travel.valueMap().toList()
    return travel.toList()


# 查询边根据边的ID、label 或 properties 来查询符合条件的边的所有属性值。
def query_edge(graph, e_id=None, label=None, properties=None):
    """
    query graph edge value list
    :param graph: graph, type: GraphTraversalSource
    :param e_id: edge id, type str
    :param label: label, type: str
    :param properties: property list, like ['p1', 'p2', {'p3': 'value'}]
    :return: valueMap list
    """
    travel = graph.E(e_id) if e_id else graph.E()
    if label:
        travel = travel.hasLabel(label)
    if properties:
        for p in properties:
            if isinstance(p, dict):
                key = list(p.keys())[0]
                travel = travel.has(key, p.get(key))
            else:
                travel = travel.has(p)
    return travel.valueMap().toList()


# 查询所有与节点相连的边根据节点（或其ID）查询与该节点相连的所有边。
def query_edges_of_vertex(graph, v_id):
    """
    query all edges of vertex
    :param graph: graph, type: GraphTraversalSource
    :param v_id: v_id: long vertex id or Vertex(id, label)
    :return: edge list
    """
    if isinstance(v_id, int):
        v_id = graph.V().hasId(v_id).next()
    result = []
    in_edges = graph.V(v_id).inE().toList()
    out_edges = graph.V(v_id).outE().toList()
    result.extend(in_edges)
    result.extend(out_edges)
    return result


# 查询所有与节点相连的节点 根据节点（或其ID）查询与该节点相连的所有节点。
def query_near_vertex(graph, v_id):
    """
    query near vertices of vertex
    :param graph: graph, type: GraphTraversalSource
    :param v_id: v_id: long vertex id or Vertex(id, label)
    :return: vertex list
    """
    if isinstance(v_id, int):
        v_id = graph.V().hasId(v_id).next()
    result = []
    out_v = graph.V(v_id).out().toList()
    in_v = graph.V(v_id).in_().toList()
    result.extend(out_v)
    result.extend(in_v)
    return


# 获取边的ID
def get_edge_id(edge):
    """
    get edge id
    :param edge: Egde(id, label, outV, inV)
    :return: edge id, type str
    """
    return edge.id.get('@value').get('relationId')


# 节点属性转字典
def vertex_to_dict(graph, vertex):
    """
    transfer Vertex's info to dict
    :param graph: graph, type: GraphTraversalSource
    :param vertex: vertex, Vertex(id, label)
    :return: vertex info dict
    """
    properties = graph.V(vertex).valueMap().toList()[0]
    for key in properties.keys():
        properties[key] = properties.get(key)[0]
    return {
        'id': vertex.id,
        'label': vertex.label,
        'properties': properties
    }


# 边属性转dict
def edge_to_dict(graph, edge):
    """
    transfer Edge's info to dict
    :param graph: graph, type: GraphTraversalSource
    :param edge: edge, Edge(id, label, outV, inV)
    :return: edge info dict
    """
    e_id = get_edge_id(edge)
    properties = graph.E(e_id).valueMap().toList()[0]
    return {
        'id': e_id,
        'label': edge.label,
        'properties': properties
    }


# 判断节点是否在图中
# 对于已知节点的 label 和 properties 值，判断该节点是否在图中；如果在，返回该节点，否则返回None。
def judge_vertex_in_graph(graph, vertex_dict):
    """
    judge a vertex whether in graph
    :param graph: graph, type: GraphTraversalSource
    :param vertex_dict: vertex dict, like {'label': 'value1', 'properties': {'p1': 'v1', ...}}
    :return: None or Vertex(id,label)
    """
    label = vertex_dict.get('label')
    properties = vertex_dict.get('properties')
    travel = graph.V()
    if label:
        travel = travel.hasLabel(label)
    if properties:
        for k in properties.keys():
            travel = travel.has(k, properties.get(k))
    if travel.hasNext():
        return travel.next()
    return None
