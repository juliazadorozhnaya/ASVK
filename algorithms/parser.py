from xml.dom import minidom

from . import models


def parse_graphml(path):
    doc = minidom.parse(path)
    root = doc.firstChild

    lat_key_id = None
    lon_key_id = None
    label_key_id = None

    for element in root.getElementsByTagName('key'):
        items = dict(element.attributes.items())
        if items['for'] != 'node':
            continue
        if items['attr.name'].lower() == 'latitude':
            lat_key_id = items['id']
        if items['attr.name'].lower() == 'longitude':
            lon_key_id = items['id']
        if items['attr.name'].lower() == 'label':
            label_key_id = items['id']

    if lat_key_id is None:
        raise Exception('Latitude key was not found in graph keys')
    if lon_key_id is None:
        raise Exception('Longitude key was not found in graph keys')
    if label_key_id is None:
        raise Exception('Label key was not found in graph keys')

    graph_element = root.getElementsByTagName('graph')[0]

    nodes = []
    for element in graph_element.getElementsByTagName('node'):
        node = models.Node()
        node.node_id = element.getAttribute('id')
        for data_element in element.getElementsByTagName('data'):
            if data_element.getAttribute('key') == lat_key_id:
                node.lat = float(data_element.firstChild.nodeValue)
            if data_element.getAttribute('key') == lon_key_id:
                node.lon = float(data_element.firstChild.nodeValue)
            if data_element.getAttribute('key') == label_key_id:
                node.label = data_element.firstChild.nodeValue
        if node.is_valid():
            nodes += [node]
        else:
            print(f'Node with id {node.node_id} '
                  f'is invalid, skipping node and all adjacent edges')
    print(f'Parsed {len(nodes)} nodes')

    edges = []
    for element in graph_element.getElementsByTagName('edge'):
        edges += [
            (element.getAttribute('source'), element.getAttribute('target'))
        ]
        edges += [
            (element.getAttribute('target'), element.getAttribute('source'))
        ]
    print(f'Parsed {len(edges)} edges')

    return models.Graph(nodes, edges)
