from math import pi, cos, sin, acos
import typing as tp


class Node:
    node_id: str
    label: str = "Unknown"
    lat: float
    lon: float

    def is_valid(self):
        return hasattr(self, 'node_id') \
               and hasattr(self, 'lat') \
               and hasattr(self, 'lon')

    def __repr__(self):
        return f'[{self.node_id}] {self.label} ({self.lon}, {self.lat})'


class Edge:
    source_id: int
    target_id: int
    length_km: float

    def __init__(self, source_id: int, target_id: int, length_km: float):
        self.source_id = source_id
        self.target_id = target_id
        self.length_km = length_km

    def __repr__(self):
        return f'{self.source_id} -> {self.target_id} ({self.length_km} km)'


def _geo_to_radian(x):
    return x / 180.0 * pi


def _get_surface_dist_km(a, b):
    lat_rad_a = _geo_to_radian(a.lat)
    lon_rad_a = _geo_to_radian(a.lon)
    lat_rad_b = _geo_to_radian(b.lat)
    lon_rad_b = _geo_to_radian(b.lon)

    central_angle = acos(
        sin(lat_rad_a) * sin(lat_rad_b) +
        cos(lat_rad_a) * cos(lat_rad_b) * cos(lon_rad_a - lon_rad_b)
    )

    # Earth's radius ~ 6371 km
    return 6371. * central_angle


def km_to_mks(km):
    return 4.8 * km


class Graph:
    nodes: tp.List[Node]
    node_cnt: int
    nodes_idx: tp.Dict[str, int]

    edges: tp.List[Edge]
    edge_cnt: int

    def __init__(self, nodes, connections):
        self.nodes = nodes
        self.node_cnt = len(nodes)
        self.nodes_idx = {
            self.nodes[i].node_id: i for i in range(self.node_cnt)
        }

        self.edges = []
        for a, b in connections:
            a_id = self.nodes_idx.get(a)
            b_id = self.nodes_idx.get(b)

            if a_id is None or b_id is None:
                # skipping invalid edges
                continue

            dist = _get_surface_dist_km(self.nodes[a_id], self.nodes[b_id])
            self.edges.append(Edge(a_id, b_id, dist))

        self.edge_cnt = len(self.edges)

    def __repr__(self):
        return f'G({self.node_cnt} nodes, {self.edge_cnt} edges)'


class Route:
    start_id: str
    target_id: str
    path_type: str = 'main'
    path = []
    delay: tp.Optional[float] = None
