"""[임시/프로토타입] '지나온 노드 제외' 측위 — 2026-06-03 현장 테스트용.

배경:
  개찰구를 지나 계단으로 가도 측위가 개찰구에 고정되는 문제.
  (개찰구 fingerprint 가 데이터가 많아 계단 구역까지 지배)
  이미 지나온 노드를 후보에서 제외하면 다음 노드가 선택된다.
  현장 데이터 검증: 계단 위치 신호에서 출입구+개찰구 제외 → 계단(floor1_stairs) 정답.
  주의: "직전 노드 1개"만 빼면 부족(투표상 출입구가 올라옴) — 지나온 노드 전체를 받는다.

⚠️ 임시 구현:
  core/knn.py(화경) 의 마스킹거리 + k=5 거리가중투표 로직을 **그대로 복제**한다.
  통합 seam(locator.estimate)을 거치지 않고 knn 모듈의 로드된 학습데이터를 직접 쓴다.
  정식판: 화경이 knn_estimate(samples, exclude=...) 를 추가하면 이 파일은 제거하고
  locate.py 는 estimate(samples, exclude=...) 호출로 돌린다.
  knn.py 의 거리식이 바뀌면 이 파일도 동기화 필요.
"""
from typing import List, Set

import numpy as np
from flask import current_app

from . import knn
from .locator import WifiSample
from .wifi_filter import filter_wifi_samples


def estimate_excluding(samples: List[WifiSample], exclude: Set[str]) -> str:
    """지나온 노드(exclude)를 후보에서 제외하고 가장 가까운 노드를 추정.

    exclude 가 비어있으면 knn.knn_estimate 와 동일 결과를 낸다.
    """
    if not samples:
        raise ValueError("Empty Wi-Fi samples")

    filtered = filter_wifi_samples(samples)
    if not filtered:
        raise ValueError("All Wi-Fi samples below RSSI threshold")

    knn._ensure_loaded()
    if knn._train_X is None or len(knn._train_X) == 0:
        raise RuntimeError("KNN classifier not initialized — no fingerprint data")

    # 측정된 AP 중 학습 벡터에 존재하는 차원만 추출 (knn.py 와 동일)
    measured_idx: List[int] = []
    measured_rssi: List[float] = []
    for s in filtered:
        idx = knn._bssid_index.get(s.bssid)
        if idx is not None:
            measured_idx.append(idx)
            measured_rssi.append(s.rssi)
    if not measured_idx:
        raise ValueError("No measured AP overlaps with fingerprint BSSIDs")

    q = np.array(measured_rssi, dtype=np.float32)
    dists = np.sqrt(np.sum((knn._train_X[:, measured_idx] - q) ** 2, axis=1))
    y = knn._train_y

    k = current_app.config.get("KNN_K", knn._DEFAULT_K)
    # exclude 라벨을 뺀 뒤 k 최근접 거리가중 투표 (knn.py 와 동일 방식)
    order = [int(i) for i in np.argsort(dists) if str(y[i]) not in exclude]
    if not order:
        raise ValueError("All candidate nodes excluded")
    order = order[:k]

    votes: dict = {}
    for i in order:
        label = str(y[i])
        votes[label] = votes.get(label, 0.0) + 1.0 / (float(dists[i]) + 1e-6)
    return max(votes, key=votes.get)
