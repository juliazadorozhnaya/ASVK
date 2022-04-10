import argparse

from utils import parser, algorithms, dump, visualize


def main(args):
    graph = parser.parse_graphml(args.file_name)
    print('Parsed graph:', graph)
    dump.dump_topo(graph, args.file_name)

    dist, next_vertex = algorithms.floyd_warshall(graph)
    routes = []

    for i in range(graph.node_cnt):
        for j in range(graph.node_cnt):
            if i == j:
                continue
            direct_route = algorithms.extract_route(
                graph, i, j, dist, next_vertex
            )
            routes.append(direct_route)
            routes.append(algorithms.find_reserve_route(
                graph, i, j, direct_route.path)
            )

    dump.dump_routes(graph, routes, args.file_name)

    if args.source_node_id is not None \
            and args.destination_node_id is not None:
        start_idx = graph.nodes_idx[args.source_node_id]
        dest_idx = graph.nodes_idx[args.destination_node_id]
        direct_route = algorithms.extract_route(
            graph, start_idx, dest_idx, dist, next_vertex
        )
        reserve_route = algorithms.find_reserve_route(
            graph, start_idx, dest_idx, direct_route.path
        )
        visualize.visualize(
            graph, args.file_name + '_demo.html', direct_route, reserve_route
        )


if __name__ == '__main__':
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument('-t', '--file-name', required=True,
                           help='filename to parse, .gml or .graphml')
    arg_parse.add_argument('-k1', '--source-node-id',
                           help='source node id to visualize')
    arg_parse.add_argument('-k2', '--destination-node-id',
                           help='destination node id to visualize')
    args = arg_parse.parse_args()
    print('Parsed arguments:')
    for arg_name, arg_value in args._get_kwargs():
        print(arg_name, '=', arg_value)
    main(args)
