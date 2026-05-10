from flask import current_app, jsonify, request

from ..core.graph import GraphData, dijkstra
from . import bp
from .errors import InvalidPayloadError


@bp.route("/route", methods=["POST"])
def route():
    """경로 탐색 (위험 노드 자동 회피)
    ---
    tags:
      - route
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [from, to]
            properties:
              from: { type: string, example: "A" }
              to:   { type: string, example: "F" }
    responses:
      200:
        description: 경로 (출발지 → 목적지 노드 ID 순서 배열)
        content:
          application/json:
            schema:
              type: object
              properties:
                path:
                  type: array
                  items: { type: string }
                  example: ["A", "B", "C", "D", "F"]
      400:
        description: INVALID_NODE / DANGER_DESTINATION / INVALID_PAYLOAD
      404:
        description: NO_ROUTE — 위험 노드 제외 시 도달 불가
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise InvalidPayloadError("Body must be a JSON object")
    a = payload.get("from")
    b = payload.get("to")
    if not isinstance(a, str) or not isinstance(b, str):
        raise InvalidPayloadError("'from' and 'to' must be strings")

    graph: GraphData = current_app.config["GRAPH"]
    path = dijkstra(graph, a, b)
    return jsonify(path=path)
