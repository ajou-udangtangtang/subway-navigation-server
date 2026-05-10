import json
from pathlib import Path

import pytest

from subway_server.api.errors import (
    DangerDestinationError,
    InvalidNodeError,
    NoRouteError,
    NotConnectedError,
)
from subway_server.core.graph import (
    GraphData,
    assert_connected,
    dijkstra,
    load_graph,
)


FIXTURE_DIR = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def graph() -> GraphData:
    return load_graph(FIXTURE_DIR)


# -- load_graph -------------------------------------------------------


def test_load_graph_reads_all_three_files(graph):
    assert "A" in graph.nodes
    assert graph.nodes["A"] == (0.0, 0.0)
    assert "B" in graph.edges["A"]
    assert "E" in graph.danger


def test_load_graph_rejects_unknown_node_in_edges(tmp_path):
    (tmp_path / "nodes.json").write_text(json.dumps({"A": {"x": 0, "y": 0}}))
    (tmp_path / "edges.json").write_text(json.dumps({"A": ["X"]}))
    (tmp_path / "danger.json").write_text("[]")
    with pytest.raises(ValueError, match="unknown node"):
        load_graph(tmp_path)


def test_load_graph_rejects_asymmetric_edge(tmp_path):
    (tmp_path / "nodes.json").write_text(
        json.dumps({"A": {"x": 0, "y": 0}, "B": {"x": 1, "y": 0}})
    )
    (tmp_path / "edges.json").write_text(json.dumps({"A": ["B"], "B": []}))
    (tmp_path / "danger.json").write_text("[]")
    with pytest.raises(ValueError, match="asymmetric"):
        load_graph(tmp_path)


# -- dijkstra ---------------------------------------------------------


def test_dijkstra_simple_path(graph):
    path = dijkstra(graph, "A", "B")
    assert path == ["A", "B"]


def test_dijkstra_avoids_danger_node(graph):
    # Without danger filter, A→F shortest is A-B-C-E-F (E is danger).
    # With danger filter, A→F goes A-B-C-D-F.
    path = dijkstra(graph, "A", "F")
    assert "E" not in path
    assert path[0] == "A"
    assert path[-1] == "F"


def test_dijkstra_to_danger_node_raises(graph):
    with pytest.raises(DangerDestinationError):
        dijkstra(graph, "A", "E")


def test_dijkstra_no_route_when_danger_isolates(graph):
    # Z only connects via E (danger). Excluding E, Z is unreachable.
    with pytest.raises(NoRouteError):
        dijkstra(graph, "A", "Z")


def test_dijkstra_invalid_from_raises(graph):
    with pytest.raises(InvalidNodeError):
        dijkstra(graph, "Q", "F")


def test_dijkstra_invalid_to_raises(graph):
    with pytest.raises(InvalidNodeError):
        dijkstra(graph, "A", "Q")


def test_dijkstra_same_node(graph):
    assert dijkstra(graph, "A", "A") == ["A"]


# -- assert_connected -------------------------------------------------


def test_assert_connected_adjacent(graph):
    assert_connected(graph, "A", "B")  # no exception


def test_assert_connected_not_adjacent(graph):
    with pytest.raises(NotConnectedError):
        assert_connected(graph, "A", "F")


def test_assert_connected_invalid_node(graph):
    with pytest.raises(InvalidNodeError):
        assert_connected(graph, "A", "Q")
