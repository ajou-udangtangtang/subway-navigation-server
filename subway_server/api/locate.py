from flask import jsonify, request

from ..core.locator import WifiSample, estimate
from . import bp
from .errors import EmptyWifiError, InvalidPayloadError, KnnError


@bp.route("/locate", methods=["POST"])
def locate():
    """현 위치 확인 (Wi-Fi Fingerprinting + KNN)
    ---
    tags:
      - locate
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [wifi]
            properties:
              wifi:
                type: array
                items:
                  type: object
                  required: [bssid, rssi]
                  properties:
                    bssid: { type: string,  example: "aa:bb:cc:dd:ee:ff" }
                    rssi:  { type: integer, example: -65 }
    responses:
      200:
        description: 추정된 노드 ID
        content:
          application/json:
            schema:
              type: object
              properties:
                node: { type: string, example: "B" }
      400:
        description: INVALID_PAYLOAD / EMPTY_WIFI
      500:
        description: KNN_ERROR — 추정 모듈 미등록 또는 내부 오류
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise InvalidPayloadError("Body must be a JSON object")

    wifi = payload.get("wifi")
    if not isinstance(wifi, list):
        raise InvalidPayloadError("'wifi' must be a list")
    if len(wifi) == 0:
        raise EmptyWifiError("'wifi' must not be empty")

    samples: list[WifiSample] = []
    for item in wifi:
        if not isinstance(item, dict):
            raise InvalidPayloadError("Each wifi item must be an object")
        bssid = item.get("bssid")
        rssi = item.get("rssi")
        if not isinstance(bssid, str) or not isinstance(rssi, int):
            raise InvalidPayloadError(
                "Each wifi item requires string bssid and integer rssi"
            )
        samples.append(WifiSample(bssid=bssid, rssi=rssi))

    try:
        node_id = estimate(samples)
    except NotImplementedError as e:
        raise KnnError(str(e)) from e
    except Exception as e:
        raise KnnError(f"Estimator failed: {e}") from e

    return jsonify(node=node_id)
