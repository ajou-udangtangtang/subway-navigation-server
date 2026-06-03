# 2026-06-03 — /locate 에 '지나온 노드 제외' 옵션 추가 (현장 이슈 대응)

## 한 일
- `/locate` 에 옵션 파라미터 `exclude`(별칭 `passed`) 추가 — 지나온 노드를 후보에서 빼고 추정. 누락 시 기존 동작 100% 동일(하위호환).
- 헬퍼 `subway_server/core/locate_filter.py` 신설 — knn.py 의 마스킹거리+k=5 투표를 복제하되 exclude 라벨 제외. Swagger docstring·검증(400) 추가.
- 회귀 66 그린, 서버·ngrok 재기동, 실 엔드포인트로 검증 완료.

## 왜 (현장 데이터로 검증된 근거)
- 증상: 개찰구 지나 계단으로 가도 측위가 개찰구에 고정 (계단에 폰 두고도 8연속 개찰구).
- 원인: 계단 위치 신호의 노드 거리 1위 fare_gate(65.8), **2위 floor1_stairs(84.5)**. 개찰구가 데이터빨(51 vs 26)로 1등 차지.
- 검증: 계단 신호 재생 시
  - exclude 없음 → 개찰구
  - 개찰구만 제외 → 출입구 (투표상 출입구가 올라옴 — **직전 1개만 빼면 부족**)
  - **출입구+개찰구 제외 → 계단** ✓
  → 앱은 "지나온 노드 전체 리스트"를 보내야 함.
- top-20 AP 필터 가설은 **반증됨**(상위 10개로 줄여도 개찰구) — AP 개수 문제 아님.

## 막힌 것 / 임시인 부분
- ⚠️ `locate_filter.py` 는 **임시 프로토타입**: knn.py(화경) 거리식을 복제하고 통합 seam(locator.estimate)을 우회함. 정식판은 화경이 `knn_estimate(samples, exclude=...)` 추가 시 이 파일 제거하고 seam 통해 호출로 교체. knn 거리식 변경 시 동기화 필요.
- 앱(최수빈)이 `/locate` 에 `exclude`/`passed` 배열(지나온 노드 전체)을 실제로 보내야 폰에서 효과 발생. 현재는 서버 준비만 됨(미사용 시 무영향).

## 다음에 할 일
- 인터페이스 합의: 앱이 `passed` 배열 전송 → 폰 라이브 테스트
- 화경 knn.py 정식 exclude 반영 시 locate_filter.py 제거

## 관련 커밋
- (이 커밋) feat(locate): exclude/passed 옵션 추가 + locate_filter 헬퍼
