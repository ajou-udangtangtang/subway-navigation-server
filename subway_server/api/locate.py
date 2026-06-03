from flask import current_app, jsonify, request

from ..core import nav_progress
from ..core.locate_filter import estimate_excluding
from ..core.locator import WifiSample, estimate
from . import bp
from .errors import EmptyWifiError, InvalidPayloadError, KnnError


@bp.route("/locate", methods=["POST"])
def locate():
    """현 위치 확인 (Wi-Fi Fingerprinting + KNN)
    ---
    tags:
      - locate
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [wifi]
          properties:
            wifi:
              type: array
              description: 측정된 Wi-Fi AP 목록
              items:
                type: object
                required: [bssid, rssi]
                properties:
                  bssid: { type: string, example: "aa:bb:cc:dd:ee:ff", description: AP MAC 주소 }
                  rssi:  { type: number, example: -65, description: "신호 세기 (dBm). int·float 모두 허용 (평균값 float 가능)" }
                  ssid:  { type: string, example: "Korail_WiFi_Free", description: "AP 이름 (선택). 보내면 서버측 이동성 기기 필터가 활성화됨" }
            exclude:
              type: array
              description: "(선택) 이미 지나온 노드 ID 목록. 보내면 해당 노드들을 후보에서 제외하고 추정 (예: 개찰구를 지났는데 계속 개찰구로 잡히는 문제 완화). 'passed' 로도 동일하게 동작. 누락 시 기존 동작."
              items: { type: string }
              example: ["station_exit", "fare_gate"]
          example:
            wifi:
              - { bssid: "aa:bb:cc:dd:ee:ff", rssi: -65, ssid: "Korail_WiFi_Free" }
              - { bssid: "11:22:33:44:55:66", rssi: -72, ssid: "Public WiFi Free" }
              - { bssid: "77:88:99:aa:bb:cc", rssi: -88, ssid: "U+zone" }
            exclude: ["station_exit", "fare_gate"]
    responses:
      200:
        description: 추정된 노드 ID
        schema:
          type: object
          properties:
            node: { type: string, example: "down_platform" }
      400:
        description: INVALID_PAYLOAD / EMPTY_WIFI
        schema:
          type: object
          properties:
            error:
              type: object
              properties:
                code:    { type: string, example: "EMPTY_WIFI" }
                message: { type: string, example: "'wifi' must not be empty" }
      500:
        description: KNN_ERROR — 추정 모듈 미등록 또는 내부 오류
        schema:
          type: object
          properties:
            error:
              type: object
              properties:
                code:    { type: string, example: "KNN_ERROR" }
                message: { type: string, example: "No estimator registered. ..." }
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
        # rssi 는 int 또는 float 허용 (앱이 최근 N개 평균을 보내면 float).
        # bool 은 isinstance(True, int) 가 True 라 명시적으로 배제.
        if (
            not isinstance(bssid, str)
            or isinstance(rssi, bool)
            or not isinstance(rssi, (int, float))
        ):
            raise InvalidPayloadError(
                "Each wifi item requires string bssid and numeric rssi"
            )
        # ssid 는 선택. 있으면 서버측 이동성 기기 필터(wifi_filter)가 활용.
        ssid = item.get("ssid")
        if ssid is not None and not isinstance(ssid, str):
            raise InvalidPayloadError("'ssid' must be a string if provided")
        samples.append(WifiSample(bssid=bssid, rssi=float(rssi), ssid=ssid))

    # 선택: 이미 지나온 노드(경로 진행상 통과한 노드)를 후보에서 제외.
    # 'exclude' / 'passed' 둘 다 허용. 없으면 기존 동작과 100% 동일.
    exclude_raw = payload.get("exclude")
    if exclude_raw is None:
        exclude_raw = payload.get("passed")
    exclude: set[str] = set()
    if exclude_raw is not None:
        if not isinstance(exclude_raw, list) or not all(
            isinstance(x, str) for x in exclude_raw
        ):
            raise InvalidPayloadError(
                "'exclude'/'passed' must be a list of node id strings"
            )
        exclude = set(exclude_raw)
    elif current_app.config.get("AUTO_EXCLUDE_PASSED"):
        # [임시/시연] 앱이 명시 안 하면 /route·/direction 진행상황으로 추론한
        # '지나온 노드'를 자동 제외 (nav_progress).
        exclude = nav_progress.get_exclude()

    try:
        if exclude:
            node_id = estimate_excluding(samples, exclude)
        else:
            node_id = estimate(samples)
    except NotImplementedError as e:
        raise KnnError(str(e)) from e
    except Exception as e:
        raise KnnError(f"Estimator failed: {e}") from e

    return jsonify(node=node_id)
