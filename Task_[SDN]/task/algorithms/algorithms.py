from . import models


def floyd_warshall(graph):
    # 250 000 turns around equator, seems enough for our task
    INFINITY_KM = 1e10

    dist = [
        # something bigger then INFINITY_KM for easier clean-up
        [INFINITY_KM * 2] * graph.node_cnt
        for _ in range(graph.node_cnt)
    ]
    next_vertex = [
        [
            i if i == j else None
            for j in range(graph.node_cnt)
        ]
        for i in range(graph.node_cnt)
    ]

    for edge in graph.edges:
        dist[edge.source_id][edge.target_id] = edge.length_km
        next_vertex[edge.source_id][edge.target_id] = edge.target_id

    for k in range(1, graph.node_cnt):
        for i in range(graph.node_cnt):
            for j in range(graph.node_cnt):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_vertex[i][j] = next_vertex[i][k]

    # Cleaning up
    for i in range(graph.node_cnt):
        for j in range(graph.node_cnt):
            if dist[i][j] > INFINITY_KM:
                dist[i][j] = None

    return dist, next_vertex


def find_reserve_route(graph, a_id, b_id, black_list):
    # set weight 1 for each edge to excluded node, 0 for all others
    # afterwards we'll look at the shortest path from A to B:
    # if path weight == 0 - reserve path exists
    #                == 2 - only with one critical node
    #                <= 3 - no satisfying reserve path

    class PriorityDistance:
        dist_km: float
        ugliness: int

        def __init__(self, ugliness, dist_km):
            self.ugliness = ugliness
            self.dist_km = dist_km

        def __repr__(self):
            return f'({self.ugliness},{self.dist_km})'

        def __add__(self, other):
            return PriorityDistance(
                self.ugliness + other.ugliness, self.dist_km + other.dist_km
            )

        def __lt__(self, other):
            if self.ugliness == other.ugliness:
                return self.dist_km < other.dist_km
            return self.ugliness < other.ugliness

    INF = PriorityDistance(1000000, 0)

    excluded_edges = [
        (black_list[i - 1], black_list[i]) for i in range(1, len(black_list))
    ]

    new_edges = {i: {} for i in range(graph.node_cnt)}
    for edge in graph.edges:
        if (edge.source_id, edge.target_id) in excluded_edges:
            continue
        ugliness = 0
        if edge.source_id in black_list:
            ugliness = 1
        new_edges[edge.source_id][edge.target_id] = PriorityDistance(
            ugliness, edge.length_km
        )

    visited = [False] * graph.node_cnt
    dist = [INF for _ in range(graph.node_cnt)]
    path = [[] for _ in range(graph.node_cnt)]

    dist[a_id] = PriorityDistance(0, 0)
    path[a_id] = [a_id]

    while not visited[b_id]:
        v = -1
        min_dist = INF

        for i in range(graph.node_cnt):
            if not visited[i]:
                if min_dist > dist[i]:
                    v = i
                    min_dist = dist[i]

        if v == -1:
            break

        visited[v] = True

        for u in new_edges[v]:
            if visited[u]:
                continue
            if dist[u] > dist[v] + new_edges[v][u]:
                dist[u] = dist[v] + new_edges[v][u]
                path[u] = path[v] + [u]

    route = models.Route()
    route.start_id = graph.nodes[a_id].node_id
    route.target_id = graph.nodes[b_id].node_id
    route.path_type = 'reserve'
    if dist[b_id].ugliness > 2:
        return route

    route.delay = models.km_to_mks(dist[b_id].dist_km)
    route.path = path[b_id]
    return route


def extract_route(graph, a_id, b_id, dist, next_vertex):
    route = models.Route()
    route.start_id = graph.nodes[a_id].node_id
    route.target_id = graph.nodes[b_id].node_id
    if next_vertex[a_id][b_id] is None:
        return route

    route.delay = int(models.km_to_mks(dist[a_id][b_id]))
    route.path = []
    x_id = a_id
    while x_id != b_id:
        route.path.append(x_id)
        x_id = next_vertex[x_id][b_id]
    route.path.append(b_id)
    return route
