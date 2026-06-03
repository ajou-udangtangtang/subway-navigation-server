"""[시연] 측위 결과 스무딩 — 경로상 1칸씩 전진 + N회 연속 확인.

문제:
  - 비슷한 1층 노드들이 헷갈려 위치가 앞/뒤로 튀거나, 계단에서 다 못 내려갔는데
    다음 노드로 일찍 인식됨.
목표 (데이터/KNN 안 건드리는 빠른 보정):
  - 경로 순서를 알고 있으니, /locate 원결과(raw)를 그대로 쓰지 말고:
    1) 뒤로 안 감 (backward 무시)
    2) 한 번에 한 칸만 전진 (먼 점프 무시)
    3) 다음 노드가 N회(기본 2) 연속 잡힐 때만 전진 확정
  - ⚠️ 노드를 '제외'하지 않음 → 출발 노드도 정상 인식 (B안 버그 회피).
    raw 가 현재 노드면 그대로 유지되므로 시작점에서 멋대로 전진하지 않음.

상태: 단일 시연 폰 기준 전역. config.SMOOTH_LOCATE 로 토글.
"""
from typing import List, Optional

_CONFIRM = 1  # 다음 노드 확인 횟수. 폴링이 노드당 1회꼴로 듬성해서 1 권장
              # (2 이상이면 전진이 뒤처짐 — 리플레이로 확인). 뒤로금지+1칸씩은 유지.

_route: List[str] = []
_idx: int = 0          # 현재 확정 노드의 경로상 인덱스
_pending: int = 0      # 다음 노드 후보 연속 카운트


def set_route(path_nodes: List[str]) -> None:
    global _route, _idx, _pending
    _route = list(path_nodes)
    _idx = 0
    _pending = 0


def smooth(raw_node: str) -> str:
    """raw 측위 결과를 경로 기반으로 보정해 확정 노드를 반환."""
    global _idx, _pending
    if not _route or raw_node not in _route:
        return raw_node  # 경로 없거나 경로밖 노드면 원결과 그대로

    ri = _route.index(raw_node)
    if ri <= _idx:
        # 현재 노드이거나 뒤 → 유지 (뒤로 안 감, 흔들림 흡수)
        _pending = 0
    else:
        # 앞 노드 감지 → 연속 확인 후 '한 칸만' 전진
        _pending += 1
        if _pending >= _CONFIRM:
            _idx += 1
            _pending = 0
    return _route[_idx]


def reset() -> None:
    global _route, _idx, _pending
    _route = []
    _idx = 0
    _pending = 0


def state() -> dict:
    return {"route_len": len(_route), "idx": _idx, "pending": _pending,
            "current": _route[_idx] if _route else None}
