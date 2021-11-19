import csv

from . import models

TOPO_HEADERS = ['Node 1 (id)', 'Node 1 (label)',
                'Node 1 (longitude)', 'Node 1 (latitude)',
                'Node 2 (id)', 'Node 2 (label)',
                'Node 2 (longitude)', 'Node 2 (latitude)',
                'Distance (km)', 'Delay (mks)']

ROUTES_HEADERS = ['Node 1 (id)', 'Node 2 (id)',
                  'Path type', 'Path', 'Delay (mks)']


def dump_topo(graph, name):
    with open(name + '_topo.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(TOPO_HEADERS)

        sorted_edges = sorted(
            graph.edges,
            key=lambda e: e.source_id * graph.node_cnt + e.target_id
        )

        for edge in sorted_edges:
            node_a = graph.nodes[edge.source_id]
            node_b = graph.nodes[edge.target_id]
            writer.writerow([
                node_a.node_id, node_a.label, node_a.lon, node_a.lat,
                node_b.node_id, node_b.label, node_b.lon, node_b.lat,
                int(edge.length_km), int(models.km_to_mks(edge.length_km))
            ])
    print('Written topology to file', name + '_topo.csv')


def _route_path_to_str(graph, route_path):
    if not route_path:
        return 'no'
    node_ids = []
    for point in route_path:
        node_ids.append(graph.nodes[point].node_id)
    return '[' + ', '.join(node_ids) + ']'


def dump_routes(graph, routes, name):
    with open(name + '_routes.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(ROUTES_HEADERS)

        for route in routes:
            writer.writerow([
                route.start_id, route.target_id, route.path_type,
                _route_path_to_str(graph, route.path),
                int(route.delay) if route.delay else ''
            ])
    print('Written routes to file', name + '_routes.csv')
