def test_route_happy_path(client):
    res = client.post("/route", json={"from": "A", "to": "F"})
    assert res.status_code == 200
    body = res.get_json()
    # Path must avoid danger node E.
    assert "E" not in body["path"]
    assert body["path"][0] == "A"
    assert body["path"][-1] == "F"


def test_route_excludes_danger_specific_path(client):
    # In the 6-node-plus-Z fixture, the only safe A→F path is A-B-C-D-F.
    res = client.post("/route", json={"from": "A", "to": "F"})
    assert res.get_json()["path"] == ["A", "B", "C", "D", "F"]


def test_route_to_danger_returns_400(client):
    res = client.post("/route", json={"from": "A", "to": "E"})
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "DANGER_DESTINATION"


def test_route_unreachable_returns_404(client):
    # Z is reachable only via danger E.
    res = client.post("/route", json={"from": "A", "to": "Z"})
    assert res.status_code == 404
    assert res.get_json()["error"]["code"] == "NO_ROUTE"


def test_route_invalid_node_returns_400(client):
    res = client.post("/route", json={"from": "A", "to": "Q"})
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "INVALID_NODE"


def test_route_missing_field_returns_400(client):
    res = client.post("/route", json={"from": "A"})
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "INVALID_PAYLOAD"
