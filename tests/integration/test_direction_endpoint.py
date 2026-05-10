def test_direction_happy_path(client):
    # A=(0,0) → B=(5,0) is east → 90°
    res = client.post("/direction", json={"from": "A", "to": "B"})
    assert res.status_code == 200
    assert res.get_json() == {"angle": 90.0}


def test_direction_invalid_node_returns_400(client):
    res = client.post("/direction", json={"from": "A", "to": "Q"})
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "INVALID_NODE"


def test_direction_not_connected_returns_400(client):
    # A and F are not directly connected.
    res = client.post("/direction", json={"from": "A", "to": "F"})
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "NOT_CONNECTED"


def test_direction_missing_field_returns_400(client):
    res = client.post("/direction", json={"from": "A"})
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "INVALID_PAYLOAD"


def test_direction_non_json_body_returns_400(client):
    res = client.post(
        "/direction", data="not-json", content_type="application/json"
    )
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "INVALID_PAYLOAD"
