# 2026-05-31 — 화경 PR #3 (마스킹 거리 KNN) main 머지 후 라이브 서버 갱신

## 한 일
- `git pull` 로 화경님 PR #3 머지본 동기화 (`e2e1057..78e9b84`)
  - `0cdf46f` raw 개별 스캔 학습 시도 (이후 폐기)
  - `76bfd0e` **마스킹 거리(measured-only distance)** 채택 — dropout 환경 21%→87.5%
  - `c17c0e8` 화경 worklog (2026-05-28)
  - `78e9b84` PR #3 머지 commit
- 기존 Flask·ngrok 종료 후 재기동
  - Flask :5001 (새 KNN 적용)
  - ngrok 고정 dev 도메인: `--url=sporty-press-unfeeling.ngrok-free.dev`
- 검증
  - `pytest tests/unit tests/integration -q` → 66 passed (그린 유지)
  - `scripts/verify_api_with_real_data.py` → locate 110/110, route 110/110, direction 20/20
  - 공개 URL `/locate` 응답 변화 관찰: 동일 입력(`down_platform` BSSID들)에 대해 이전 `b1_stairs` → 현재 `down_platform` (실제로 더 정확해짐)

## 왜 이렇게 했는지
- **마스킹 거리의 동기**: 지하철역은 사람·기둥에 막혀 AP 가 자주 누락됨. 기존 KNN 은 누락 AP 를 -100 으로 채워 *"측정 안 됨"* 을 *"멀다"* 로 처리해 오인식. 마스킹은 잡힌 AP 로만 거리 계산해 dropout 강건.
- **본인 변경 없음** — knn.py 는 화경 영역, locator.py 의 contract(`estimate(samples) -> str`) 그대로라 `register_estimator` 도 그대로 작동.
- **자체 검증 스크립트는 데이터 누수**라 110/110 유지가 정상 (학습=검증). 진짜 개선치는 화경님 dropout 시뮬레이션 결과(21%→87.5%) 참고.

## 막힌 것 / 결정 미뤄진 것
- 현장 신규 측정 데이터로 마스킹 거리 KNN held-out 정확도 확인 필요 (현장 테스트 단계)
- 안드로이드 통합 테스트 시간 미정

## 다음에 할 일
- 단톡방에 *"서버 새 KNN 반영됨, 통합 테스트 시간 정하자"* 의향 묻기
- 현장 테스트에서 dropout 환경 실측 정확도 확인

## 관련 커밋
- pull 만 했고 본인 추가 코드 변경 없음
- 머지된 커밋: `78e9b84` (Merge PR #3)
