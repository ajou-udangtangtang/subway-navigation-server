import heapq
import json
import math
from dataclasses import dataclass
from pathlib import Path

from ..api.errors import (
    DangerDestinationError,
    InvalidNodeError,
    NoRouteError,
    NotConnectedError,
)


Coord = tuple[float, float]


@dataclass(frozen=True)
class GraphData:
    nodes: dict[str, Coord]
    edges: dict[str, list[str]]
    danger: frozenset[str]

    def has_node(self, node_id: str) -> bool:
        return node_id in self.nodes

    def neighbors(self, node_id: str) -> list[str]:
        return self.edges.get(node_id, [])

    def is_connected(self, a: str, b: str) -> bool:
        return b in self.edges.get(a, [])

    def coord(self, node_id: str) -> Coord:
        return self.nodes[node_id]


def load_graph(data_dir: Path | str) -> GraphData:
    data_dir = Path(data_dir)
    nodes_raw = json.loads((data_dir / "nodes.json").read_text(encoding="utf-8"))
    edges_raw = json.loads((data_dir / "edges.json").read_text(encoding="utf-8"))
    danger_raw = json.loads((data_dir / "danger.json").read_text(encoding="utf-8"))

    nodes: dict[str, Coord] = {
        nid: (float(d["x"]), float(d["y"])) for nid, d in nodes_raw.items()
    }
    edges: dict[str, list[str]] = {nid: list(adj) for nid, adj in edges_raw.items()}
    danger = frozenset(danger_raw)

    _validate_graph(nodes, edges, danger)

    return GraphData(nodes=nodes, edges=edges, danger=danger)


def _validate_graph(
    nodes: dict[str, Coord],
    edges: dict[str, list[str]],
    danger: frozenset[str],
) -> None:
    """Surface data bugs early. Does not auto-fix."""
    for nid in edges:
        if nid not in nodes:
            raise ValueError(f"edges references unknown node: {nid!r}")
        for neighbor in edges[nid]:
            if neighbor not in nodes:
                raise ValueError(
                    f"edges[{nid!r}] references unknown node: {neighbor!r}"
                )
            if nid not in edges.get(neighbor, []):
                raise ValueError(
                    f"asymmetric edge: {nid!r} -> {neighbor!r} but no reverse"
                )
    for nid in danger:
        if nid not in nodes:
            raise ValueError(f"danger references unknown node: {nid!r}")


def dijkstra(graph: GraphData, start: str, goal: str) -> list[str]:
    """Shortest path from start to goal, excluding danger nodes (except endpoints).

    Raises:
        InvalidNodeError: start or goal is not in the graph.
        DangerDestinationError: goal is a danger node.
        NoRouteError: no path exists when danger nodes are excluded.
    """
    if not graph.has_node(start):
        raise InvalidNodeError(f"Unknown node id: {start!r}")
    if not graph.has_node(goal):
        raise InvalidNodeError(f"Unknown node id: {goal!r}")
    if goal in graph.danger:
        raise DangerDestinationError(f"Destination is a danger node: {goal!r}")

    if start == goal:
        return [start]

    # If start is a danger node, allow leaving it but never re-entering.
    distances: dict[str, float] = {start: 0.0}
    came_from: dict[str, str] = {}
    heap: list[tuple[float, str]] = [(0.0, start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if node == goal:
            break
        if cost > distances.get(node, math.inf):
            continue
        for neighbor in graph.neighbors(node):
            if neighbor != goal and neighbor in graph.danger:
                continue
            edge_cost = _edge_cost(graph, node, neighbor)
            new_cost = cost + edge_cost
            if new_cost < distances.get(neighbor, math.inf):
                distances[neighbor] = new_cost
                came_from[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    if goal not in distances:
        raise NoRouteError(f"No safe route from {start!r} to {goal!r}")

    return _reconstruct_path(came_from, start, goal)


def _edge_cost(graph: GraphData, a: str, b: str) -> float:
    ax, ay = graph.coord(a)
    bx, by = graph.coord(b)
    return math.hypot(bx - ax, by - ay)


def _reconstruct_path(came_from: dict[str, str], start: str, goal: str) -> list[str]:
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def assert_connected(graph: GraphData, a: str, b: str) -> None:
    """Raise NotConnectedError if a and b are not directly adjacent."""
    if not graph.has_node(a):
        raise InvalidNodeError(f"Unknown node id: {a!r}")
    if not graph.has_node(b):
        raise InvalidNodeError(f"Unknown node id: {b!r}")
    if not graph.is_connected(a, b):
        raise NotConnectedError(f"Nodes {a!r} and {b!r} are not directly connected")
