from flask import current_app, jsonify, request

from ..core.direction import angle_between
from ..core.graph import GraphData, assert_connected
from . import bp
from .errors import InvalidPayloadError


@bp.route("/direction", methods=["POST"])
def direction():
    """노드 간 절대 방향 산출
    ---
    tags:
      - direction
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [from, to]
            properties:
              from: { type: string, example: "A" }
              to:   { type: string, example: "B" }
    responses:
      200:
        description: 절대 각도 (정북=0°, 시계방향)
        content:
          application/json:
            schema:
              type: object
              properties:
                angle: { type: number, example: 90.0 }
      400:
        description: INVALID_NODE / NOT_CONNECTED / INVALID_PAYLOAD
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: object
                  properties:
                    code:    { type: string }
                    message: { type: string }
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise InvalidPayloadError("Body must be a JSON object")
    a = payload.get("from")
    b = payload.get("to")
    if not isinstance(a, str) or not isinstance(b, str):
        raise InvalidPayloadError("'from' and 'to' must be strings")

    graph: GraphData = current_app.config["GRAPH"]
    assert_connected(graph, a, b)

    angle = angle_between(graph.coord(a), graph.coord(b))
    return jsonify(angle=angle)
