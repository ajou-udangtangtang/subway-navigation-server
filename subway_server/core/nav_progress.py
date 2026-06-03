"""[임시/시연] 경로 진행상황 추적 — 앱 변경 없이 '지나온 노드' 자동 추론.

배경:
  개찰구를 지나 계단으로 가도 측위가 개찰구에 고정되는 문제. 해결책인
  '지나온 노드 제외'를 쓰려면 누가 지나온 노드를 알려줘야 하는데, 앱은 아직
  /locate 에 passed 를 안 보낸다. 그러나 앱은 이미:
    - /route 로 경로(노드 순서)를 받고,
    - /direction(from=현재노드, to=다음노드) 로 현재 어느 구간을 안내 중인지 알린다.
  → 서버가 이 둘을 관찰하면 "경로상 from 까지는 지났다"를 추론할 수 있다.

동작:
  - /route 성공     → 현재 경로(노드 순서) 저장 + 진행 리셋
  - /direction(from)→ 경로상 from 의 인덱스까지 진행 (단조: 뒤로 안 감)
  - /locate         → 경로상 progress 인덱스까지(포함) 노드를 exclude 로 제공

⚠️ 단일 클라이언트(시연 폰) 기준 전역 상태. 정식판은 앱이 passed 를 직접
   보내거나 화경 knn_estimate(exclude=) 사용. config.AUTO_EXCLUDE_PASSED 로 토글.
"""
from typing import List, Set

_route: List[str] = []
_progress_idx: int = -1  # 지나온(=현재 안내 from) 노드의 경로상 최대 인덱스. -1 = 시작전


def set_route(path_nodes: List[str]) -> None:
    """/route 결과로 경로 순서 저장하고 진행 리셋 (새 내비게이션 세션)."""
    global _route, _progress_idx
    _route = list(path_nodes)
    _progress_idx = -1


def mark_from(node: str) -> None:
    """/direction(from=node) 관찰 — 경로상 node 인덱스까지 진행(단조 증가)."""
    global _progress_idx
    if node in _route:
        _progress_idx = max(_progress_idx, _route.index(node))


def get_exclude() -> Set[str]:
    """현재까지 지나온 노드 집합 (경로 시작 ~ progress 인덱스 포함)."""
    if not _route or _progress_idx < 0:
        return set()
    return set(_route[: _progress_idx + 1])


def reset() -> None:
    global _route, _progress_idx
    _route = []
    _progress_idx = -1
