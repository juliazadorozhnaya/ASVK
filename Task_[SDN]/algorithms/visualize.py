HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<script src="https://api-maps.yandex.ru/2.1/?
apikey=73bc02d2-1232-4c7a-b4a7-5a58f210a2e0&lang=en_US"
        type="text/javascript"></script>
<script type="text/javascript">
    ymaps.ready(function () {
        var myMap = new ymaps.Map("YMapsID", {
            center: [55.76, 37.64],
            zoom: 1
        });
        %s
    });
</script>
<div id="YMapsID" style="width: 99vw; height: 99vh;"></div>
</body>
</html>
'''


def _vis_node(node, is_selected):
    return f'''myMap.geoObjects.add(
    new ymaps.Placemark(
        [{node.lat}, {node.lon}],
        {{ balloonContent: "{node.label}" }},
        {{ preset: 'islands#circleIcon', iconColor: '{"#000000" 
    if is_selected else "#3b599855"}' }}
    )
);'''


def _vis_edge(graph, edge):
    a = graph.nodes[edge.source_id]
    b = graph.nodes[edge.target_id]
    return f'''myMap.geoObjects.add(
    new ymaps.Polyline([
        [{a.lat}, {a.lon}],
        [{b.lat}, {b.lon}],
    ])
);'''


def _vis_route(graph, route, is_reserve=False):
    d = []
    for node_id in route.path:
        node = graph.nodes[node_id]
        d += [f'[{node.lat}, {node.lon}]']

    return f'''myMap.geoObjects.add(
    new ymaps.Polyline(
        [{" ,".join(d)}],
        {{}},
        {{
            strokeColor: '{"#FF0000AA" if is_reserve else "#000000"}',
            strokeWidth: 6,
        }}
    )
);'''


def visualize(graph, filename, route, reserve_route=None):
    code_lines = []
    for node in graph.nodes:
        code_lines.append(
            _vis_node(
                node,
                node.node_id == route.path[0] or
                node.node_id == route.path[-1],
            )
        )
    for edge in graph.edges:
        code_lines.append(_vis_edge(graph, edge))
    if reserve_route:
        code_lines += [_vis_route(graph, reserve_route, True)]
    code_lines += [_vis_route(graph, route)]

    with open(filename, 'w') as file:
        file.write(HTML_TEMPLATE % '\n'.join(code_lines))

    print('Visualization available at file', filename)
